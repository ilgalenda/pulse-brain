# Substrate: the Model and Retrieval engine room

Engine code beneath the kernel, **not an instrument**. The authority is
[`MODEL-RETRIEVAL.md`](../../../MODEL-RETRIEVAL.md) (Brain-OS layer 10). This directory
exists because embedding generation needs the network (a model pull or an API) and
optional credentials, which the Builder `tool` kind forbids ([BUILDER.md §3](../../../BUILDER.md)).
So it lives in its own `substrate/` lane under the [`instruments.md` §1](../instruments.md)
carve-out (instruments vs engine substrate). It is fronted by the
[`/reindex`](../commands/reindex.md) command; the substrate code itself is not
registry-listed.

## What ships now (the deterministic shell)

- `embedding.py`: the provider-agnostic interface plus `StubEmbedder` (deterministic,
  dependency-free, for cold runs and tests), `LocalAdapter` (on-device, with a pinned id and
  a checksum on pull, its encode path wired up when you instantiate your brain), and
  `ApiAdapter` (opt-in, key supplied via `.env`).
- `store.py`: the vector store as an eventually-consistent **derived cache of canon**
  (canon always wins). It holds per-page shards keyed by page-id and content-hash, with an
  atomic single-writer rebuild (the `session-reconcile` temp-then-rename precedent).
- `retrieval.py`: incremental indexing and a **re-rank-only** read surface (it re-orders the
  graph walk's candidates and adds none). A content-hash **staleness guard** demotes a stale
  vector to graph order rather than trusting it, and the duplicate and edge finders produce
  **candidates** only: they are never auto-applied, and they require a calibrated threshold.
- `__main__.py`: `python -m substrate index|search|dedup <vault> ...` (defaults to the
  stub adapter, so it runs cold).

## What is deferred to when you instantiate your brain

A few things wait until you instantiate your brain: threshold calibration (the
relevance and duplicate cosine cut, tuned against real content), the real model selection
and pull, ranking-quality and dedup-precision evaluation, and **turning re-ranking on in the
kernel's read-routing**. Until then the shell is exercised with the stub. See
[`MODEL-RETRIEVAL.md §6`](../../../MODEL-RETRIEVAL.md).

## Data boundary

The store, the embeddings, and the pulled model are **derived live content and runtime
state**: instance-only, gitignored, **never committed** ([`MODEL-RETRIEVAL.md §5`](../../../MODEL-RETRIEVAL.md)).
The store materialises at runtime under `.claude/substrate/store/` in the live vault; the
engine ships the code and this README, not a store. Run cold from `vault-template/.claude/`
(so the package imports) against the shipped synthetic corpus:

```
python3 -m substrate index tests/fixtures/model-retrieval --adapter stub --store /tmp/pulse-store
```
