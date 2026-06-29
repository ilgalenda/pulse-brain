# Pulse_Brain: The Thinking Layer

The brain's first **active** layer (Brain-OS layer 3). Where the Operations
Kernel, the Context Engine, and the Node-Graph build and maintain the knowledge
substrate, Thinking is the layer that **reasons over** it: connecting ideas
across pages, generating insight that exists in no single note, proposing the
edges and promotions the graph is missing, and advising {{OWNER}} as a partner.

It is an **instruction** layer (in the Brain-OS instruction-vs-code map, Thinking
is instruction): markdown the LLM follows, with Claude Code as the runtime. It is
the home of Law 3 (the intelligence partner): the brain that thinks *with*
{{OWNER}}, not just *for* them. The graph model it applies is
[`NODE-GRAPH.md`](NODE-GRAPH.md); the runtime it composes is
[`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md).

## 1. What the layer is: reflection, not reaction

Thinking is defined by its contrast with the kernel's integration step. Both
read the graph and write canon, so the line between them must be exact:

| | **Integration** (kernel §3) | **Thinking** (this layer) |
|---|---|---|
| Trigger | A **new source** arrives | **Reflection**: a question, an opportunity, a deliberate pass |
| Stance | **Reactive** | **Reflective** |
| Scope | The pages **that source touches** | **Across what the brain already knows** |
| Job | Compile *this source* into the wiki | Find what *connects, conflicts, implies, or emerges* in the existing graph |

Integration asks *"given this new source, what changes?"* Thinking asks *"across
everything we already hold, what is true that no single page yet states?"* The
kernel keeps the wiki current as material flows in; Thinking makes the wiki
**think**: it is where the brain reasons, not merely records.

## 2. Lanes: what this doc owns, and what it doesn't

Thinking owns **reasoning over existing knowledge**. It defers everything else
to the layers that already own it, and **adds no new kernel primitive**. Every
operation below composes the existing capability contract (§5):

- **[`TAXONOMY.md`](TAXONOMY.md)** owns structure (fields, page kinds).
- **[`OPERATIONS-KERNEL.md`](OPERATIONS-KERNEL.md)** owns runtime mechanics:
  ingestion, the integration pipeline, read-routing, index/log integrity.
- **[`NODE-GRAPH.md`](NODE-GRAPH.md)** owns the node/edge model Thinking traverses.
- **[`CONTEXT-ENGINE.md`](CONTEXT-ENGINE.md)** (Canon) owns the editorial standard
  for the pages Thinking writes: kinds, atomicity, the flag protocol, lifecycle.

Where another layer already specifies something, this doc points to it. Thinking
is the *reasoning* on top of mechanics that already run.

## 3. The operations

Five operations. Each names whether Thinking **owns** the operation outright or
only **feeds** an existing lifecycle owned elsewhere, so no lane collides.

### 3.1 Synthesis (owned)

The signature output. Thinking reasons across several pages or entities to reach
an insight that is in **no single source** (a comparison, a thesis, an
implication) and writes it as a **`page_type: synthesis`** canon page
([Canon §1](CONTEXT-ENGINE.md)). "Given X and Y, therefore Z." This is the layer
earning its place: the wiki gains a claim no source handed it. Every synthesis
page obeys the Canon editorial standard and the grounding discipline (§6).

### 3.2 Link proposal (owned)

A note is only as valuable as its edges ([Node-Graph §1](NODE-GRAPH.md)).
Thinking walks the graph for pages that **bear on each other but are not yet
linked**, and creates the missing `related` / `[[wikilink]]` edges (Node-Graph
§7 *create*, named as a Thinking consumer in §8). Routine, well-justified links
are written freely. A link that meets [Canon §4](CONTEXT-ENGINE.md)'s
*significant-revision* test (it reverses or materially changes a claim other
pages depend on) is surfaced via the existing flag (§6): Thinking reuses that
test, it does not coin a new threshold.

### 3.3 Contradiction resolution proposal (feeds, does not own)

When the graph carries an **unresolved `contradicts` flag**, Thinking reasons
across the graph to propose *which claim wins, or how the two synthesise*.

The seam is strict. Thinking does **not**:
- **detect or raise** the contradiction: that is source-driven, owned by the
  kernel ([§5](OPERATIONS-KERNEL.md)) and [Canon §4](CONTEXT-ENGINE.md);
- **finalise** it: resolution belongs to the Canon §4 lifecycle ({{OWNER}}
  reviewing in Obsidian, or a later source that settles it).

Thinking **proposes into** that existing lifecycle: it offers a reasoned
resolution as a candidate, surfaced via the existing flag (§6), for {{OWNER}} to
ratify. Unresolved contradictions are also a graph-health signal that the
**Self-Development layer** monitors (Node-Graph §6/§8): Thinking supplies the
reasoning, Self-Development owns the system-level watch.

### 3.4 Content-promotion candidates (owned for content; feeds for ontology)

Two different promotions, two different owners, kept apart deliberately:

- **Content promotion**: surfacing **canon-worthy material** (raw source content
  or a recurring pattern that deserves its own page), per Brain-OS layer 3's
  "proposing promotions into canon". *Owned by Thinking.*
- **Edge-type / ontology promotion**: naming a *new typed edge* when a relation
  recurs ([Node-Graph §3.3](NODE-GRAPH.md) provisional → recurring → promoted).
  Thinking may **surface a recurring relation as a candidate**, but the promotion
  *decision* (extending the edge vocabulary) is the **Self-Development layer's**,
  reviewed through the graph-health and Self-Development loop (Node-Graph
  §3.3/§8). *Feeds, does not own.*

### 3.5 Challenge and advise (owned, zero seam-overlap)

Law 3 in full. This is the one operation **no other layer touches**, and the
clearest expression of the intelligence partner. It is two halves:

- **Honest**: pressure-test, challenge, surface the weakness or the
  consideration {{OWNER}} is missing. An advisor, not a yes-man.
- **Decision-support**: reason *toward a recommendation*, weigh options, lay out
  trade-offs, advise. "Help {{OWNER}} think and decide", "with, not for".

**Pure-questioning delivery.** The *honest/challenge* half can be run on its own,
with the recommendation deliberately withheld, via the
[`socratic`](vault-template/.claude/skills/socratic/SKILL.md) skill: {{OWNER}}
questioned toward their *own* answer. That is **this operation instrumentised, not
another layer touching it**. Socratic stays within the Thinking lane and coins no
new primitive, so "zero seam-overlap" holds: it *is* §3.5, delivered pure. Use
challenge-and-advise when {{OWNER}} wants the brain's view, socratic when they want to
reach their own and have chosen not to be given one.

Output is **conversational**, not a wiki write, so it sits outside the
flag-don't-gate machinery (§6). A decision worth keeping may be captured as an
{{OWNER}} `thought` source ([Inbox §1](CONTEXT-ENGINE.md)) and integrated like any
other, **but only if {{OWNER}} actually ratifies it.** An {{OWNER}} `thought` is
*primary* and can assert or override canon (Inbox §1); the brain must therefore
**never** label its *own* recommendation as an {{OWNER}} thought. The captured
note records {{OWNER}}'s explicit decision; absent that ratification the advice is
the **brain's inference** (§6.1, marked accordingly), not a primary source. This
is what keeps decision-support from becoming a back-door that launders advice into
owner-authority canon.

**The engine specifies the capability and the discipline, not the texture.**
What a good advisor *sounds like* (the judgement of when to push, what to
recommend) matures at instance time against real data (`Pulse-{{OWNER}}-Brain`).
The Thinking layer states the stance and stops short of scripting a voice the
engine has no data to ground.

## 4. Triggers: when Thinking runs

- **On-demand**: {{OWNER}} asks a question or for a view; Thinking reasons over
  the loaded graph to answer, synthesise, or advise.
- **Proactive / opportunistic**: mid-work, Thinking surfaces a connection,
  tension, or implication unprompted (Law 3, *proactive*). The brain volunteers
  what it notices.
- **Deliberate sweep**: a "think pass" that reasons across a slice of the graph
  to generate synthesis, propose links, and work open inferences. The sweep also
  runs the **grounding re-trace** (§6.2): for each synthesis page it checks the
  Summary's load-bearing claim against the page's cited `sources` and surfaces any
  claim that is **unsourced and unmarked**, the missed-marker backstop. This is a
  traceability check (does a cited source assert the claim?), not a re-derivation.

**The sweep reasons over knowledge, not graph health.** It asks what *connects,
conflicts, or emerges in the content*; it does **not** compute graph-health
metrics (orphans, hub overload, stale edges). Those are Node-Graph §6 signals
owned by the **Self-Development layer**. (The unsourced-and-unmarked check above
is the one signal Thinking feeds that layer's §6 list; see §6.2.) Same `load`
primitive, different object.

**Sweep output is throttled so it cannot overflow core memory.** A bulk sweep can
generate many significant items, and `core.md`'s "Needs review" list is
**always-loaded and hard-capped** (kernel §10). So a sweep flags at most a small
cap of items individually into `core.md`; the remainder roll up into a **single
line**, *"N further proposals from sweep <date>, see [[log]]"*, with the detail
appended to the uncapped `log.md`. This is **not a gate** (nothing blocks the
writes; only their *index* moves off the capped file), and it keeps session
anchors from being crowded out.

**Autonomy belongs to the Research and Background Agents layer, not Thinking.**
Thinking defines the *capability*; the **scheduling and background execution** of
any trigger (running a sweep unattended, watching for the moment to be proactive)
belongs to the **Research and Background Agents layer**. Thinking is what that
layer runs; the agents layer is when it runs.

## 5. Built on the kernel contract

Thinking introduces **no new primitive**. Every operation is a composition of the
kernel's existing capability contract ([§12](OPERATIONS-KERNEL.md)):

```
load (graph-first read)  →  reason  →  link / write (synthesis) / flag  →  update-index / update-log / update-memory
```

It **reads** graph-first (kernel §7), **reasons** over what it loads, and
**writes** through the same routed, index-keeping path every other write uses, so
the maps never drift (kernel §8). "The runtime everything plugs into" includes
Thinking: it is a consumer of the contract, not an exception to it.

## 6. Grounding and the quality bar

The load-bearing section. Thinking is the first layer that **generates** rather
than records, so it is the one most able to let an inference masquerade as a fact.
Grounding works in **two passes**, because no single pass is enough:

- **At write time**: the brain marks the inference it *recognises* it is making
  (§6.1). This is honest self-report; it catches the acknowledged guess.
- **As a backstop**: a later **re-trace** catches the inference the brain *failed
  to recognise* at write time, the real confabulation case (§6.2). Self-report
  alone cannot catch this, so the system does not rely on it.

**One principle: unverified claims are always visibly marked, never silently
asserted.** The brain already does this twice; Thinking is the third face of the
same idea:

| Mechanism | Marks | Owner |
|---|---|---|
| `confidence: high/medium/low` | open-world source reliability | Dynamic ([§2](CONTEXT-ENGINE.md)) |
| `[!contradiction]` callout | conflicting claims | Canon ([§4](CONTEXT-ENGINE.md)) |
| **`[!inference]` callout** | **brain-generated, un-sourced reasoning** | **Thinking (here)** |

### 6.1 The `[!inference]` marker: the decidable test

The test is on the **load-bearing conclusion, not the page**. Every synthesis
page rests on cited sources *and* states a conclusion, so "is this page derived
or compiled?" is undecidable and must not be asked. Ask instead:

> **Does any one cited source actually assert this conclusion, or only the
> premises I reasoned from?**

If a source asserts it, it is sourced canon (cite it). If the conclusion is the
brain's own step *beyond* every source (true only if the reasoning holds) it
carries an `[!inference]` marker, symmetric with the `[!contradiction]`
convention already in [`canon-note.md`](vault-template/_templates/canon-note.md):

```
> [!inference] <the reasoned claim, in one line>
> - **basis:** [[page-a]], [[page-b]] — the pages this was reasoned from
> - **status:** unverified | weakly-supported (<source>) | confirmed (<source>)
```

This restates, for generated claims, [Canon §5](CONTEXT-ENGINE.md) ("mark
unsupported synthesis as the brain's own inference, not fact") and [Canon §8](CONTEXT-ENGINE.md)
("every *non-inferential* claim traces to a `[[source]]`"). Only `confirmed`
clears the marker; `weakly-supported` records a medium/low source that does not
yet harden the claim (§6.2).

**The limit, stated plainly.** This marker is honest **self-report at write
time**: it catches the inference the brain *recognises*. Confabulation is the
case where the brain does **not** recognise it is guessing, so the marker alone
cannot catch it. The backstop is §6.2's re-trace, surfaced as a graph-health
signal ([Node-Graph §6](NODE-GRAPH.md)): **a canon claim with no cited
`[[source]]` and no `[!inference]` marker** is the confabulation surface, caught
on a later pass, *not* at write time.

### 6.2 Resolution and the missed-marker backstop

**Open markers are findable from the map.** An open `[!inference]` is registered
in the edge-map as an **`edge/inference` tag** (the tag-surfacing convention of
[Node-Graph §3.2](NODE-GRAPH.md), with no new frontmatter field) and **indexed by
its `basis` pages**. So the brain can find every open inference, and every inference
that *depends on* a given page, without opening files. This is what makes both
the backstop and resolution actually fire.

**The backstop (catches missed markers).** The grounding re-trace runs on the
sweep (§4): for each synthesis page, check the Summary's load-bearing claim
against the cited `sources`. A claim that is **unsourced and unmarked** is
surfaced as the [Node-Graph §6](NODE-GRAPH.md) health signal and either marked
(if it is inference) or sourced (if a citation was simply missed). This is the
second pass §6.1 relies on; it does *not* depend on the brain having recognised
the inference the first time.

**Resolution: active hunt is primary, not passive integration.** A marker
clears when evidence grounds the claim, but matching a source to a *specific* open
inference is **reasoning, not a mechanical attach** (until the semantic-matching
substrate, [described in NODE-GRAPH.md §9](NODE-GRAPH.md), is added). The two
paths, in priority order:

1. **Active hunt (primary).** §6.3's background agents and the sweep walk the
   `edge/inference` set, research each open marker, and resolve it. This is the
   path that reliably closes markers, because it *seeks them out*.
2. **Passive clear-on-touch (opportunistic).** When integration happens to touch
   a page in an open marker's `basis`, it checks whether the new source grounds
   the marked claim and clears it if so: *not-gated upkeep* ([Canon §3/§4](CONTEXT-ENGINE.md)).
   This only fires when evidence lands on a basis page, so it is a bonus, not the
   mechanism the loop depends on.

Either path respects source trust ([Dynamic §2](CONTEXT-ENGINE.md)):

- source **supports** it, **high confidence** → `status: confirmed`, marker cleared;
- source **supports** it, **weak** (medium/low) → `status: weakly-supported`,
  marker **stays** (a weak source does not harden a guess into a fact);
- source **conflicts** with it → not a resolution; routes to the
  `[!contradiction]` flag ([Canon §4](CONTEXT-ENGINE.md)) for {{OWNER}}.

### 6.3 The self-correction loop (seam to the agents layer)

An `[!inference]` marker is the brain admitting *"reasoned, but unproven"*, which
is precisely a **research prompt**, and the `edge/inference` set (§6.2) is the
queue of them. The **Research and Background Agents layer** walks that set, tries
to confirm each in the open world, and resolution clears them per §6.2: the
**primary** resolution path. This closes Law 1's *"synthesise → (maybe) research"*
loop on itself: the brain checks its own homework without being asked.

### 6.4 Audit stamp: accountability for autonomy

When the active hunt (§6.3) **auto-confirms** an inference via a reliable source, a
claim's status has changed *without {{OWNER}} in the loop*, the only such case.
That resolution is **stamped in [`log.md`](OPERATIONS-KERNEL.md)** (kernel §6/§8):
what was confirmed, on which page, by which source/agent, and at what confidence.
{{OWNER}} gets a one-glance trail of everything the brain settled on its own.

### 6.5 Flag-don't-gate still holds

Thinking writes under the same law as integration ([Canon §4](CONTEXT-ENGINE.md),
kernel §5): routine links and synthesis are **written freely**; significant
proposals (a resolution, a reframing, a promotion candidate) are **surfaced via
the existing two-part flag**: the page callout plus the "Needs review" list in
[`memory/core.md`](OPERATIONS-KERNEL.md). There is **no separate proposals queue**:
a review queue proposals must clear before entering the wiki would re-introduce
the pre-write gate the kernel's flag-don't-gate design abolished (kernel §5;
ARCHITECTURE §1 boundary). The existing flag *is* the surface. Precision over
recall: when unsure, the brain marks rather than asserts.

## 7. Seams to neighbouring layers

- **← Node-Graph.** Thinking *applies* the model: it traverses edges,
  proposes new ones (§3.2), and respects the seeded-but-open edge vocabulary. It
  reasons over the graph; it does not redefine it.
- **→ Research and Background Agents.** When reasoning hits a gap internal
  knowledge cannot fill (an open inference, an unsupported claim), Thinking hands
  a research prompt to the agents layer (§6.3). That layer also *schedules*
  Thinking's triggers (§4).
- **↔ Self-Development and Growth.** The split is **content vs system**.
  Thinking reasons over *knowledge*; Self-Development audits the *platform*: graph
  health (Node-Graph §6), ontology promotions (Node-Graph §3.3), capability gaps.
  Thinking supplies reasoning and surfaces candidates; Self-Development owns the
  meta-loop.
- **Law 3 (cross-cutting).** Thinking is where the intelligence partner most
  visibly lives (§3.5), but the proactive, honest, with-not-for stance colours
  every layer.

> **Thinking complete.** The brain no longer only stores and compiles knowledge:
> it reasons over it, proposes what the graph is missing, marks honestly what it
> has only inferred, and advises {{OWNER}} as a partner. Next on the roadmap is
> the **Research and Background Agents layer**, the autonomy that runs Thinking
> unattended and closes the self-correction loop.
