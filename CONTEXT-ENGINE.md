# Pulse_Brain: Context Engine

The Context Engine is the brain's **knowledge substrate**: Brain-OS layer 2, sitting on the [Operations Kernel](OPERATIONS-KERNEL.md). It is **`canon/`** (the living wiki) compiled from **`inbox/`** and **`dynamic/`** (the raw sources). This document is the **editorial authority** for that substrate: how its pages are written and maintained.

It covers three pillars, one each:

- **Canon**, the wiki itself.
- **Dynamic**, agents' sources and how they are ingested.
- **Inbox**, {{OWNER}}'s sources and capture ergonomics.

This is an **instruction** layer (Brain-OS instruction-vs-code map: Context Engine = instruction). It is markdown the LLM follows; Claude Code is the runtime.

## Lanes: what this doc owns, and what it doesn't

The Context Engine is one of three documents that govern knowledge, and they do not overlap:

- **[`TAXONOMY.md`](TAXONOMY.md) owns structure:** pillars, domains, filenames, and the per-type frontmatter contracts. *What fields a page carries.*
- **[`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md) owns runtime mechanics:** the ingestion front-door (§1), the integration pipeline (§3), graph-first read routing (§7), and index/log integrity (§8). *How a source moves through the brain.*
- **This document owns the editorial standard:** what a good wiki page *is*, and how to keep it good as sources are integrated into it. *What the kernel's `integrate` step should produce on the canon side.*

Where the kernel or taxonomy already specifies something, this doc points to it rather than restating it. The Canon pillar adds the editorial layer on top of the mechanics the kernel already runs.

---

# Canon: the living wiki

> Obsidian is the IDE · the LLM is the programmer · **the wiki is the codebase.**

`canon/` is the compiled, current synthesis the brain serves from. It is **maintained freely** (routine upkeep is never gated) and disagreement is made **visible**, never silently overwritten. The Canon mandate has two halves: a page is *written* (the standard it meets) and *maintained* (how it changes over time). Both follow.

## 1. The three page kinds

Canon holds atomic pages of three kinds, plus glossary terms. Each has a distinct job; choosing the right kind is the first editorial decision.

| Kind | Template | What it is | What belongs in it |
|---|---|---|---|
| **Entity page** | [`entity.md`](vault-template/_templates/entity.md) | The canonical definition of a *thing* the brain refers to repeatedly: a person, organisation, product, protocol, concept, or account. Lives in `canon/entities/`. | What the thing *is*: its identity, defining attributes, and the stable facts other pages depend on. The single place that thing is defined. |
| **Topic summary** | [`canon-note.md`](vault-template/_templates/canon-note.md) (`page_type: topic`) | The compiled, current state of *one subject* within a domain. | The synthesis of what is known about that subject, kept current as sources arrive. Descriptive: "here is the state of X." |
| **Synthesis page** | [`canon-note.md`](vault-template/_templates/canon-note.md) (`page_type: synthesis`) | A page that connects several topics or entities into an **insight that exists in no single source**: a comparison, a thesis, an implication. | Reasoning *across* the graph: "given X and Y, therefore Z." This is where the brain thinks, not just records. |
| **Glossary term** | [`glossary-term.md`](vault-template/_templates/glossary-term.md) | A short, reusable definition referenced across the brain. Lives in `canon/glossary/`. | One term, defined once, linked everywhere. Use when a concept needs a shared definition but not a full entity page. |

**Entity vs glossary vs topic.** An **entity** is a *thing that acts or is acted upon* and accretes facts over time (an account, a product). A **glossary term** is a *definition that stays small* and is pointed at for shared vocabulary (a piece of jargon). A **topic** is the *evolving state of a subject* that draws on many sources. When unsure between entity and topic: if other pages will link to it *as a noun*, it is an entity; if it is *a body of knowledge about something*, it is a topic.

**Topic vs synthesis.** A topic *reports* the current state of one subject. A synthesis *derives* something new by connecting subjects. If you find a topic page starting to argue a thesis that spans other pages, that thesis wants to be its own synthesis page, linked from the topic.

## 2. Atomicity & page boundaries

**One idea, one page** (Brain-OS Law 2). The boundary decisions:

- **Create new vs extend existing.** Before writing a new page, check `canon/_index.md` for an existing home. Extend the existing page when the source deepens a subject already covered; create a new page only when the idea is genuinely distinct. A new page is a new node in the graph, so justify it.
- **Split.** When a page accretes a *second* idea, so that its Summary needs an "and also" to be accurate, split it. The original keeps the primary idea; the second moves to its own page; link the two with `related`.
- **Merge.** Two pages covering the same idea are a defect (duplicate nodes fracture the graph). Merge into the better-sourced page, fold in the other's sources and links, and leave the merged-away page as a redirect (see §6, supersede) so inbound links survive.
- **Don't redefine inline.** When a page mentions an entity or term that has its own page, **link it by `title`** (`[[Entity Name]]`) rather than restate its definition. Each fact has exactly one home; everything else points at it.

## 3. Maintaining freely: how to revise (the integration outcome)

The kernel's [`integrate`](OPERATIONS-KERNEL.md) step (§3) compiles a source into the wiki. This is the standard for what that produces on the page:

- **Reconcile, don't append.** Integration is not a changelog. Read the new source against what the page already claims and *rewrite the synthesis* so the page reads as one current, coherent statement rather than a stack of dated additions. (The append-only timeline is [`log.md`](OPERATIONS-KERNEL.md)'s job, not the page's.)
- **The Summary is the live synthesis.** `## Summary` is the single paragraph that states the page's *present* understanding. It is the most-read line in the brain (read routing surfaces it first). Keep it true after every integration; if the body changes and the Summary doesn't, the page is stale.
- **Preserve provenance on every revision.** A claim that came from a source keeps its `[[source]]` citation when the page is rewritten. Reconciling the prose must not orphan the evidence (see §5).
- **Strengthen *or* challenge.** Integration can confirm the existing synthesis (strengthen it, add the corroborating source) or contradict it (flag it, §4). Both are progress; appending without doing either is not.
- **Routine upkeep is not gated.** Tightening prose, adding a corroborating source, growing a link, fixing a Summary: the LLM does this freely and records it via the kernel's index/log write. No confirmation step.

## 4. Flag, don't gate: the contradiction protocol

The brain maintains the wiki autonomously, but it **never silently overwrites a claim**. When a new source conflicts with an established claim, integration still proceeds: the **flag is the handshake**, not a blocker. This is the operational heart of the Canon pillar.

**Routine revision vs significant revision.** Most integrations are routine and need only the index/log write. A revision is **significant, and must be flagged**, when it:

- *contradicts* an established claim (a source says the opposite of what the page states), or
- *reverses or materially changes* a recorded decision, position, or fact other pages depend on, or
- *merges, splits, supersedes, or deprecates* a page (§6).

Tightening prose, adding corroboration, or growing a link is **not** significant; flagging it would be noise.

**The two-part flag.** A significant revision is surfaced in exactly two places, so it is visible without hunting:

1. **On the page**, an inline callout at the point of conflict, using the standard convention (mirrored in [`canon-note.md`](vault-template/_templates/canon-note.md)):

   ```
   > [!contradiction] <one-line summary of the conflict>
   > - **established:** <prior claim> — [[source-a]]
   > - **new:** <conflicting claim> — [[source-b]]
   > - **status:** unresolved | resolved (<how>)
   ```

2. **In core memory**, a line in the **"Needs review"** list of [`memory/core.md`](OPERATIONS-KERNEL.md) (kernel §5, §10): what conflicts, which page (`[[page]]`), and the source. This is the surface {{OWNER}} scans; the page callout is the detail.

**Resolution lifecycle.** A flag is `unresolved` until reconciled. {{OWNER}} reviews live in Obsidian. When resolved, whether by {{OWNER}} or by a later source that settles it, set `status: resolved (<how>)`, fold the settled claim into the Summary/body, remove the line from core memory's "Needs review", and record the resolution in [`log.md`](OPERATIONS-KERNEL.md). An unresolved flag never silently disappears; it is resolved, not dropped.

> Nothing blocks integration. The synthesis moves forward carrying its disagreement in the open, until the disagreement is settled.

## 5. Provenance & sourcing

The wiki is the answer surface; the sources are its evidence. The discipline:

- **Every page cites its `sources`.** A canon page records, in frontmatter `sources` and inline where a specific claim needs it, the `[[source notes]]` (in `inbox/`/`dynamic/`) it was compiled from. A page with **no source is a smell**: either it predates ingestion (find and attach the source) or it is unsupported synthesis (mark it as the brain's own inference, not fact).
- **Citations survive revision.** When §3 reconciles prose, the supporting `[[source]]` links move with the claims they support. Never drop a citation because the sentence was reworded.
- **Sources are referenced, never absorbed.** Canon compiles *from* sources; it does not copy them. The source note keeps the raw material and provenance; the canon page keeps the synthesis and points back. This is also the data-boundary discipline: the engine ships the *pattern*, never the content.

## 6. Page lifecycle

A canon page is a living node. Its states:

- **Create:** a genuinely new idea earns a new page (§2), fully formed: frontmatter, Summary, body, sources, links, and the index/log write.
- **Revise:** the default, every time a source is integrated (§3). Routine, or significant-and-flagged (§4).
- **Split / merge:** atomicity maintenance (§2). Both are significant revisions: flag and log them.
- **Supersede / deprecate:** a page that is **no longer true is never silently deleted**. Mark it superseded, pointing it at the page that replaces it (`related`, and a one-line note in the body), so inbound `[[wikilinks]]` resolve and the graph stays intact. Removing a node is a graph edit with consequences; treat it as one. Genuine deletion (a page created in error, never linked) is itself a significant, logged action.

Every lifecycle change obeys the kernel's **integrity rule** (§8): the same step updates `canon/_index.md` (including the `links` column), `index.md`, and `log.md`. The map never drifts from the territory.

## 7. The graph is the intelligence

The brain develops by **growing and refining its node-graph**, not by accumulating pages (kernel §13, Brain-OS; the graph model itself is [`NODE-GRAPH.md`](NODE-GRAPH.md)). At the page level this means:

- **Curate `related` deliberately.** Each page's `related` edges are part of the synthesis, not decoration. Add an edge when two pages genuinely bear on each other; the link should earn its place.
- **Link entities and terms by `title`.** Inline `[[Entity Name]]` / `[[Term]]` references *are* graph edges: they are how a page connects to canonical definitions without restating them (§2).
- **Strengthen and prune.** Integration creates new edges, strengthens existing ones (a second source for a link), and prunes dead ones (a `related` page that was superseded). Orphan pages, with no inbound or outbound links, are a graph-health defect the Self-Development layer watches for.
- **The graph spans pillars.** Canon pages link freely to the `[[source notes]]` that feed them and to pages in other domains, so the brain renders as one connected graph in Obsidian.

## 8. Quality bar: an exemplary canon page

The checklist a finished canon page meets. Templates ship this standard into every instance, so it is held high:

- [ ] **One idea.** The page is about exactly one thing; its Summary needs no "and also".
- [ ] **Right kind.** Entity / topic / synthesis / glossary chosen per §1.
- [ ] **Frontmatter complete.** `title` + one-sentence `description` always; the rest of the type's contract per [`TAXONOMY.md`](TAXONOMY.md); a stable `id`.
- [ ] **Summary is current.** One paragraph stating the present synthesis; true as of the last integration.
- [ ] **Sourced.** Every non-inferential claim traces to a `[[source]]`; `sources` frontmatter populated (§5).
- [ ] **Linked.** Canonical things referenced by `[[title]]`, not redefined; `related` curated; no orphan (§7).
- [ ] **Reconciled, not stacked.** Reads as one coherent statement, not a pile of additions (§3).
- [ ] **Disagreement visible.** Any contradiction carries the callout and a core-memory line (§4).
- [ ] **Map in sync.** `canon/_index.md`, `index.md`, and `log.md` updated in the same step (§6, kernel §8).

---

# Dynamic: agents' sources

`dynamic/` is the brain's **agent-gathered source pillar**: raw inputs that background agents find in the open world (web pages, feeds, files, monitoring hits) captured with provenance and compiled into the wiki. It is a *sibling of `inbox/`* (the [Inbox section](#inbox-owners-sources) below); the two are split **by origin**, where dynamic is what *agents* gather and inbox is what *{{OWNER}}* gathers. Like all sources, a dynamic note is kept for provenance and is **never the answer surface**; the wiki is (kernel §2).

**Disambiguation.** "Dynamic" is used in three unrelated senses across the brain; this section is only the first:
- the **dynamic source pillar**, this section;
- `tier: dynamic` on a **glossary term**, a term discovered at runtime rather than curated (a canon property, not this pillar);
- the kernel's **`log.md` recall timeline**, operational continuity, explicitly *distinct from the dynamic knowledge pillar* (kernel §10).

## 1. The capture contract

When an agent finds something, it files **one `dynamic-note`** ([`dynamic-note.md`](vault-template/_templates/dynamic-note.md)) per source. This is the **receiving contract**: the Research & Background Agents layer builds the agents, and this pillar defines what a well-formed source they hand in must contain. A dynamic note is complete when it carries:

- **`## Summary`**, one paragraph: what this source says.
- **`## Extracted points`**, the specific claims the kernel will integrate into the wiki. This is the payload; vague sources that yield no extractable point are not worth capturing.
- **`## Provenance`**, where it came from, when, and how retrieved, enough to **re-find or cite** it.
- **Frontmatter** (per [`TAXONOMY.md`](TAXONOMY.md)): `source` + `source_type` (the provenance handle), **`contributed_by`** (which agent gathered it, the author), **`confidence`** (§2), `domain`, `tags`, and `feeds` (filled once integrated, §3).

One source, one note (atomic, Law 2). A find that spans two genuinely distinct subjects is two notes.

## 2. Confidence & trust

Dynamic sources come from the **open world**, so their reliability varies, unlike inbox sources, which are {{OWNER}}'s own and implicitly trusted. Every dynamic note therefore carries a structured **`confidence: high | medium | low`** so trust is machine-usable, not buried in prose.

**Assigning it.** The gathering agent sets confidence from the source's **authority** (is the origin reputable or primary?), **corroboration** (do independent sources agree?), and **recency** (is it current for a claim that changes over time?). When unsure, it rates *down*: precision over optimism.

**Using it.** Confidence weights how a source is integrated into canon:
- **High**: integrate normally per the Canon pipeline.
- **Medium / low**: the claim must be **corroborated** before it hardens into a canon assertion; until then it is integrated as *reported, not established* (attributed in-line to its source).
- A medium/low source **never silently overwrites** an established canon claim. A conflict routes through the **Canon flag protocol** ([Canon §4](#4-flag-dont-gate-the-contradiction-protocol)), flagged on the page and in core memory, not resolved by the weaker source alone.

Confidence **travels with the claim's provenance** into canon: a canon assertion resting on a low-confidence source carries that qualifier until corroboration lifts it.

## 3. Lifecycle: capture, integrate, feed

A dynamic source's life:

- **Capture**: the agent files the note (§1) into `dynamic/<domain>/`. **Dedup first:** if the source is already held, *refresh or extend* the existing note rather than create a duplicate, since duplicate sources distort confidence and clutter the graph.
- **Integrate**: the kernel runs the integration pipeline (kernel §3), compiling the extracted points into `canon/`. The **canon-side outcome is governed by the [Canon section](#canon-the-living-wiki)**; this pillar does not restate it.
- **Feed**: `feeds` records the `[[wiki pages]]` this source informed, the back-link that makes provenance traceable from source to synthesis and back.
- **Freshness**: monitoring sources go stale. A newer source on the same fact **supersedes** the older; the stale note is **kept for provenance but not re-surfaced** in read-routing (recency is a ranking signal, kernel §7). Stale never means deleted; provenance is permanent.

## 4. Graph participation

A dynamic note **is a node**; its `feeds` (→ canon pages) and `related` (→ other notes) entries **are edges** registered in [`dynamic/_index.md`](vault-template/dynamic/_index.md) (the edge-map, kernel §8; the node/edge model is [`NODE-GRAPH.md`](NODE-GRAPH.md)). This pillar owns how a *source node* enters and what it connects to. **Growing and refining the canon graph** (synthesis, strengthening, pruning) is the integration outcome, owned by [Canon §7](#7-the-graph-is-the-intelligence) and kernel §13, and is the subject of its own dedicated Node-Graph work on the roadmap. This pillar hands the source to that pipeline; it does not re-own the graph.

## 5. Boundary with the agents layer

This pillar is the **source pillar**: the capture contract, the trust model, and the source lifecycle, that is, *what a dynamic source is and what it must contain*. The **Research & Background Agents layer** is the **producers**: the agents that gather these sources and the scheduling and autonomy that runs them. That layer inherits this contract rather than inventing its own.

---

# Inbox: {{OWNER}}'s sources

`inbox/` is the brain's **{{OWNER}}-gathered source pillar**: everything {{OWNER}} adds (a thought, a link, a file, a page, a photo or video) captured with provenance and compiled into the wiki. It is the **sibling of the [Dynamic section](#dynamic-agents-sources)**, split by origin: dynamic is what *agents* gather, inbox is what *{{OWNER}}* gathers. Like all sources, an inbox note is kept for provenance and is **never the answer surface**; the wiki is.

Inbox sources are **implicitly trusted**, since {{OWNER}} added them, so there is **no `confidence` field** (that is dynamic-only; kernel sources from the open world need it, {{OWNER}}'s do not). The trust work here is done by the **two sub-kinds** below, not a score.

## 1. Two sub-kinds: primary vs curated-external

What {{OWNER}} adds is one of two kinds, and integration treats them differently because their *authority* differs:

- **Primary, {{OWNER}}'s own thoughts & decisions** (`source_type: thought`, sometimes `note`). {{OWNER}} **is the authority**. A primary source can **assert or seed canon directly**, and it **carries weight in contradictions**: an {{OWNER}} decision can settle or override an existing claim. If it contradicts established synthesis it still routes through the **Canon flag protocol** ([Canon §4](#4-flag-dont-gate-the-contradiction-protocol)) so the change is visible, but {{OWNER}}'s stated position is authoritative, not merely another voice. `source` is optional (the owner *is* the origin).
- **Curated-external, material {{OWNER}} collected** (`source_type: url | file | page`, and the multimodal types below). Trusted as **worth attention** because {{OWNER}} flagged it, but its *claims* are the **external author's**, not {{OWNER}}'s. So it is integrated like any external source: claims are **attributed to their author** and **corroborated before they harden** into a canon assertion. Curation raises priority, not truth-value. Provenance is required.

The distinction is about **who is making the claim**, not how it arrived.

## 2. Source modalities

An inbox source's `source_type` spans three modality groups:

- **Text**: `thought` / `note` ({{OWNER}}'s own words).
- **Collected**: `url` / `file` / `page` (external material, by reference).
- **Multimodal**: **`image` / `video`** (a photo, screenshot, or clip {{OWNER}} captures or uploads).

Multimodal sources are captured like any other, but the brain only draws *meaning* from them once a **multimodal model perceives** them, transcribing a video or reading a photo, into the `## Extracted points` the kernel then integrates. That perception capability is the **Model & Retrieval Substrate**; this pillar defines the source kind and capture contract and leans on the substrate for extraction. Modality is **orthogonal** to the two sub-kinds (§1): a whiteboard photo of {{OWNER}}'s own idea is *primary*; a photo of someone else's slide is *curated-external*.

## 3. The capture contract

When {{OWNER}} adds something, the kernel files **one `inbox-note`** ([`inbox-note.md`](vault-template/_templates/inbox-note.md)) per source, complete when it carries:

- **`## Summary`**, one paragraph: what this source is.
- **`## Extracted points`**, the claims to integrate (for multimodal, what the model perceived).
- **`## Provenance`**, where it came from and **why {{OWNER}} captured it**, enough to re-find or cite (optional origin for a pure thought).
- **Frontmatter** (per [`TAXONOMY.md`](TAXONOMY.md)): `source_type`, `source` (optional for a thought), **`added_by: {{OWNER}}`** (author), `domain`, `tags`, `feeds` (filled once integrated). No `confidence`.

One source, one note (atomic, Law 2).

## 4. Capture ergonomics: the front-door

Inbox is where **friction matters most**: friction kills capture, and a brain that is annoying to feed stays empty. The kernel's **no-manual-filing** rule (kernel §1) is the contract: {{OWNER}} drops a file, pastes a URL or text, or simply **says a thought in conversation**, and the kernel **captures, integrates, and reports what changed**, with no filing and no forms. {{OWNER}} adds; the brain does the rest.

This pillar owns these capture *behaviours* on the **CLI/chat channel**. Additional **capture channels (a mobile app for capture or upload on the go, and the sync backend it needs) are deferred to the Interface layer and MCP hosting**: recorded on the roadmap, built later as code. The contract here is what those channels will feed into.

## 5. Lifecycle: capture, integrate, feed

Mirrors the Dynamic lifecycle:

- **Capture**: the note is filed into `inbox/<domain>/`. **Dedup first:** if the source is already held, refresh or extend the existing note rather than duplicate it.
- **Integrate**: the kernel runs the integration pipeline (kernel §3), compiling the extracted points into `canon/`; the **canon-side outcome is governed by the [Canon section](#canon-the-living-wiki)**.
- **Feed**: `feeds` records the `[[wiki pages]]` this source informed, the back-link that makes provenance traceable from source to synthesis.

## 6. Graph participation

An inbox note **is a node**; its `feeds` (→ canon pages) and `related` (→ other notes) entries **are edges** in [`inbox/_index.md`](vault-template/inbox/_index.md) (the edge-map, kernel §8; the node/edge model is [`NODE-GRAPH.md`](NODE-GRAPH.md)). This pillar owns how an {{OWNER}}-source node enters and what it connects to; **growing the canon graph** is the integration outcome, owned by [Canon §7](#7-the-graph-is-the-intelligence) and kernel §13 (and the dedicated Node-Graph work on the roadmap).

---

> **Context Engine complete.** With **Canon** (the wiki), **Dynamic** (agents' sources), and **Inbox** ({{OWNER}}'s sources) all specified, Brain-OS layer 2 is fully defined. Next on the roadmap is the **Node-Graph** work, consolidating the graph model the whole brain runs on.
