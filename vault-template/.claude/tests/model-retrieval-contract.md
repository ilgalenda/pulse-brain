# Fixture: the Model and Retrieval Substrate contract

The acceptance checklist the **Model and Retrieval Substrate**
([`MODEL-RETRIEVAL.md`](../../../MODEL-RETRIEVAL.md), Brain-OS layer 10) must pass. It has
two halves matching the layer. **Part A** covers model orchestration (the `resolve-model` tool,
the bindings-as-instance-config, the tiering exemplar). **Part B** covers the semantic-retrieval
shell (`substrate/`: derived-cache store, re-rank-only, staleness guard, single-writer
atomic write, candidates-only). Throughout, the governing rule is **re-rank, never
retrieve-instead-of-compile** (§1), together with the **determinism split** below. This restates the
authority as a *test*, not a new authority. If any item fails, the layer is not correct.

> **The determinism split (read first).** Unlike `graph-health-scan` and `session-reconcile`,
> this layer contains a non-deterministic component: a real embedding model varies across
> version, hardware, and float precision. So the bar is split. The **deterministic shell**
> (resolver, content-hash keying, the staleness guard, the atomic write, the
> re-rank/candidate *shape*) is asserted exactly, with the embedder stubbed by the
> dependency-free `StubEmbedder`. The **embedder itself** is asserted by *property and
> tolerance* (stable within an epsilon, order-invariant on re-run), **never** by a
> golden-vector fixture. A test that pins exact embedding floats is wrong by construction.

## Part A: model orchestration

- [ ] **The resolver is deterministic and session-free.** `resolve-model <bindings> <role>`
      returns the bound model for a role; an unbound role returns `--default` (the session
      model the *caller* passes in) or the `(session-model)` sentinel. It reads the bindings
      file ONLY, never `core.md` or session state, so the same (file, role, default) gives a
      byte-identical answer regardless of any cache state. A duplicate binding for one role,
      or a missing file, exits 2.
- [ ] **Bindings are instance config, not engine content.** The engine ships
      [`model-bindings.md`](../model-bindings.md) commented and placeholdered; concrete model
      ids are populated when you instantiate your brain (the watchlist / preset pattern). A role absent from the file
      resolves to the session model, so the brain runs un-bound. Populating it *tunes*
      routing; it is never a prerequisite.
- [ ] **The binding rule lives in the Builder's authority.** `instruments.md` §1 carries
      the role-to-model rule, and the Builder's `create-agent` calls `resolve-model` when it stamps
      a new instrument's `model:`. There is no parallel registry in this layer.
- [ ] **Orchestration is at task boundaries, not a runtime interceptor.** The resolver sets
      a subagent's declared `model:` or a spawn's `model`; it does NOT (cannot) swap the main
      loop's model mid-turn. The main loop's model is documented (recommended: Opus), set via
      `/model`, not bound by the resolver.
- [ ] **The tiering exemplar is rationale, generic.** `MODEL-RETRIEVAL.md` §2.4 documents
      Opus loop, strong hard-workers, balanced default-worker, and fast extraction, with the
      *why* (the loop's canon writes are non-delegable; mechanical work gains nothing from a
      strong model). The **cost model** ships as levers plus reasoning only (cache the stable
      prefix; tier the workers), with **no modelled figures or usage volumes** (these are instance-specific
      and sit behind the data boundary).
- [ ] **No metered self-tuning loop.** Nothing claims or consumes per-route cost or rework
      telemetry (uncapturable at this tier, and not a Node-Graph signal). A real routing signal
      would be a tier-3 ontology addition: named deferred, not built. No bespoke model-monitor
      agent.

## Part B: the semantic-retrieval shell

- [ ] **The store is a derived cache; canon wins.** The vector store is rebuildable from
      canon and never authoritative. Embedding is out-of-band (not the kernel §8 same-step
      rule). Indexing is incremental by content-hash: an unchanged page is skipped, and a deleted
      page's shard is pruned.
- [ ] **The staleness guard is first-class.** A candidate whose page content-hash differs from its
      shard's hash (edited but not yet reindexed) is treated as **stale, demoted to graph
      order**, never trusted. A missing shard is stale.
- [ ] **Re-rank only: adds nothing, drops nothing.** `rerank(candidate_ids, …)` returns a
      *permutation* of exactly its input ids: fresh candidates by descending similarity, then
      stale or missing ones in original graph order. There is **no code path** that surfaces a page
      outside the candidate set into a read-routing result (compile-don't-retrieve, §1).
- [ ] **Graph-distant similars are edge-candidates, separate.** `edge_candidates(…)` emits
      pages *outside* the anchor/candidate set for the **Thinking layer** to propose as edges;
      it is never folded into a rerank result.
- [ ] **Candidates only, threshold-gated.** `semantic_duplicates` and `edge_candidates` output
      candidates for {{OWNER}}/Thinking, **never auto-merge or auto-write**, and **refuse** (raise)
      without a calibrated threshold rather than apply a guessed cut. Thresholds are instance
      config, calibrated when you instantiate your brain.
- [ ] **Single-writer-safe in the multi-tab world.** Shards are per-page (collision-free
      new-file writes), and the whole-store rebuild is staged-then-renamed (the `session-reconcile`
      `write_atomic` precedent). Two tabs reindexing cannot tear the store. Vector-store health
      is its own lane, never folded into the deterministic `graph-health-scan`.
- [ ] **Local-first, honestly framed.** The `StubEmbedder` runs cold (no deps, no key); the
      `LocalAdapter` is zero-*API*-config (not zero-install) and **fails closed** on a model
      checksum mismatch; the `ApiAdapter` activates only when its key env var is set. Sources,
      if embedded, are fenced to dedup, never a read/answer surface.
- [ ] **Data boundary holds.** The store, embeddings, and pulled model are derived live
      content / runtime state: gitignored, never committed. The engine ships code plus contracts
      plus this fixture only.

## Worked PASS example (the shell, run cold with the stub)

> The shipped synthetic corpus `tests/fixtures/model-retrieval/` (no live data) has three
> pages: `topics/tea.md`, `topics/coffee.md` (both hot beverages), and `topics/bicycle.md`
> (unrelated), plus a `_index.md`. From `vault-template/.claude/` (so the package
> imports), with `V=tests/fixtures/model-retrieval` and a throwaway `S=/tmp/pulse-store`:
>
> ```
> python3 -m substrate index  $V --adapter stub --store $S                 # → indexed 3 (incremental)
> python3 -m substrate index  $V --adapter stub --store $S                 # → indexed 0, skipped 3
> python3 -m substrate index  $V --adapter stub --store $S --rebuild       # → rebuilt 3 (atomic full swap)
> python3 -m substrate search $V --query "hot drink" \
>   --candidates topics/bicycle.md,topics/tea.md,topics/coffee.md --adapter stub --store $S
>   # → the SAME three ids, re-ordered (a permutation; none added, none dropped)
> python3 -m substrate dedup  $V --adapter stub --store $S                 # → refuses, exit 2 (no threshold)
> python3 -m substrate dedup  $V --threshold 0.5 --adapter stub --store $S # → runs, candidates only
> ```
>
> To see the staleness guard, copy the corpus to a tmp dir (never mutate the committed
> fixture), edit one page there, and re-run `search` **without** reindexing: the edited
> page's hash no longer matches its shard, so it is **demoted to graph order** (it sorts
> after the fresh candidates), not trusted on a stale vector. A re-`index` re-embeds only
> that page (or `--rebuild` regenerates the whole store atomically).

*Why this is correct:* the pipeline runs with no model and no key (the stub), incremental
indexing skips unchanged pages, re-rank returns a permutation of the candidate set, and the
staleness guard refuses to trust a vector whose page has moved on. The derived cache never
overrides canon.

## FAIL examples the layer must NOT produce

- **Recall expansion.** Any path that injects a page the graph walk did not surface into a
  read-routing result. Retrieval-instead-of-compile (§1/§5); the page belongs in the
  edge-candidate queue, not the result.
- **Trusting a stale vector.** Re-ranking a candidate whose page hash no longer matches its
  shard, silently demoting a freshly-correct page beneath a stale-similar one.
- **A golden-vector test.** Asserting exact embedding floats; the embedder is not
  deterministic across versions or hardware (use property/tolerance plus the stub).
- **An auto-merge or auto-written edge.** Applying a duplicate or similarity candidate
  without {{OWNER}}/Thinking judgement, or minting a new edge type unpromoted.
- **A guessed threshold shipped cold.** A hardcoded cosine cut presented as calibrated; the
  finders must refuse without an instance-tuned threshold.
- **A torn store under concurrency.** A non-atomic whole-store write, or a shared temp name,
  letting two tabs interleave bytes (use per-page shards plus staged-rename).
- **The resolver reading session state.** Resolving against `core.md` or the live session,
  making the same (file, role) return different models as the cache lags.
- **Committed embeddings or model.** A vector store, shard, or model artifact in the engine
  repo (derived live content: gitignored, never committed).
- **Cost figures in the engine.** Modelled token costs or usage volumes written into
  `MODEL-RETRIEVAL.md`; only the levers plus reasoning ship (instance figures are data).
- **A model pull without a checksum.** Fetching the local model without pinning and verifying
  it (fetched untrusted input must fail closed on mismatch).
