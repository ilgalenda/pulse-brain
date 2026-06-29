---
description: Rebuild or refresh the semantic vector index over canon, the Half-B substrate's incremental indexer. Re-embeds only changed pages; the index is a derived cache of canon, never authoritative.
argument-hint: [optional --adapter stub|local|api (default: the configured embedding adapter)]
---

Refresh the **semantic vector index** over the canon wiki (the Model and Retrieval
Substrate; see [`MODEL-RETRIEVAL.md`](../../../MODEL-RETRIEVAL.md) §3).

This fronts the engine [`substrate/`](../substrate/) code. The substrate is engine code,
not an instrument (the [`instruments.md` §1](../instruments.md) carve-out). The index is
an **eventually-consistent derived cache of canon**: canon always wins, and the index is
always rebuildable from it (§3.2). Run this when canon has changed enough that semantic
re-ranking would otherwise re-rank on stale vectors. Routine staleness is handled at read
time (a stale candidate is demoted to graph order, never trusted), so this is a
maintenance refresh, not a write the kernel depends on.

Run it from the brain's `.claude/` directory (so the `substrate` package imports),
pointing at the vault root, against the configured adapter (`$ARGUMENTS` may override it):

```
cd .claude && python3 -m substrate index .. --adapter <stub|local|api>
```

Add `--rebuild` to force a full atomic re-embed of every page (the derived-cache recovery
path; use it after a model change or a suspected corrupt store) instead of the
incremental default.

- **`stub`**: the dependency-free deterministic embedder; runs cold, used for tests.
- **`local`**: the on-device model (zero-API-config). It requires the model pull and
  checksum performed when you instantiate your brain (`MODEL-RETRIEVAL.md` §3.6).
- **`api`**: opt-in; requires the embedding key in `.env`.

Indexing is **incremental by content-hash**: unchanged pages are skipped, changed and new
pages are re-embedded, and pages removed from canon have their shards pruned. The store is
written single-writer-safe (per-page shards plus atomic rebuild), so a concurrent tab cannot
tear it ([DEVELOPMENT.md §6](../../../DEVELOPMENT.md) lane note). The store is **instance
runtime state, gitignored, never committed** (§5).

Report back: pages indexed, skipped, and removed, the adapter used, and any page that
failed to embed. The reindex cadence, threshold calibration, and turning semantic
re-ranking *on* in read-routing are **deferred to when you instantiate your brain**
([`scheduling.md`](../scheduling.md)). Until then `/reindex` maintains the index, but the
kernel's read-routing stays graph-first with semantic similarity as the reserved,
not-yet-active tie-breaker.
