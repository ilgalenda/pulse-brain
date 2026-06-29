# Pulse_Brain — Operations Kernel

The kernel is the brain's runtime: the layer everything plugs into. This document is the **authority for how the brain runs** — how knowledge comes in, gets compiled, is stored, found, and remembered. It is **instruction** the brain follows; Claude Code is the execution engine. Structure is in [`TAXONOMY.md`](TAXONOMY.md); the layered OS is in [`BRAIN-OS.md`](BRAIN-OS.md).

## The defining idea — compile, don't retrieve

Pulse is **not** query-time retrieval over raw notes. The LLM maintains a **persistent wiki** that sits between {{OWNER}} and raw sources. When a source arrives, the LLM reads it, extracts what matters, and **integrates it into the wiki** — updating pages, revising summaries, flagging contradictions, strengthening or challenging the synthesis. Knowledge is **compiled once and kept current**, not re-derived per query.

> Obsidian is the IDE · the LLM is the programmer · the wiki is the codebase.

**Pillar roles:**
- **`canon/` = the living wiki** — entity pages, topic summaries, compiled synthesis. The LLM maintains it.
- **`inbox/` = {{OWNER}}'s sources** · **`dynamic/` = agents' sources** — raw inputs by origin, with provenance. Compiled *into* canon.

The brain develops by **growing and refining its node-graph** — the edges between sources, pages, entities, and pillars are where synthesis lives. This is relational learning: the **frontier model stays pluggable** (Claude now, others later); what grows and is owned is the graph.

## 1. Ingestion front-door

When {{OWNER}} provides a source on the CLI — a file, a URL, a pasted page — the kernel ingests it automatically. **No manual filing.**

1. **Acquire** — read the file, fetch the URL, or take the pasted text.
2. **Capture a source note** → `inbox/<domain>/` (provided by {{OWNER}}) or `dynamic/<domain>/` (found by an agent), using the source template: raw input reference + extracted key points + provenance.
3. **Integrate** — run the integration pipeline (§3).
4. **Report** — tell {{OWNER}} what changed in the wiki (pages created/revised, contradictions flagged).

Manual filing into a pillar is a fallback, never the requirement. The {{OWNER}}-side capture ergonomics (sub-kinds, source modalities incl. image/video, and the capture channels) are specified in [`CONTEXT-ENGINE.md`](CONTEXT-ENGINE.md) (Inbox); this section owns the runtime front-door.

## 2. Sources (`inbox` + `dynamic`)

Sources are raw inputs, kept for provenance. A source note records: what it is, where it came from, the extracted key points, and `[[links]]` to the wiki pages it feeds. `inbox` = {{OWNER}}-added; `dynamic` = agent-gathered. Sources are never the answer surface — the **wiki** is. The per-pillar capture contracts — including the agent capture contract and the `confidence` trust model for dynamic sources — are in [`CONTEXT-ENGINE.md`](CONTEXT-ENGINE.md) (Dynamic / Inbox); this section owns the runtime role.

## 3. Integration pipeline — the heart (Law 1 operationalised)

On each new source, the kernel runs:

```
read → extract → INTEGRATE into the wiki → cross-link [[…]] → re-index
```

**Integrate** means, concretely:
- **Update entity pages** the source touches.
- **Revise topic summaries** so they reflect the new information.
- **Flag contradictions** where the source conflicts with existing claims (§5).
- **Strengthen or challenge** the evolving synthesis — don't just append; reconcile.
- **Grow the graph** — create, strengthen, or prune `[[wikilinks]]`/`related` edges (§13).

The LLM maintains the wiki **freely** — routine integration and upkeep are **not gated**.

## 4. The wiki (`canon`) shape

Atomic pages — **one idea per page** — of three kinds: **entity pages**, **topic summaries**, and **synthesis pages**. Every page:
- carries the atomic-note frontmatter + `## Summary` + body (per `TAXONOMY.md`),
- **cites the sources** it was compiled from (`[[links]]` back to `inbox`/`dynamic`),
- is interlinked with related pages via `[[wikilinks]]`.

The editorial standard for these pages — what each kind is for, atomicity & page boundaries, how to revise, lifecycle, and the quality bar — is [`CONTEXT-ENGINE.md`](CONTEXT-ENGINE.md) (Canon). This section owns the runtime *shape*; that doc owns *how the page is written*.

## 5. Contradiction & review surface

The LLM maintains freely, but it must make disagreement **visible** — never silently overwrite a claim:
- **On the page** — a standard inline marker (see the contradiction-flag convention in the templates) noting the conflicting claims and their sources.
- **In core memory** — a short **"needs review"** list so flags are visible without hunting.

{{OWNER}} reviews live in Obsidian. Nothing blocks integration; the flag is the handshake. The full protocol — what counts as a *significant* revision, the callout format, and the resolution lifecycle — is in [`CONTEXT-ENGINE.md`](CONTEXT-ENGINE.md) (Canon §4).

## 6. Brain-level artifacts — `index.md` + `log.md`

Two files at the brain root give it a content axis and a time axis:
- **`index.md`** — the master **content catalog / map-of-content**: the domains, the key entry pages, and links into each pillar's `_index.md`. The orientation map, read at session start.
- **`log.md`** — the chronological **evolution log**: an append-only record of every meaningful change (source ingested, page created/revised, contradiction flagged/resolved). The brain's changelog, and the raw material the Self-Development layer reviews.

Both are maintained by the kernel as part of every write (§8).

## 7. Read routing — read the compiled wiki, graph-first

Because the wiki is already compiled, reading means **reading the synthesis**, not re-deriving it.

1. Read **core memory** (anchors: current focus, active preset) + **`index.md`** (orientation).
2. Read `canon/_index.md` (**always**); load the **pinned wiki core** + the **active domain(s)' relevant** pages — never the whole wiki. The active domain(s) are the task's domain when it names one, else the active preset's `default_domains` ([`PERSONA-PRESETS.md`](PERSONA-PRESETS.md) — a set, biased not exclusive).
3. **Identify anchor nodes** for the task (the entities/pages it concerns).
4. **Traverse the graph** from anchors over the index `links` — **bounded depth**, **distance decay**, **hub weighting**.
5. Use **domain / tags / recency** as secondary tie-breakers; semantic similarity is added by the Model & Retrieval Substrate (S17, [`MODEL-RETRIEVAL.md`](MODEL-RETRIEVAL.md)) as a **re-rank of this candidate set** — it re-orders the pages the walk already surfaced, never adds pages the walk missed (compile-don't-retrieve, §5). Built; turned on in read-routing at S19 after threshold calibration.
6. Open **only** the selected pages; pull source notes or `log.md` only if needed.

Map wide, reads narrow. The traversal *model* this applies — anchors, bounded depth, distance decay, hub weighting — is defined in [`NODE-GRAPH.md`](NODE-GRAPH.md) §5; this section is its read-routing application.

## 8. Index — the edge-map

Each pillar has an `_index.md`: a table with columns **`title · description · path · domain · tags · links`**. The `links` column carries each note's outbound `[[wikilinks]]`/`related`, so the kernel **traverses the graph from the index** without opening files. `canon/_index.md` is the wiki's working map; `index.md` is the curated front page over the three.

**Integrity rule:** every write updates, in the same step, the relevant `_index.md` (including `links`), `index.md`, and `log.md`. The map never drifts from the territory. The edge-map is the **serialisation of the graph** whose model — node kinds, edge types, representation — is defined in [`NODE-GRAPH.md`](NODE-GRAPH.md) (§4).

## 9. Loading efficiency & output quality (first-class)

Uncontrolled loading degrades output (context dilution), not just cost. The rules:
- **canon-always-first ≠ load the whole wiki** — always the canon *index* + pinned *core* pages + *active-domain relevant* pages only.
- **Index-first** — scan the maps; open full pages only once selected.
- **Per-tier budgets/caps** — top-N for wiki pages, sources, and recall (bounded `max_*` limits).
- **Relevance threshold** — load only what clears it.
- **Progressive** — load the minimum; expand on demand.
- **Precision over recall** — when unsure, load less.

## 10. Memory — two tiers

- **Core memory** (`memory/core.md`, **always loaded**): identity / active-preset anchor, current focus, live threads, recent decisions, the **review-flags** list, last-updated. Compact by design — a hard size ceiling; overflow demotes to the timeline.
- **Timeline / recall** (`log.md`, **on demand**): the chronological evolution log is the recall store. There is **no separate journal** — `log.md` is the timeline.

NB: this recall timeline is kernel-owned operational continuity — **distinct from the dynamic knowledge pillar**.

**Concurrency (safe-by-default):** append to `log.md` freely (append-only is collision-safe); `core.md` is a **cache** of the `log.md` **ledger** — last-writer-with-care, and the kernel reconciles its derivable anchors (`active_preset`, `updated`, the review-flags list) against the log on load, the log winning on a disagreement. Curated prose in `core.md` is not log-derivable and is never machine-rebuilt. The full multi-tab protocol — the write-class taxonomy, this ledger/cache guarantee, the `sessions.md` presence note, and the `session-reconcile` reconciler — is the Development layer ([`DEVELOPMENT.md`](DEVELOPMENT.md)).

## 11. Model routing — model-pluggable (ML ground)

The kernel is **model-agnostic**. A route or agent **may declare** which model serves it; absent a declaration, the **session model** is used. Models are pluggable, orchestratable resources. This is the hook the **Model & Retrieval Substrate** (S17, [`MODEL-RETRIEVAL.md`](MODEL-RETRIEVAL.md)) realises: the `resolve-model` tool turns a route/agent's declaration into a deterministic lookup against the instance bindings, and **MCP hosting** (S18) slots in the same way. Pulse is, in effect, an LLM that grows alongside Claude — and other API models if added.

## 12. Kernel capability contract

The kernel exposes its operations as named, reusable primitives:

`ingest` · `integrate` · `load` (graph-first read) · `route`/`write` · `link` · `flag` · `update-index` · `update-log` · `update-memory` · `model-route`

**Skills, agents, commands, and tools are built against this contract** to grow the brain — Claude's coding role, and the Builder layer (S12). A capability composes these primitives rather than reinventing them; this is what "the runtime everything plugs into" means. The contract is defined here as instruction; capabilities are built on top in later sections. The **optional small determinism helpers for index integrity** noted in the instruction-vs-code map ([BRAIN-OS](BRAIN-OS.md)) are built as **Builder *tools*** (S12, [`BUILDER.md`](BUILDER.md) §3) that *compose* `update-index`/`update-log` deterministically — the kernel owns the contract; the tool is the helper that supports it.

## 13. The graph as developing intelligence

The brain's growth **is** the growth and refinement of its node-graph. The integration pipeline must actively **create, strengthen, and prune** links — not merely file notes. The connections (across sources, wiki pages, entities, pillars) are where synthesis and intelligence live.

This is the brain's analogue to model development — **relational** learning, with the frontier model pluggable. **Graph health** — connectedness, orphan pages, stale or contradictory edges — is a signal the Self-Development layer (S13) monitors and acts on. The owned graph is the moat; the model is rented. The full graph model — node kinds, the seeded-but-open edge vocabulary, traversal, health signals, and growth rules — is the authority in [`NODE-GRAPH.md`](NODE-GRAPH.md); this section is the kernel's edge-work mandate within it.
