# Pulse_Brain — Node-Graph

The brain's **graph model**: what its nodes and edges are, how they are traversed, how their health is judged, and how they grow. This document is the **single authority for the node/edge model**; the layers that read, grow, or audit the graph (the [Operations Kernel](OPERATIONS-KERNEL.md), the [Context Engine](CONTEXT-ENGINE.md), Thinking, Self-Development) **apply** this model and cite it rather than redefining it.

It is an **instruction** layer (Brain-OS instruction-vs-code map: this is the graph *model* the LLM follows). The *code substrate* that runs the graph at scale — embeddings, semantic edges, automated traversal and metrics, vector retrieval — is the **Model & Retrieval Substrate (S17)**. S9 defines what the graph **is**; S17 builds the machinery (§9).

## 1. The graph is the intelligence

Pulse does not develop by swapping in a bigger model. It develops by **growing and refining its node-graph** — the edges between sources, wiki pages, entities, and terms are where synthesis lives. This is **relational learning**: the frontier model stays **pluggable** (Claude now, others later), while the **owned graph is the moat**. Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase — and the graph is the program's structure.

Two consequences govern everything below:
- **A note is only as valuable as its edges.** An unconnected fact is dead weight; a well-connected one compounds.
- **Growth is edge-work, not file-work.** Integration's real job is to create, strengthen, and prune edges (§7) — filing a note without connecting it is incomplete.

## 2. Nodes

A **node** is one **atomic markdown file** — one idea, one file (Brain-OS Law 2) — identified by its stable `id` (set once, never changed; the durable handle for cross-references, per [`TAXONOMY.md`](TAXONOMY.md)). The node kinds:

| Node kind | Pillar | Defined in |
|---|---|---|
| **Entity page** | `canon/entities/` | Context Engine, Canon §1 |
| **Topic summary** | `canon/` | Canon §1 |
| **Synthesis page** | `canon/` | Canon §1 |
| **Glossary term** | `canon/glossary/` | Canon §1 |
| **Source note** (inbox · dynamic) | `inbox/` · `dynamic/` | Context Engine, Dynamic / Inbox |

**Not nodes — infrastructure.** The brain artifacts — `index.md`, `log.md`, `memory/core.md`, and the per-pillar `_index.md` edge-maps — are *about* the graph; they are not knowledge nodes in it. They orient, serialise, and remember; they are not traversed as content.

## 3. Edges — the model

Edges carry the graph's meaning. Pulse runs a **seeded-but-open** edge model: a fixed set of structural edges, a small seed of typed semantic edges the brain already performs, and a governed way for the vocabulary to grow.

### 3.1 Structural edges (always present)

| Edge | Direction | Meaning | Recorded in |
|---|---|---|---|
| `feeds` | source → page | "this source was compiled into that page" (provenance) | source-note frontmatter `feeds` |
| `sources` | page → source | "this page was compiled from that source" (citation; the inverse of `feeds`) | canon-page frontmatter `sources` |
| `related` | page ↔ page | associative — "these bear on each other" | frontmatter `related` |
| `[[wikilink]]` | note → entity/term/page | inline reference, by `title`, to a canonical thing | the note body |

`feeds` and `sources` are inverses and should agree — a page citing a source implies that source feeds the page. Keeping them consistent is part of the integrity rule (kernel §8).

### 3.2 Seeded semantic edges

Three **typed relations** the brain already performs (so they are surfaced, not invented). Each is directed and named:

| Edge | Direction | Meaning | Already performed by |
|---|---|---|---|
| `supersedes` | newer → older | the newer node replaces the older; the older is kept for provenance, not re-surfaced | page lifecycle (Canon §6); dynamic freshness (Dynamic §3) |
| `contradicts` | node ↔ node | the two make conflicting claims; unresolved until reconciled | the flag protocol (Canon §4) |
| `corroborates` | source → claim | independent support that lets a low-confidence claim harden | the confidence model (Dynamic §2) |

**Representation — no new required field.** These already have homes: `supersedes` is the supersede body-note + a `related` link to the replacement; `contradicts` is the `[!contradiction]` callout (Canon §4); `corroborates` lives in the corroborating source's extracted points and `feeds`. S9 **names** them as edge types and unifies their meaning; where an edge-map needs to show one, it is surfaced as a **tag** (e.g. `edge/contradicts`), not a new frontmatter schema field. The graph stays expressible in the existing structure. **The tag sits on the node carrying the open relation and clears when it resolves** — `edge/supersedes` on the superseded (older) node, `edge/contradicts` on a node in unresolved conflict — so an open tag in the edge-map is itself the unresolved signal (the same convention `edge/inference` follows, below). Direction in the table above is the relation's semantics, not where the tag lives.

The same tag convention carries the Thinking layer's **open inference markers**: an unresolved `[!inference]` ([`THINKING.md`](THINKING.md) §6) surfaces as an **`edge/inference`** tag, indexed by its `basis` pages, so the brain can traverse to every claim it has reasoned-but-not-proven — and to every inference depending on a given page — straight from the map. Resolving the marker clears the tag.

### 3.3 Open ontology — the promotion rule

The edge vocabulary is **open**. A rich ontology imposed up front ossifies; richness should **emerge as the brain grows**. But ungoverned emergence drifts into inconsistency (one relation expressed five ways). So new relation types are **promoted deliberately**:

1. **Provisional** — a relation is first expressed in prose / as an annotated `related` link, not yet a named type.
2. **Recurring** — the same relation shows up across several nodes.
3. **Promoted** — when it recurs and proves useful, it is **named as a typed edge here**, in this document, and may be surfaced as an `edge/<type>` tag.

Promotion is reviewed through the **graph-health / Self-Development loop (S13)**. The ontology grows with the brain — seeded small, extended on evidence.

## 4. Edge representation & the edge-map

The graph is **not a separate database**. It *is* the `[[wikilink]]` / `related` / `sources` / `feeds` structure across the notes, **serialised in the per-pillar `_index.md` edge-maps** — the `links` column carries each node's outbound edges so the graph is traversable from the map without opening files (kernel §8). The union of the three edge-maps plus the notes' frontmatter is the materialised graph. Semantic and vector edges (embedding-derived similarity) are realised by the **Model & Retrieval Substrate (S17, [`MODEL-RETRIEVAL.md`](MODEL-RETRIEVAL.md))** as **candidates** the Thinking layer proposes and {{OWNER}} ratifies (§3.3) — never auto-written; the explicit link structure remains the materialised graph.

## 5. Traversal — the read model

Reading the brain is a **bounded walk** of the graph, not a scan. This document owns the traversal *model*; the kernel **applies** it for read-routing ([`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md) §7):

- **Anchor** on the nodes the task concerns (the entities/pages it names).
- **Walk** outward over the edge-map `links` — **bounded depth**, **distance decay** (nearer nodes weigh more), **hub weighting** (highly-connected nodes are strong signals).
- **Tie-break** on domain, tags, and recency; semantic similarity is added by S17 as a **re-rank** of the surfaced candidates (never a recall path that adds graph-distant pages — [`MODEL-RETRIEVAL.md`](MODEL-RETRIEVAL.md) §1; turned on at S19).
- **Open narrowly** — select from the map first, open only the chosen nodes.

Map wide, read narrow. Precision over recall.

## 6. Graph health — the signals

The graph's condition is itself a signal. S9 **defines** these; **Self-Development (S13) monitors and acts on** them:

- **Orphans** — nodes with no inbound or outbound edges (dead weight).
- **Weak connectivity** — nodes reachable only through a single fragile edge.
- **Stale edges** — links pointing at a `supersedes`-ed (superseded) node that should be re-pointed.
- **Unresolved `contradicts`** — conflicts flagged but never reconciled.
- **Unsourced-and-unmarked claim** — a canon claim with no cited `[[source]]` *and* no `[!inference]` marker: the confabulation surface. Surfaced by the Thinking layer's grounding re-trace ([`THINKING.md`](THINKING.md) §6.2) so a guess that escaped its marker is caught on a later pass, not left to read as fact.
- **Hub overload** — a node so over-connected it has stopped being atomic (a split candidate, Canon §2).
- **Duplicate nodes** — two nodes for one idea (a merge candidate; fractures the graph).

## 7. Growth rules

The graph **compounds** when integration does edge-work, not just file-work (kernel §13, Canon §7):

- **Create** edges to connect a new node into the existing graph — never leave it an orphan.
- **Strengthen** edges as corroboration arrives (a second `sources`/`feeds`, a `corroborates`).
- **Prune** dead edges — re-point or drop links to superseded/merged nodes.
- **Promote** recurring relations into named edge types (§3.3).

Relational learning is this loop, run on every input. The model is rented; the graph is owned and grows.

## 8. Where the model is applied

S9 is the authority; these are the consumers:

- **Operations Kernel** — applies traversal (§7-read), maintains the edge-map serialisation (§8), runs edge-work in integration (§13).
- **Context Engine** — Canon §7 (page-level link discipline), Dynamic/Inbox graph-participation (source nodes + their edges).
- **Thinking (S10)** — proposes new edges and synthesis across the graph.
- **Self-Development (S13)** — monitors graph-health (§6) and reviews ontology promotions (§3.3).

## 9. Seam to the Model & Retrieval Substrate (S17)

S9 is **instruction-tier**: the graph model the LLM follows by reading and writing markdown. **S17 is code**: the substrate for running this model at scale. Its full *remit* spans embeddings and **semantic (similarity) edges**, **automated traversal and graph-health metrics**, and **vector retrieval** layered over the explicit graph — though this build delivers only part of it (see below). S9 defines what the graph is and how it should grow and be read; S17 builds the machinery to do it programmatically. The model comes first so the machinery has something correct to implement. **Built in S17** ([`MODEL-RETRIEVAL.md`](MODEL-RETRIEVAL.md)): the deterministic shell — the embedding/store substrate, vector **re-ranking**, and the semantic-duplicate and edge-candidate finders. (**Not** part of this build: automated graph traversal and graph-health metrics — traversal stays the instruction-tier read model above, and the mechanical health signals stay `graph-health-scan`'s; only the *semantic*-duplicate signal is the substrate's.) Two boundaries the machinery honours — vector retrieval is **re-ranking only** (it re-orders the walk's candidates, never adds graph-distant pages: the graph stays load-bearing), and embedding-derived edges and semantic-duplicate findings are **candidates** the Thinking layer proposes, never auto-written. Threshold calibration and read-routing integration are S19.
