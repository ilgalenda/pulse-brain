# Pulse_Brain: Taxonomy

The authoritative specification for how knowledge is organised, shaped, and moved through a Pulse brain. The skeleton that implements it lives in [`vault-template/`](vault-template/). The runtime that operates it (ingest, integrate, read, remember) is the Operations Kernel ([`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md)).

## Pillars: wiki vs sources

A Pulse brain has three pillars. **`canon/` is the living wiki**; `inbox/` and `dynamic/` are the **raw sources** that are compiled into it (the *compile-don't-retrieve* model, described in [`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md)).

| Pillar | Role | Behaviour |
|---|---|---|
| **`canon/`** | The **living wiki**: entity pages, topic summaries, compiled synthesis | The LLM **maintains it freely**. Not gated; contradictions are **flagged on the page**, not silently overwritten. |
| **`inbox/`** | {{OWNER}}'s **sources** (files, URLs, pages, thoughts) | Captured freely, kept for provenance, compiled into the wiki. |
| **`dynamic/`** | Agents' **sources** (research, monitoring) | Gathered freely, kept for provenance, compiled into the wiki. |

`inbox/` and `dynamic/` are raw inputs split by origin; `canon/` is the compiled synthesis they feed. There is **no review queue and no pre-write confirmation gate**, because this is a single-owner brain. The LLM maintains the wiki autonomously and **surfaces contradictions and significant revisions** for {{OWNER}} to review live in Obsidian (flagged on the page and listed in core memory).

## Domains

Each pillar is organised by **domains**, the top-level areas of {{OWNER}}'s work. **Domains are owner-defined**: chosen at instantiation (`/setup`), scaffolded by the `instantiate` tool, and freely changed later. The set below is the shipped **example**, modelled on one owner's dual role (GTM lead and AI orchestrator); a new instance replaces it with its own:

| Domain | Holds |
|---|---|
| `gtm` | Accounts, ICP, playbooks, messaging, competitors, pipeline thinking |
| `ai-orchestration` | Agent and system designs, prompts, build logs, orchestration patterns |
| `product` | {{COMPANY}} products, technology, positioning |
| `people` | Contacts, team, network, relationships |
| `operating` | {{OWNER}}'s preferences, decisions, routines, objectives |
| `glossary` | Short reusable definitions referenced across the brain |
| `entities` | Canonical definitions of recurring things (**canon-only**) |

`entities/` exists only under `canon/`, because entity pages are part of the wiki, not raw sources. The other six domains mirror across all three pillars.

## Frontmatter contracts

**Universal rule: every entry carries a `title` and a one-sentence `description`.** Beyond that, the contract is set by pillar/type. Templates live in [`vault-template/_templates/`](vault-template/_templates/).

Wiki pages (`canon/`):
- **canon-note** (topic/synthesis page): `title, description, domain, tier: canon, page_type, tags, aliases, related, sources, id, created, updated`
- **entity** (entity page): `title, description, type: entity, entity_type, aliases, tags, related, sources, id, created, updated`
- **glossary-term**: `title, description, tier, aliases, tags, related, sources, first_seen_in, id, created, updated`

Source notes (`inbox/`, `dynamic/`):
- **inbox-note**: `title, description, domain, type: source, source_type, source, added_by, tags, feeds, related, id, created`
- **dynamic-note**: `title, description, domain, type: source, source_type, source, contributed_by, confidence, tags, feeds, related, id, created`

`confidence` (`high | medium | low`) is **dynamic-only**. Agent-gathered sources come from the open world, so their reliability is recorded and weighted on integration (see `CONTEXT-ENGINE.md`, Dynamic §2). Inbox sources are {{OWNER}}'s own and implicitly trusted, so they carry no `confidence` field.

Every note also follows the **atomic-note body**: `## Summary` then the body; wiki pages cite their `sources`, source notes link the wiki pages they `feeds`.

## Conventions

- **Filenames:** kebab-case; entities and glossary terms named for the thing they define (e.g. `clock-drift.md`).
- **`id`:** a stable kebab-case slug, set once and not changed. It is the durable handle for cross-references.
- **Linking:** `[[wikilinks]]` cross pillars and domains freely, so the brain renders as one connected graph in Obsidian. Point at canonical entities and glossary terms by their `title`.
- **Markdown + YAML frontmatter** throughout; Obsidian-compatible.

## Lifecycle: ingest then integrate

*Defined here; operated by the kernel ([`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md)).*

1. **Ingest.** A source arrives (a file/URL/page from {{OWNER}}, or an agent's find) and is captured into `inbox/` or `dynamic/` with provenance.
2. **Integrate.** The LLM compiles the source **into the wiki** (`canon/`): updates entity pages, revises topic summaries, flags contradictions, strengthens or challenges the synthesis.
3. **Connect.** It grows the graph, creating, strengthening, or pruning `[[wikilinks]]`/`related` edges across pages and pillars. The graph is where synthesis lives.
4. **Surface.** Contradictions and significant revisions are flagged on the page and listed in core memory for {{OWNER}}'s review. The wiki is maintained freely; nothing blocks integration.
