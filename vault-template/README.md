# vault-template

The skeleton for a Pulse brain. This is **structure only** — empty folders, `.gitkeep` markers, frontmatter templates in `_templates/`, and the index/log/memory scaffolding. It carries **no live data**.

When the living instance (`Pulse-{{OWNER}}-Brain`) is created (S19), it is stamped from this skeleton and then filled with real notes — which never come back into this engine repo.

## Compile, don't retrieve — wiki over sources

- **`canon/`** — the **living wiki**: entity pages, topic summaries, compiled synthesis. The LLM maintains it freely and flags contradictions for review (no pre-write gate).
- **`inbox/`** — {{OWNER}}'s **sources** (files, URLs, pages, thoughts).
- **`dynamic/`** — agents' **sources** (research, monitoring).

`inbox` + `dynamic` are raw inputs, compiled *into* the `canon` wiki by the Operations Kernel. Each pillar is organised by the dual-role **domains**: `gtm`, `ai-orchestration`, `product`, `people`, `operating`, `glossary` (and `entities`, a canon-only wiki page type).

## Scaffolding

- **`index.md`** — the brain's master content catalog (map-of-content), read at session start.
- **`log.md`** — the chronological evolution log (append-only); also the recall timeline.
- **`memory/core.md`** — the always-loaded snapshot ("where am I").
- **`<pillar>/_index.md`** — per-pillar edge-maps (incl. a `links` column) the kernel traverses graph-first.

## Authority

- Structure, frontmatter contracts, lifecycle — **[`../TAXONOMY.md`](../TAXONOMY.md)**.
- How the brain runs (ingest, integrate, read, remember) — **[`../OPERATIONS-KERNEL.md`](../OPERATIONS-KERNEL.md)**.
