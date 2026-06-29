# Pulse_Brain — The Brain Operating System

The generic architecture of the brain's operating system: the layers it is made of, the laws every layer obeys, and how the Operations Kernel coordinates them. This document is **architectural and generic** — it names and frames each layer; each is then fully developed in its own section. Structure lives in [`TAXONOMY.md`](TAXONOMY.md); roles live in [`.claude/CLAUDE.md`](.claude/CLAUDE.md).

The brain is **not a filing cabinet**. It is a layered, living system that rewrites and evolves itself with every input.

## The ten layers

```
        ┌──────────────  Interface (UX · open design)  ──────────────┐
        │            Persona / Presets  (GTM Lead · AI Orchestrator)  │
   ┌────┴────────────────────────────────────────────────────────────┴────┐
   │  Self-Development & Growth  —  the platform evolves itself (meta-loop) │
   ├───────────────────────────────────────────────────────────────────────┤
   │  Active:   Thinking  ·  Research & Background Agents  ·  Builder        │
   ├───────────────────────────────────────────────────────────────────────┤
   │  Context Engine — canon (the wiki)  ◀─compile─  inbox / dynamic (sources)│
   ├───────────────────────────────────────────────────────────────────────┤
   │  Operations Kernel — ingest · integrate · graph-load · route · index ·  │
   │  log · memory   (+ Development: multi-tab / concurrent-session operation)│
   ├───────────────────────────────────────────────────────────────────────┤
   │  Model & Retrieval Substrate — the models the brain runs on + semantic  │
   │  retrieval (the ML engine room; pluggable, MCP-hostable)                │
   └───────────────────────────────────────────────────────────────────────┘
```

### 1. Operations Kernel — the wiki engine
The core runtime everything plugs into, defined in [`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md). It **compiles, it doesn't retrieve**: it ingests sources, **integrates them into the wiki**, serves context by reading the compiled wiki (graph-first), and owns the index, the `log.md` timeline, and memory. It exposes a **capability contract** (`ingest`, `integrate`, `load`, `route`, `link`, `flag`, `update-index/log/memory`, `model-route`) that skills, agents, and commands are built against. *Built in S5.*

### 2. Context Engine
The knowledge substrate. **`canon/` is the living wiki** (entity pages, topic summaries, compiled synthesis); **`inbox/` and `dynamic/` are the raw sources** ({{OWNER}}'s and agents') compiled into it. It serves context **index-first, canon-always-first** — but canon-first means the wiki *index* + pinned *core* + relevant pages, never the whole wiki. The editorial standard for the substrate — how pages are written and maintained — is in [`CONTEXT-ENGINE.md`](CONTEXT-ENGINE.md). *Pillars built in S6–S8 — Canon, Dynamic, and Inbox all done; layer complete.*

### 3. Thinking
Reasoning and synthesis over loaded context, defined in [`THINKING.md`](THINKING.md): connecting ideas across notes, proposing new `[[wikilinks]]`, proposing promotions into canon, and generating insight that did not exist in any single note. The brain's first **active** layer — it *reasons over* the graph rather than maintaining it — and the home of Law 3 (the intelligence partner). Un-sourced reasoning carries an `[!inference]` marker so a guess never reads as fact. *Built in S10.*

### 4. Research & Background Agents
Autonomous workers that run continuously — researching, monitoring, and gathering — and feed new knowledge into the Context Engine so {{OWNER}} stays current without asking, defined in [`RESEARCH-AGENTS.md`](RESEARCH-AGENTS.md). The brain's first **code** layer: realised as Claude Code operating artifacts (agents · skills · commands) on native scheduling, not a bespoke daemon. It also **drains the `[!inference]` queue** to close S10's self-correction loop. *Built in S11.*

### 5. Builder
Reactive self-extension, defined in [`BUILDER.md`](BUILDER.md). When a task needs a capability that does not exist, the brain creates a new instrument — **skill, agent, command, or tool** (the one code kind, a deterministic helper script) — to solve *that* problem, built to the engine's standards via one build lifecycle, registered, and audited for reuse. Two callers, one gate: an {{OWNER}} `/build` request and the brain's own reactive gap-detection both pass through the dual-role build gate. *Built in S12.*

### 6. Self-Development & Growth
The meta-loop that grows the **platform itself**, defined in [`SELF-DEVELOPMENT.md`](SELF-DEVELOPMENT.md). It audits the brain for gaps and weaknesses — graph health (Node-Graph §6), ontology promotions (§3.3), recurring capability gaps — and *drives* Builder, Research, and Thinking to mend them: the judgement that points the hands, never the hands. A three-tier autonomy gate keeps it honest — changes to shared meaning (the ontology, the architecture) are proposed build-complete and ratified, never silently applied. Distinct from the living-vault law below: that is *content* evolving; this is the *system* evolving. *Built in S13.*

### 7. Persona / Presets
Selectable operating presets for {{OWNER}}'s roles — GTM Lead, AI Orchestrator, and others, defined in [`PERSONA-PRESETS.md`](PERSONA-PRESETS.md). A preset is a **lens, not a store**: it shapes focus, default domains, tone, and which agents and skills lead, and switching it reconfigures how the whole stack behaves **without changing the knowledge beneath it**. Two boundaries hold it in place — *lens-not-filter* (default domains lead read-routing, they never blind the brain to what a task needs) and *one voice* (a scoped operating role beneath the director, never a second identity). Config tier; switching sets the `active_preset` anchor the kernel already reads. *Built in S14.*

### 8. Development
How the brain is operated and evolved across **multiple concurrent CLI tabs**, defined in [`DEVELOPMENT.md`](DEVELOPMENT.md): coordinating sessions so they do not collide on the shared vault — concurrency made safe by construction and self-healing, not locked — and the workflow for developing the brain itself. A write-class taxonomy, the `log.md`-is-ledger / `core.md`-is-cache guarantee, an append-only session-presence note, and one deterministic `session-reconcile` tool that heals rather than prevents. *Built in S15.*

### 9. Interface
The UX layer — how {{OWNER}} interacts with the brain day to day, defined in [`INTERFACE.md`](INTERFACE.md): the surfaces through which {{OWNER}} enters, feeds, and reviews the brain (boot/entry, channel-agnostic capture, Obsidian review). Built **lean and design-first** — the surfaces are designed in full, and the ones honest to build against the local vault are realised now (the `/pulse` boot/entry command), while the experiential parts mature with the live vault (S19). *Built in S16 (boot/entry shipped; capture + review realise progressively).*

### 10. Model & Retrieval Substrate — the ML engine room
The foundation beneath the kernel: the **models the brain runs on** and the **semantic retrieval** over the wiki. The kernel is model-pluggable (a route/agent may declare its model; default = session model), so this substrate can grow into **multi-model orchestration** (different models bound to different routes/agents, in harmony) and **embedding-based retrieval**, and be **hosted as an external MCP server**. This is what "build Pulse as an ML" means — not a bespoke trained model, but an **LLM + RAG, multi-model** system whose owned, compounding **node-graph is the moat** while the frontier model stays rented. Retrieval here is **re-ranking, not retrieval-instead-of-compile**: it re-orders the graph walk's candidates and never displaces the wiki as the answer surface ([`MODEL-RETRIEVAL.md`](MODEL-RETRIEVAL.md) §1). *Built in S17 — the deterministic shell (the `model-route` resolver + the embedding/store substrate); threshold calibration, the real model pull, and read-routing integration land at S19. MCP hosting is S18.*

## How the brain develops — the graph is the intelligence

Pulse grows chiefly by **growing and refining its node-graph**: the edges (`[[wikilinks]]`/`related`) between sources, wiki pages, entities, and pillars are where synthesis lives. This is the brain's analogue to model development — **relational** learning, with the frontier model pluggable. The integration pipeline's real job is to create, strengthen, and prune links; **graph health** is a signal the Self-Development layer acts on. The node/edge model itself — node kinds, edge types & semantics, traversal, health, and growth — is the authority in [`NODE-GRAPH.md`](NODE-GRAPH.md).

## Instruction vs code — what each layer is

The brain is **instruction-first** (markdown the LLM follows; Claude Code is the runtime). Code enters only where a layer genuinely needs a running process, a UI, or hard determinism.

| Layer | Instruction or code |
|---|---|
| Operations Kernel | **Instruction** (+ optional small determinism helpers for index integrity — built as Builder *tools*, S12) |
| Context Engine (wiki + sources) | **Instruction** (markdown files) |
| Thinking | **Instruction** |
| Research & Background Agents | **Code** — needs scheduling/autonomy |
| Builder | **Instruction** that *produces* skills/agents/commands (which may be code) |
| Self-Development & Growth | **Instruction** (may produce code via Builder) |
| Persona / Presets | **Instruction** (config) |
| Development (multi-tab) | **Instruction** (+ light tooling if needed) |
| Interface | **Code** — a UX surface |
| Model & Retrieval Substrate | **Code** — the `substrate/` category (engine code beneath the kernel: models, embeddings, vector store, MCP host); distinct from Builder *tools*, which are deterministic and network/credential-free |

## Three cross-cutting laws

These bind every layer.

### Law 1 — The vault is alive
Every input triggers the **evolution loop**, owned by the kernel:

```
input → route → link → synthesise → (maybe) research → re-index
```

The brain never sits still. A new note is routed to a pillar, linked to related notes, considered for synthesis or promotion, may spawn background research, and the index is updated — all as part of taking the input in. Knowledge compounds rather than accumulating dead.

### Law 2 — Atomic notes
One idea, one file. Every note follows the same shape so the brain stays legible and linkable:

```
---
# frontmatter — pillar-specific fields, always including: title, description,
# tags, author (contributed_by / added_by / source), related (links), id
---

## Summary
One short paragraph — the idea in brief.

## <body>
The full text.
```

Notes cross-reference with `[[wikilinks]]` so the whole brain renders as one connected graph. Templates for each pillar/type live in [`vault-template/_templates/`](vault-template/_templates/).

### Law 3 — The brain is an intelligence partner
The brain does not only store and serve knowledge — it **thinks with {{OWNER}}**. This expands its scope: from a knowledge system that powers Claude, to a partner that helps {{OWNER}} think and decide. It is:

- **Proactive** — anticipates needs, surfaces connections across the graph, and brings in outside intelligence before being asked.
- **Honest** — challenges and pressure-tests rather than merely agreeing; an advisor, not a yes-man.
- **With, not for** — it reasons alongside {{OWNER}}, advising rather than only answering.

This stance is expressed mainly through the **Thinking** layer (synthesis, challenge, advice) and the **Research & Background Agents** layer (proactive outside intelligence), but it colours every interaction across all layers.

## Kernel coordination model

Detailed in [`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md); the shape:

- **Ingest:** a source ({{OWNER}}'s file/URL/page → `inbox/`, agent's find → `dynamic/`) is captured with provenance — no manual filing.
- **Integrate (compile, don't retrieve):** the LLM reads the source and compiles it **into the wiki** — updates pages, revises summaries, flags contradictions, grows the graph. The wiki is **maintained freely**; routine integration is **not gated**.
- **Surface, don't gate:** contradictions and significant revisions are **flagged** on the page and in core memory for {{OWNER}}'s review — nothing blocks integration. (This replaces the earlier confirmation-gate model.)
- **Load (read):** read the compiled wiki, **graph-first** — index-first, canon-always-first (wiki index + pinned core + relevant pages, *not* the whole wiki), traverse the graph from anchors, open notes narrowly. No per-query re-synthesis.
- **Index/log maintenance:** every write updates the relevant `_index.md`, `index.md`, and `log.md` in the same step, so the maps never drift.
