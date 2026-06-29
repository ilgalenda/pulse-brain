"""retrieval — indexer, re-ranker, and candidate finders (MODEL-RETRIEVAL.md §1/§3.4/§3.5).

ONE JOB: maintain the derived vector store from canon pages, and use it to RE-RANK the
candidate set the graph walk already surfaced — never to retrieve pages the walk missed
(the compile-don't-retrieve boundary, OPERATIONS-KERNEL.md §5/§7.5). It also surfaces
duplicate and edge CANDIDATES (never auto-applied).

The load-bearing invariants this module enforces in code:
  - rerank() returns a permutation of its input candidate ids — it can drop nothing and
    ADD nothing. Recall expansion has no code path here.
  - a stale/missing candidate (current page hash != shard hash) is demoted to graph order,
    never trusted (the read-time staleness guard).
  - duplicate and edge-candidate finders REQUIRE a calibrated threshold (instance config,
    S19); with none they refuse rather than apply a guessed cut (the §9 silent-cap trap).
  - edge-candidates are emitted SEPARATELY (for the Thinking layer), never folded into a
    rerank result.

BOUNDS: deterministic given (pages, store, embedder, threshold). The only nondeterminism
is the embedder itself (a real model), which is why its tests are property/tolerance, not
golden-vector (MODEL-RETRIEVAL.md §7). No network/credentials here — those live in the
adapter.
"""

import math
import os

from . import store


def cosine(a, b):
    """Cosine similarity of two equal-length vectors. Unit vectors → plain dot product."""
    if len(a) != len(b):
        raise ValueError("vector dimension mismatch")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def read_canon_pages(canon_dir):
    """Read canon pages as {page_id: text}. page_id is the path relative to canon_dir.

    Skips the `_index.md` edge-maps and any dotfiles — those are infrastructure, not
    knowledge nodes (NODE-GRAPH.md §2). Deterministic order (sorted).
    """
    pages = {}
    for root, dirs, files in os.walk(canon_dir):
        # Prune hidden directories (.git, .obsidian, .trash, .claude, …) from the walk —
        # a basename filter alone would still descend into them and ingest their .md as
        # knowledge nodes. Sorted for deterministic traversal.
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in sorted(files):
            if not name.endswith(".md") or name == "_index.md" or name.startswith("."):
                continue
            path = os.path.join(root, name)
            page_id = os.path.relpath(path, canon_dir)
            with open(path, encoding="utf-8") as handle:
                pages[page_id] = handle.read()
    return pages


def index_pages(store_dir, pages, embedder, full_rebuild=False):
    """Refresh the store from the current pages — incremental by content-hash.

    Embeds only pages whose content changed (or are new); leaves unchanged shards alone;
    prunes shards for pages no longer in canon. Returns a deterministic summary dict.

    `full_rebuild=True` ignores the existing store and regenerates it wholesale via an
    atomic swap (store.rebuild) — the derived-cache recovery path: the store is always
    rebuildable from canon, so a corrupt or model-changed store is fixed by re-embedding
    every page and swapping the whole set in one rename (MODEL-RETRIEVAL.md §3.2).
    """
    if full_rebuild:
        shards = {}
        for page_id in sorted(pages):
            page_hash = store.content_hash(pages[page_id])
            vector = embedder.embed(pages[page_id])
            shards[page_id] = store.make_shard(page_id, page_hash, vector, embedder.name)
        store.rebuild(store_dir, shards)
        return {"indexed": sorted(pages), "skipped": [], "removed": [], "model": embedder.name, "rebuilt": True}

    existing = store.all_shards(store_dir)
    current_hashes = {pid: store.content_hash(text) for pid, text in pages.items()}

    indexed, skipped = [], []
    for page_id in sorted(pages):
        page_hash = current_hashes[page_id]
        shard = existing.get(page_id)
        if shard is not None and shard.get("hash") == page_hash:
            skipped.append(page_id)
            continue
        vector = embedder.embed(pages[page_id])
        store.write_shard(store_dir, page_id, page_hash, vector, embedder.name)
        indexed.append(page_id)

    removed = [pid for pid in sorted(existing) if pid not in pages]
    for page_id in removed:
        store.remove_shard(store_dir, page_id)

    return {"indexed": indexed, "skipped": skipped, "removed": removed, "model": embedder.name, "rebuilt": False}


def rerank(store_dir, query_text, candidate_ids, pages, embedder):
    """Re-order ONLY the given candidate ids by similarity to the query (the §7.5 slot).

    Returns the same ids, re-ordered: fresh candidates first (by descending similarity),
    then stale/missing candidates in their original graph order (the staleness guard —
    never trusts a stale vector). It cannot add an id outside `candidate_ids` and cannot
    drop one. This is the entire read-routing surface S17 touches.
    """
    query_vector = embedder.embed(query_text)
    fresh_scored, demoted = [], []
    for position, page_id in enumerate(candidate_ids):
        shard = store.read_shard(store_dir, page_id)
        current = store.content_hash(pages[page_id]) if page_id in pages else None
        # Demote (to graph order, never trusted) when the page is absent, the shard is
        # missing/stale, OR the stored vector's dimension differs from the query model's —
        # a dimension mismatch means the store was embedded by a different model and is
        # stale-by-model, exactly what --rebuild fixes. This keeps the no-raise permutation
        # invariant: rerank never calls cosine on mismatched vectors.
        if current is None or store.is_stale(shard, current) or len(shard["vector"]) != len(query_vector):
            demoted.append((position, page_id))  # graph order preserved
            continue
        fresh_scored.append((cosine(query_vector, shard["vector"]), position, page_id))
    # Sort fresh by similarity desc; ties break on original position, then id — total order.
    fresh_scored.sort(key=lambda item: (-item[0], item[1], item[2]))
    ranked = [page_id for _score, _pos, page_id in fresh_scored]
    ranked.extend(page_id for _pos, page_id in demoted)
    return ranked


def _require_threshold(threshold):
    if threshold is None:
        raise ValueError(
            "no calibrated threshold — duplicate/edge candidates need a cosine cut tuned "
            "against real content at S19; refusing to apply a guessed cut "
            "(MODEL-RETRIEVAL.md §3.6, the §9 silent-cap rule)"
        )


def semantic_duplicates(store_dir, pages, threshold):
    """Return near-duplicate page pairs (id_a, id_b, score) at or above `threshold`.

    CANDIDATES only — for {{OWNER}} / the Thinking layer to judge, never an auto-merge
    (NODE-GRAPH.md §6, the SELF-DEVELOPMENT autonomy gate). Compares only FRESH shards.
    Deterministic order (by score desc, then ids).
    """
    _require_threshold(threshold)
    shards = store.all_shards(store_dir)
    fresh = []
    for page_id in sorted(shards):
        if page_id in pages and not store.is_stale(shards[page_id], store.content_hash(pages[page_id])):
            fresh.append((page_id, shards[page_id]["vector"]))
    pairs = []
    for i in range(len(fresh)):
        for j in range(i + 1, len(fresh)):
            if len(fresh[i][1]) != len(fresh[j][1]):
                continue  # different embedding model/dim — not comparable, skip
            score = cosine(fresh[i][1], fresh[j][1])
            if score >= threshold:
                pairs.append((fresh[i][0], fresh[j][0], score))
    pairs.sort(key=lambda item: (-item[2], item[0], item[1]))
    return pairs


def edge_candidates(store_dir, anchor_ids, pages, embedder, threshold, exclude_ids):
    """Pages semantically near the anchors but OUTSIDE the candidate/anchor set — emitted
    as Thinking edge-candidates, NEVER injected into a rerank result (MODEL-RETRIEVAL.md
    §1/§3.4). The doctrine's fix for a relevant-but-distant page is edge-work; this is the
    mechanism that proposes that edge, not a recall path into read-routing.

    Returns (page_id, anchor_id, score) above `threshold`. Deterministic order.
    """
    _require_threshold(threshold)
    excluded = set(exclude_ids) | set(anchor_ids)
    anchors = []
    for anchor_id in anchor_ids:
        shard = store.read_shard(store_dir, anchor_id)
        if anchor_id in pages and not store.is_stale(shard, store.content_hash(pages[anchor_id])):
            anchors.append((anchor_id, shard["vector"]))
    shards = store.all_shards(store_dir)
    found = []
    for page_id in sorted(shards):
        if page_id in excluded or page_id not in pages:
            continue
        if store.is_stale(shards[page_id], store.content_hash(pages[page_id])):
            continue
        for anchor_id, anchor_vector in anchors:
            if len(anchor_vector) != len(shards[page_id]["vector"]):
                continue  # different embedding model/dim — not comparable, skip
            score = cosine(anchor_vector, shards[page_id]["vector"])
            if score >= threshold:
                found.append((page_id, anchor_id, score))
    found.sort(key=lambda item: (-item[2], item[0], item[1]))
    return found
