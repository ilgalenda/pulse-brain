# Substrate — the Model & Retrieval engine room

Engine code beneath the kernel — **not an instrument**. The authority is
[`MODEL-RETRIEVAL.md`](../../../MODEL-RETRIEVAL.md) (Brain-OS layer 10). This directory
exists because embedding generation needs the network (a model pull or an API) and
optional credentials, which the Builder `tool` kind forbids ([BUILDER.md §3](../../../BUILDER.md)) —
so it lives in its own `substrate/` lane under the [`instruments.md` §1](../instruments.md)
carve-out (instruments vs engine substrate). It is fronted by the
[`/reindex`](../commands/reindex.md) command; the substrate code itself is not
registry-listed.

## What ships now (the deterministic shell)

- `embedding.py` — the provider-agnostic interface + `StubEmbedder` (deterministic,
  dependency-free, for cold runs and tests), `LocalAdapter` (on-device; pinned id +
  checksum-on-pull, encode wired at S19), `ApiAdapter` (opt-in; key via `.env`).
- `store.py` — the vector store as an eventually-consistent **derived cache of canon**
  (canon always wins): per-page shards keyed by page-id + content-hash, atomic
  single-writer rebuild (the `session-reconcile` temp-then-rename precedent).
- `retrieval.py` — incremental indexing; **re-rank-only** read surface (re-orders the
  graph walk's candidates, adds none); a content-hash **staleness guard** (a stale vector
  is demoted to graph order, never trusted); duplicate + edge **candidate** finders
  (candidates only — never auto-applied; they require a calibrated threshold).
- `__main__.py` — `python -m substrate index|search|dedup <vault> ...` (defaults to the
  stub adapter, so it runs cold).

## What is deferred to S19

Threshold calibration (the relevance/duplicate cosine cut, tuned against real content),
the real model selection + pull, ranking-quality / dedup-precision evaluation, and
**turning re-ranking on in the kernel's read-routing**. Until then the shell is exercised
with the stub. See [`MODEL-RETRIEVAL.md §6`](../../../MODEL-RETRIEVAL.md).

## Data boundary

The store, the embeddings, and the pulled model are **derived live content / runtime
state** — instance-only, gitignored, **never committed** ([`MODEL-RETRIEVAL.md §5`](../../../MODEL-RETRIEVAL.md)).
The store materialises at runtime under `.claude/substrate/store/` in the live vault; the
engine ships the code and this README, not a store. Run cold from `vault-template/.claude/`
(so the package imports) against the shipped synthetic corpus:

```
python3 -m substrate index tests/fixtures/model-retrieval --adapter stub --store /tmp/pulse-store
```

