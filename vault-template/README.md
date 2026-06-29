# vault-template

The skeleton for a Pulse brain. This is **structure only**: empty folders, `.gitkeep` markers, frontmatter templates in `_templates/`, and the index/log/memory scaffolding. It carries **no live data**.

When you instantiate the living brain (`Pulse-{{OWNER}}-Brain`), it is stamped from this skeleton and then filled with real notes, which never come back into this engine repo.

## Compile, don't retrieve: wiki over sources

- **`canon/`** is the **living wiki**: entity pages, topic summaries, compiled synthesis. The LLM maintains it freely and flags contradictions for review (no pre-write gate).
- **`inbox/`** holds {{OWNER}}'s **sources** (files, URLs, pages, thoughts).
- **`dynamic/`** holds agents' **sources** (research, monitoring).

`inbox` and `dynamic` are raw inputs, compiled *into* the `canon` wiki by the Operations Kernel. Each pillar is organised by the dual-role **domains**: `gtm`, `ai-orchestration`, `product`, `people`, `operating`, `glossary` (and `entities`, a canon-only wiki page type).

## Scaffolding

- **`index.md`** is the brain's master content catalogue (map-of-content), read at session start.
- **`log.md`** is the chronological evolution log (append-only), and also the recall timeline.
- **`memory/core.md`** is the always-loaded snapshot ("where am I").
- **`<pillar>/_index.md`** holds the per-pillar edge-maps (including a `links` column) the kernel traverses graph-first.

## Authority

- For structure, frontmatter contracts, and lifecycle, see **[`../TAXONOMY.md`](../TAXONOMY.md)**.
- For how the brain runs (ingest, integrate, read, remember), see **[`../OPERATIONS-KERNEL.md`](../OPERATIONS-KERNEL.md)**.
