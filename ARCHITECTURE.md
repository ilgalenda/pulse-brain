# Pulse_Brain: Architecture

This document defines how Pulse_Brain is designed. It is the single source of truth for the system's shape, and it is kept current as the brain grows.

## 1. Engine vs instance

Pulse_Brain exists in two tiers with a hard boundary between them.

- **Engine (`Pulse_Brain`, this repo).** Architecture only: directory structure, operating rules, frontmatter templates, skill and agent definitions, documentation. It is sanitised by design and safe to version in git. It is the reusable model from which any number of instances can be created.
- **Instance (`Pulse-{{OWNER}}-Brain`).** A live Obsidian vault on the machine, instantiated from the engine, holding real {{COMPANY}} knowledge. Private, local, never committed.

**The data boundary is absolute.** Live data, secrets, client names, financial figures, and PII never enter the engine repo. The engine ships *templates and structure*; the instance holds *content*. This boundary is enforced by `.gitignore` and by the security protocol in `.claude/CLAUDE.md`.

**Roles.** Within the project, work runs on a **dual-role model** governed by the project director (`.claude/CLAUDE.md`). **Pulse** is the brain (memory, knowledge, identity, curation, growth) and **Claude** is the mind (reasoning, execution, agent orchestration). The full definition and the collaboration seam live in `.claude/CLAUDE.md`, the authority for roles.

## 2. Knowledge model: a compiled wiki over raw sources

**Compile, don't retrieve.** `canon/` is a **living wiki** the LLM maintains; `inbox/` and `dynamic/` are the raw **sources** compiled into it. Knowledge is compiled once and kept current, not re-derived per query.

- **`canon/`, the living wiki.** Entity pages, topic summaries, the compiled synthesis. The LLM **maintains it freely** and **flags** contradictions and major revisions for review. There is **no pre-write confirmation gate**.
- **`inbox/`, {{OWNER}}'s sources.** Files, URLs, pages, and thoughts {{OWNER}} adds.
- **`dynamic/`, agents' sources.** What research and monitoring agents gather.

`inbox/` and `dynamic/` are raw inputs by origin, kept for provenance; `canon/` is the synthesis they feed. Each pillar is organised by the dual-role **domains** (`gtm`, `ai-orchestration`, `product`, `people`, `operating`, `glossary`), plus `entities`, a canon-only wiki page type.

**Frontmatter contract.** Every entry carries at least a `title` and a one-sentence `description`. `[[wikilinks]]` cross pillar boundaries freely so the whole brain renders as one connected graph in Obsidian. The skeleton lives in [`vault-template/`](vault-template/); the full taxonomy, per-pillar frontmatter contracts, and lifecycle are specified in [`TAXONOMY.md`](TAXONOMY.md). The pillars are the **Context Engine** layer of the operating system (below).

## 3. The Brain Operating System

The brain is a **layered, living system**, not a filing cabinet. Its operating system is in [`BRAIN-OS.md`](BRAIN-OS.md): **ten layers** (Operations Kernel · Context Engine · Thinking · Research & Background Agents · Builder · Self-Development & Growth · Persona/Presets · Development · Interface · **Model & Retrieval Substrate**) over **three laws**. The laws are *living vault* (every input runs the integration pipeline: ingest, integrate into the wiki, link, then re-index), *atomic notes* (one idea per file; frontmatter, summary, body; `[[wikilinks]]`), and *intelligence partner* (it thinks *with* {{OWNER}}, being proactive, honest, and advising). Its runtime is the **Operations Kernel** ([`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md)), which exposes a **capability contract** that skills, agents, and commands are built against. The **Context Engine** layer is the knowledge substrate (`canon/` compiled from `inbox/` and `dynamic/`) and the editorial standard for it, specified in [`CONTEXT-ENGINE.md`](CONTEXT-ENGINE.md). The **node/edge model** the whole brain runs on (what its nodes and edges are, how they are traversed, judged, and grown) is the authority in [`NODE-GRAPH.md`](NODE-GRAPH.md).

The brain **develops by growing its node-graph**: relational learning, with the frontier model pluggable (Claude now, others later), and the owned graph is the moat. Self-growth is two layers: **Builder** (a capability for a present problem) and **Self-Development & Growth** (the meta-loop evolving the platform). The brain is **instruction-first**; code enters only where a layer needs a process, a UI, or hard determinism (see the instruction-vs-code map in `BRAIN-OS.md`).

## 4. Cross-surface access

Pulse_Brain is operated **exclusively through Claude Code on the CLI and desktop app, primarily the CLI.** The intended working pattern is **multiple concurrent sessions**: several tabs open at once, each running one or more agents that work on {{OWNER}}'s behalf against the same shared local brain. There is no dependency on the web (claude.ai) surface or any external connector.

## 5. How the system is organised

The brain is built as ten layers over the knowledge model of section 2. They divide into the parts that *hold and maintain* knowledge, the parts that *reason and act* over it, and the parts that *grow, present, and run* the whole thing. Each layer has its own authority document; this section explains what each one does and how they fit together.

**The foundation: identity and the data boundary.** Beneath everything sits the engine repo, the operating identity, and the security boundary. The dual-role model (Pulse the brain, Claude the mind) and the engine/instance split described above are the ground every layer stands on.

**The Operations Kernel: the wiki engine.** The kernel is the runtime. It puts compile-don't-retrieve into practice: an ingestion front door, the integration pipeline that turns a source into wiki content, the graph-first read that loads only what a task needs, the edge-map index, the `index.md` content catalogue and `log.md` evolution timeline, the two-tier memory, and the **capability contract** (`ingest`, `integrate`, `load`, `route`, `link`, `flag`, `update-*`, `model-route`) that every skill, agent, and command is built against. Model choice is pluggable. The authority is [`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md).

**The Context Engine: the knowledge itself.** This is the three-pillar knowledge substrate and the editorial standard for it. `canon/` is the living wiki: its page kinds, its rule of one idea per file, its maintain-freely revision, and the flag-don't-gate contradiction protocol with a resolution lifecycle. `dynamic/` is the agent-gathered source pillar, carrying a structured `confidence` (high, medium, or low) trust model for open-world reliability. `inbox/` is {{OWNER}}'s own source pillar, covering primary thoughts and decisions as well as curated external material, multimodal sources including image and video, and frictionless capture on the CLI. The authority is [`CONTEXT-ENGINE.md`](CONTEXT-ENGINE.md), with the taxonomy and frontmatter contracts in [`TAXONOMY.md`](TAXONOMY.md).

**The Node-Graph: how knowledge connects.** This is the node and edge model the whole brain runs on, consolidated into one authority. It defines the node kinds, the structural edges (`feeds`, `sources`, `related`, `[[wikilink]]`), and a seeded-but-open semantic-edge model (`supersedes`, `contradicts`, `corroborates`, with a promotion rule so the ontology grows with the brain). It also defines traversal, graph-health signals, and growth rules. The authority is [`NODE-GRAPH.md`](NODE-GRAPH.md).

**The Thinking layer: reasoning over the graph.** The first layer that is *active* rather than custodial. It reasons over the graph rather than maintaining it, through synthesis pages, link proposals, contradiction-resolution proposals, content-promotion candidates, and the challenge-and-advise duty of the intelligence-partner law. It is anchored by inference-marking discipline: the `[!inference]` callout (so unverified claims are always marked, with `confidence` and `[!contradiction]`), confidence-aware auto-resolution, a self-correction loop, and a `log.md` audit stamp for autonomous confirmations. The authority is [`THINKING.md`](THINKING.md).

**The Research & Background Agents layer: gathering from the open world.** The first layer with real code, built from Claude Code operating artefacts rather than a bespoke daemon. It runs two worker kinds (research, which pulls on demand, and monitor, which runs on a cadence), the gather lifecycle, the inference-queue drain that closes the Thinking loop, and the scheduling model. The authority is [`RESEARCH-AGENTS.md`](RESEARCH-AGENTS.md), with the machinery (skills, agents, commands, tests, the `instruments.md` registry, and a scheduling template) in `vault-template/.claude/`.

**The Builder layer: building a capability on demand.** Reactive self-extension. When a task needs a capability that does not exist, the brain builds one instrument to solve it, against the kernel contract, registered and audited. It defines one build lifecycle over four instrument kinds (skill, agent, command, and **tool**, the one code kind, a deterministic helper script), a unified `/build` entry, the reactive gap-detection trigger, a dual-role build gate (Claude detects, Pulse decides and records), and a Test-Driven acceptance bar. The authority is [`BUILDER.md`](BUILDER.md).

**The Self-Development & Growth layer: growing the platform itself.** The meta-loop. It audits the brain's own condition and *drives* the Builder, Research, and Thinking layers to mend it; it is the judgement that points the hands, never the hands themselves. One bounded loop (audit, triage, route, drive, record) runs over the graph-health signals from [`NODE-GRAPH.md`](NODE-GRAPH.md) §6, each routed to the layer that owns the fix, plus the two growth decisions this layer owns: ontology promotion and systemic capability gaps. A three-tier autonomy gate keeps it safe: computing and routing is free, driving the Builder inherits build-then-record, and changes to shared meaning (the ontology or the architecture) follow propose-build-complete then ratify, so the brain never silently rewrites its own engine. The authority is [`SELF-DEVELOPMENT.md`](SELF-DEVELOPMENT.md).

**The Persona / Presets layer: a lens for each role.** Selectable operating presets for {{OWNER}}'s roles. A preset is a lens, not a store: it biases focus, default domains, tone, and which instruments lead for one role (such as GTM Lead or AI Orchestrator) without changing the knowledge, the identity, or the laws beneath it. Two boundaries hold it in place: lens-not-filter (default domains *lead* read-routing but never suppress a domain the task needs or hide a `core.md` flag) and one voice (a preset is a scoped operating role beneath the director; `tone` is register and emphasis, never a second identity). The authority is [`PERSONA-PRESETS.md`](PERSONA-PRESETS.md), shipping the preset contract, two exemplar presets, and the `/preset` command.

**The Development layer: many tabs, one brain.** Concurrent-session operation over one shared local vault, plus the workflow for developing the brain itself. It uses local-filesystem coordination rather than distributed consensus, making concurrency safe by construction and self-healing rather than prevented by locking. A write-class taxonomy (append-only and new-file writes are collision-free; `core.md` is a reconcilable cache; co-edited shared meaning is kept rare by lane discipline and a session note) sits alongside the ledger guarantee: `log.md` is the append-only truth and `core.md` a cache the kernel rebuilds from it, so a clobber is always recoverable. It ships a `sessions.md` presence note and a deterministic `session-reconcile` tool that heals rather than prevents. The authority is [`DEVELOPMENT.md`](DEVELOPMENT.md).

**The Interface layer: how {{OWNER}} enters, feeds, and reviews.** The UX surfaces, built lean and design-first. The `/pulse` command wakes the brain: it paints a banner, runs read-routing, greets {{OWNER}}, and reports the active preset, focus, review state, and last activity. It is summoned deliberately, not auto-booted. Capture is channel-agnostic with no bespoke app: the CLI, a remote-control surface for the phone while the Mac is awake (local-only, so it does not cross the data boundary), and a synced drop-folder for asynchronous capture (the sync provider is the always-on intermediary, needing no app and no backend). The authority is [`INTERFACE.md`](INTERFACE.md).

**The Model & Retrieval Substrate: the engine room.** The machine-learning layer beneath the kernel. It realises two kernel hooks: `model-route` (the deterministic `resolve-model` tool, an instance bindings template, and the tiered-worker policy with its cache-the-prefix cost rationale) and a semantic tie-breaker (an embedding substrate that *re-ranks* the graph walk's candidates and never retrieves graph-distant pages, so compile-don't-retrieve holds). It introduces the `substrate/` code category for engine code beneath the kernel, which uses the network and credentials and so is kept distinct from a Builder tool. The authority is [`MODEL-RETRIEVAL.md`](MODEL-RETRIEVAL.md).

**Distribution and sharing.** Two further pieces sit around the layers. The instantiation kit turns a clone of the engine into a working private brain through `/setup`: a `setup` skill interviews the owner (identity, owner-defined domains, presets, writing voice, embedding choice) and drives the deterministic `instantiate` tool, which stamps a live instance *outside* the engine, refusing any target inside it, so the data boundary is safe by construction. The procedure is in [`SETUP.md`](SETUP.md). Going public ships a newcomer-facing README and the MIT licence (see [`LICENSE`](LICENSE)); the engine is published from a fresh clean-history snapshot, so no real-name or email history travels, while the full-history private repo is retained as a backup.

**A note on maturity.** Most of the engine is built and working: the knowledge model, the kernel, the full Context Engine, the Node-Graph, and the Thinking, Research, Builder, Self-Development, Persona, and Development layers are all in place, along with the instantiation kit. The Interface layer has its boot and entry path working, with the experiential review surfaces maturing once you instantiate your own brain. The Model & Retrieval Substrate ships as a deterministic shell; threshold calibration, the real model pull, and turning re-ranking on in read-routing are deferred to when you instantiate your brain. Exposing Pulse as an external MCP server, and the sync backend that a hosted capture endpoint would need, are planned and not yet built.

## 6. Conventions

- **Language:** British English.
- **Markdown + frontmatter:** all knowledge is plain markdown with YAML frontmatter, Obsidian-compatible.
- **Linking:** `[[wikilinks]]` for cross-references.
- **Security:** see `.claude/CLAUDE.md`; the engine/instance data boundary is a hard rule.
- **Placeholders:** the engine is generic and names no real person or company. Two placeholders stand in for instance-specific identity and are filled when the living vault is instantiated:
  - `{{OWNER}}` is the brain's owner.
  - `{{COMPANY}}` is the owner's organisation.
  - The owner's instance follows the pattern `Pulse-{{OWNER}}-Brain`. Auditing the engine for leaks is therefore a grep for real names returning nothing, and a grep for `{{` returning only intended template markers.
