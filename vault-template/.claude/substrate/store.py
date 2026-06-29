"""store — the vector store as an eventually-consistent derived cache (MODEL-RETRIEVAL.md §3.2/§3.3).

ONE JOB: persist one vector per canon page, keyed by page-id + content-hash, so the store
is (a) a derived cache that is ALWAYS rebuildable from canon — never authoritative,
canon wins — and (b) single-writer-safe in S15's multi-tab world (DEVELOPMENT.md §3/§6),
because index integrity is NOT session-reconcile's lane.

Two write classes, both collision-free:
  - per-page SHARD writes — one file per page (a new-file / replace write, atomic via a
    process-unique temp-then-rename, the session-reconcile precedent); two tabs touching
    different pages never collide, and the same page is last-writer-wins on a clean file.
  - a full REBUILD — staged in a temp dir then renamed into place, so the whole store
    swaps atomically and a torn half-rebuild is never observable.

A shard records the content-hash it was embedded from; a page whose CURRENT hash differs
is STALE (the read-time guard — staleness demotes a candidate to graph order, it is never
trusted). Embedding is out-of-band (not the kernel's same-step integrity rule, §8).

BOUNDS: deterministic given its inputs; writes ONLY under the store dir; no network, no
credentials (the network lives in the embedding adapter, never here).
"""

import hashlib
import json
import os
import shutil

SHARDS_DIRNAME = "shards"


def content_hash(text):
    """The stable key for a page's current content. Same text → same hash."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _shard_filename(page_id):
    """A filesystem-safe, collision-free shard name for a page id.

    The id is hashed for the filename (page ids may contain '/', spaces, etc.); the id
    itself is stored inside the shard, so the mapping is recoverable and unambiguous. The
    `.shard` extension is what `.gitignore` matches (`*.shard`), so a store is ignored
    wherever `--store` points it, not only at the default path.
    """
    return hashlib.sha256(page_id.encode("utf-8")).hexdigest() + ".shard"


def _write_atomic(path, text):
    """temp-then-rename with a process-unique temp, so neither an interrupted write nor
    two concurrent tabs leave a torn file (the session-reconcile precedent)."""
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp, path)


def shards_dir(store_dir):
    return os.path.join(store_dir, SHARDS_DIRNAME)


def make_shard(page_id, page_hash, vector, model):
    """The self-describing shard record for a page (shared by single-write and rebuild)."""
    return {"id": page_id, "hash": page_hash, "model": model, "dim": len(vector), "vector": vector}


def write_shard(store_dir, page_id, page_hash, vector, model):
    """Persist one page's vector as a self-describing shard (atomic, single-page)."""
    directory = shards_dir(store_dir)
    os.makedirs(directory, exist_ok=True)
    shard = make_shard(page_id, page_hash, vector, model)
    _write_atomic(os.path.join(directory, _shard_filename(page_id)), json.dumps(shard, sort_keys=True))


def read_shard(store_dir, page_id):
    """Return a page's shard dict, or None if absent."""
    path = os.path.join(shards_dir(store_dir), _shard_filename(page_id))
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def all_shards(store_dir):
    """Every shard as {page_id: shard}, read deterministically (sorted by file)."""
    directory = shards_dir(store_dir)
    if not os.path.isdir(directory):
        return {}
    shards = {}
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".shard"):
            continue
        with open(os.path.join(directory, name), encoding="utf-8") as handle:
            shard = json.load(handle)
        shards[shard["id"]] = shard
    return shards


def is_stale(shard, current_hash):
    """A shard is stale when the page's current content-hash differs from the embedded
    one. A missing shard (None) is treated as stale by callers."""
    return shard is None or shard.get("hash") != current_hash


def remove_shard(store_dir, page_id):
    """Drop a page's shard (e.g. the page was deleted from canon). Idempotent."""
    path = os.path.join(shards_dir(store_dir), _shard_filename(page_id))
    if os.path.isfile(path):
        os.remove(path)


def _clear_rebuild_artifacts(store_dir):
    """Remove leftover staging dirs and backups from ANY crashed rebuild (any pid), so a
    crash never accumulates `.rebuild.*.tmp` / `.shards.*.old` turds (the latter a full
    store duplicate). Call only after _recover_interrupted_rebuild, so a backup that is
    still needed for recovery is consumed first."""
    if not os.path.isdir(store_dir):
        return
    for name in os.listdir(store_dir):
        if (name.startswith(".rebuild.") and name.endswith(".tmp")) or (
            name.startswith(".shards.") and name.endswith(".old")
        ):
            shutil.rmtree(os.path.join(store_dir, name), ignore_errors=True)


def _recover_interrupted_rebuild(store_dir):
    """Self-heal a rebuild that crashed in the swap gap.

    If a prior rebuild moved the live shards aside (`shards/` -> `.shards.<pid>.old`) but
    crashed before swapping the new set in, `shards/` is absent while a backup remains.
    Restore the newest backup so the store is never left empty by an interrupted swap.
    (The store is also rebuildable from canon, and a missing `shards/` degrades reads to
    graph order rather than corrupting anything — this is belt-and-braces.)
    """
    final = shards_dir(store_dir)
    if os.path.isdir(final) or not os.path.isdir(store_dir):
        return
    backups = sorted(n for n in os.listdir(store_dir) if n.startswith(".shards.") and n.endswith(".old"))
    if backups:
        os.replace(os.path.join(store_dir, backups[-1]), final)


def rebuild(store_dir, shards_by_id):
    """Replace the whole shard set, crash-safe and single-writer-safe.

    The only writer of the whole store at once — used to regenerate from canon wholesale
    (the derived-cache guarantee). On entry it self-heals any interrupted prior rebuild
    and clears stale turds; it stages the new set in a process-unique temp dir, then swaps
    by rename and cleans its own backup. The swap is two renames (POSIX cannot atomically
    replace a populated directory); a crash in the tiny gap is healed on the next run by
    _recover_interrupted_rebuild, and worst case the store rebuilds from canon.
    """
    os.makedirs(store_dir, exist_ok=True)
    _recover_interrupted_rebuild(store_dir)
    _clear_rebuild_artifacts(store_dir)
    staging = os.path.join(store_dir, f".rebuild.{os.getpid()}.tmp")
    os.makedirs(staging)
    for page_id, shard in shards_by_id.items():
        with open(os.path.join(staging, _shard_filename(page_id)), "w", encoding="utf-8") as handle:
            handle.write(json.dumps(shard, sort_keys=True))
    final = shards_dir(store_dir)
    if os.path.isdir(final):
        backup = os.path.join(store_dir, f".shards.{os.getpid()}.old")
        os.replace(final, backup)
        try:
            os.replace(staging, final)
        finally:
            shutil.rmtree(backup, ignore_errors=True)
    else:
        os.replace(staging, final)
