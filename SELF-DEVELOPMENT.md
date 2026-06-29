# Pulse_Brain — Self-Development & Growth

Brain-OS **layer 6**: the meta-loop that grows the **platform itself**. Where
Thinking reasons over knowledge, Research gathers into it, and Builder grows the
capability surface on demand, this layer **audits the brain for weakness and drives
the other layers to fix it**. It is the brain turning its intelligence on its own
condition — the judgement that decides *when* and *what* to grow, and points the
hands that do the growing.

This is an **instruction** layer ([BRAIN-OS instruction-vs-code map](BRAIN-OS.md)):
markdown the LLM follows; Claude Code is the runtime. It introduces **no new kernel
primitive** — every action composes the existing capability contract
([OPERATIONS-KERNEL §12](OPERATIONS-KERNEL.md)) and the layers it drives. The
*code* that computes graph-health metrics at scale is **S17**, not this layer
([NODE-GRAPH §9](NODE-GRAPH.md)); S13 is the model, S17 is the machinery.

## 1. What this layer is — the meta-loop, not a hand

S13 is defined by its contrast with Builder. Both grow the brain, so the line must
be exact ([BUILDER §1](BUILDER.md) draws it from the other side):

- **Builder (S12)** is **reactive**: a *present task* needs a capability that isn't
  here — build one instrument, now. The caller (owner or the brain) already knows
  what is missing.
- **Self-Development (S13)** is the **meta-loop**: nobody asked. The brain audits
  *itself*, finds where it is weak across the whole graph and capability surface,
  decides what is worth fixing, and **drives Builder, Research, and Thinking** to do
  it.

S12 is the **hands**; S13 is the **judgement that points them**. The act of fixing
is identical whether a task surfaced the need or the audit did — S13 adds the
*system-level noticing and prioritising* that no single task performs. It owns the
**when** and the **what**, never the **how**: the how already belongs to the layer
it dispatches to.

## 2. Lanes — owns, drives, defers

- **Owns** the audit-and-growth meta-loop (§3): the system-level scan, the triage,
  the prioritisation, and the *record* of what was grown and why.
- **Owns** two growth decisions outright (§5): **ontology promotion**
  ([NODE-GRAPH §3.3](NODE-GRAPH.md)) and **systemic capability-gap** detection.
- **Drives** — does not perform — remediation: it routes each finding to the layer
  that owns the fix (§4). It never link-proposes, resolves a contradiction, gathers,
  or builds itself.
- **Monitors** the graph-health signals **defined** by [NODE-GRAPH §6](NODE-GRAPH.md);
  it does not define them. It acts on them.
- **Composes** the kernel capability contract and the existing layers; it adds no
  primitive and coins no new flag — significant proposals surface through the
  **existing** two-part flag ([Canon §4](CONTEXT-ENGINE.md), kernel §10).
- **Defers** scheduling to S11 (§6), metric computation at scale to S17
  ([NODE-GRAPH §9](NODE-GRAPH.md)), and every editorial/graph/runtime mechanic to
  the layer that already owns it (§4).
- **Does not** own the reactive single-task gap (that is S12), the content sweep
  (that is S10 — [THINKING §4](THINKING.md) keeps health metrics *out* of it and
  assigns them here), or the heavy code substrate (S17/S18).

## 3. The meta-loop

One cycle, run on a slice of the brain at a time:

```
audit  →  triage / prioritise  →  route to the owning hand  →  drive  →  record
```

- **Audit** — compute the graph-health signals (§4) over the edge-maps, and scan for
  the two owned growth signals (§5). The cheap, mechanically-decidable signals come
  from the [`graph-health-scan`](vault-template/.claude/tools/graph-health-scan)
  tool (exact, deterministic); the judgement signals the LLM reasons out.
- **Triage / prioritise** — not every signal is worth acting on now. Rank by
  **damage to the graph** (a duplicate node fractures more than a single orphan) and
  by **cheapness of the fix**. A bounded audit reports the top findings and stops; it
  does not try to heal the whole graph in one pass.
- **Route** — map each finding to the layer that owns its remedy (§4). S13 names the
  fix and the owner; it does not apply the fix.
- **Drive** — hand the work off: invoke the owning layer's instrument (a Thinking
  link pass, a research prompt onto the `edge/inference` queue, a `/build` request),
  or, for the two owned decisions, prepare the proposal to the autonomy gate (§5).
- **Record** — stamp what the audit found and dispatched through the kernel's
  **`update-log`** ([OPERATIONS-KERNEL §6/§8/§12](OPERATIONS-KERNEL.md), the
  append-only audit tier), so the brain's self-growth has a permanent, reviewable
  trail. The layer *composes* the capability; an autonomous worker hands the record
  off for the kernel to write, never writing `log.md` itself (§8).

## 4. The signals it monitors, and where each routes

S13 **dispatches**; the remedy belongs to the named layer. The seven
[NODE-GRAPH §6](NODE-GRAPH.md) signals, with their owners:

| Signal | Decided by | Routed to (owns the fix) |
|---|---|---|
| **Orphans** | tool | Thinking link-proposal ([§3.2](THINKING.md)) — connect, or prune if dead weight ([Canon §6](CONTEXT-ENGINE.md)) |
| **Weak connectivity** | judgement (needs traversal — S17) | Thinking link-proposal ([§3.2](THINKING.md)) |
| **Stale edges** (link to a superseded node) | tool | kernel edge-work — re-point/prune in integration ([NODE-GRAPH §7](NODE-GRAPH.md)) |
| **Unresolved `contradicts`** | tool (open `edge/contradicts` tag) | Thinking resolution-*proposal* ([§3.3](THINKING.md)) → {{OWNER}} ratifies via the flag ([Canon §4](CONTEXT-ENGINE.md)) |
| **Unsourced-and-unmarked claim** | judgement (Thinking re-trace feeds it, [THINKING §6.2](THINKING.md)) | Research agents — onto the `edge/inference` queue (the S10/S11 self-correction loop) |
| **Hub overload** | judgement | Canon split candidate ([§2](CONTEXT-ENGINE.md)) → surfaced for {{OWNER}} |
| **Duplicate nodes** | tool (exact title) / judgement (semantic — S17) | Canon merge candidate ([§6](CONTEXT-ENGINE.md)) → surfaced for {{OWNER}} |

Two reads of this table matter:

- **The tool decides the mechanical signals; the LLM decides the judgement ones.**
  Orphans, stale edges, exact-title duplicates, and open `edge/contradicts` tags are
  set/tag operations over the edge-map (§7) — exact, and the tool's job. Whether a
  hub is *overloaded enough* to split, whether two pages are *the same idea* in
  different words, and *weak connectivity* (a node reachable only through one fragile
  edge) are judgements the LLM makes — the last two need real graph traversal, which
  S17 industrialises ([NODE-GRAPH §9](NODE-GRAPH.md)); until then they are reasoned,
  not scanned.
- **Every route lands in an existing lifecycle.** S13 never invents a fix path: it
  feeds Thinking's proposals, the kernel's edge-work, the research queue, or Canon's
  editorial lifecycle — all of which already exist and already flag-don't-gate.

## 5. The two growth decisions it owns

Beyond routing health signals, S13 owns two decisions outright — both **mutate
shared meaning**, so both pass the autonomy gate (§6):

- **Ontology promotion** ([NODE-GRAPH §3.3](NODE-GRAPH.md)). A relation that began
  provisional, recurred across nodes, and proved useful is **named as a typed edge**.
  Thinking *surfaces* the recurring relation as a candidate
  ([THINKING §3.4](THINKING.md), *feeds*); S13 *decides* the promotion. Deciding
  means editing the edge vocabulary in `NODE-GRAPH.md` itself — a change to the frame
  every layer reads, so it is gated, never silent.
- **Systemic capability gaps.** A *recurring* unmet need across sessions — not the
  single-task gap S12 handles, but a pattern ("the brain keeps needing X and has to
  improvise each time"). S13 names it and **drives Builder**: it issues the
  `/build` request, then Builder's own lifecycle and gate ([BUILDER §4/§5](BUILDER.md))
  take over. S13 decides *that* the brain should grow a capability; Builder decides
  *how* and builds it.

The brain may also notice **architecture weakness** — a layer doc that is wrong,
under-specified, or contradicted by how the brain actually runs. This is the most
consequential growth of all, and the most tightly gated (§6): S13 *proposes* the
edit, never applies it.

## 6. The autonomy gate — three tiers

S13 acts without being asked, so its authority must be drawn precisely. The
governing distinction is **additive-and-isolated vs mutating-shared-meaning**, not a
vague risk dial. Three tiers, each matched to the nature of the change:

| Change | Gate | Why |
|---|---|---|
| Compute signals · route remediation | **Free** | Read-only, or the route lands in a lane that already flag-don't-gates |
| Drive Builder to add an instrument | **Build-then-record** ([BUILDER §5](BUILDER.md)) | A new instrument is additive, isolated, reversible — a file in a lane |
| **Mutate shared meaning** — promote an edge type, or edit a layer doc | **Propose build-complete → ratify** | It changes the frame every layer reads *and ships into every instance*; the engine, not one vault |

The third tier is the one this layer adds. The discipline that keeps it sharp rather
than toothless: **S13 does the full preparation autonomously** — detect the recurring
relation or the architecture flaw, draft the *exact* edit, validate it against the
existing vocabulary and the surrounding docs, and queue it — so {{OWNER}}'s
ratification is a one-glance yes/no, not work. **Autonomy runs right up to the
boundary of changing shared meaning; the human crosses that boundary cheaply.** A
queued proposal is surfaced as a **Pulse decision** (project `.claude/CLAUDE.md`) via
the existing flag (page callout + `core.md` "Needs review", kernel §10) and recorded
in `log.md`. The brain **never silently rewrites its own ontology or architecture** —
those are explicit, logged, ratified state transitions ([Immutability](PRINCIPLES.md)).

This mirrors how S13 treats the layers it drives: it does the judgement and the
preparation, and the consequential act crosses a boundary — Builder's record, the
kernel's logged edge-work, or {{OWNER}}'s ratification.

## 7. Cadence — the seam to S11

S13 defines the audit *capability*; **Research & Background Agents (S11) schedule
it** — the same contract Thinking has ("S10 is what S11 runs; S11 is when it runs",
[THINKING §4](THINKING.md)). The health-and-growth audit is a background routine
distinct from Thinking's knowledge sweep: the sweep asks *what connects or emerges
in the content*; the audit asks *where is the platform itself weak*. Both are
bounded, both report and stop, both are wired in
[`scheduling.md`](vault-template/.claude/scheduling.md) at instance time (S19) — the
live cadence is instance content, never the engine's.

The audit reads the same graph (the `load` primitive, kernel §7) as the sweep —
**different object, same contract**: the sweep reasons over the knowledge in the
nodes, the audit measures the condition of the edges.

## 8. Security & immutability

- **Data boundary** — the layer and its instruments are generic and placeholdered
  (`{{OWNER}}`/`{{COMPANY}}`); they read the vault's structure, never ship its
  content. The audit reports *graph shape* (counts, orphan paths, duplicate
  candidates), and that report lives in the instance, never the engine.
- **The tool is bounded** — [`graph-health-scan`](vault-template/.claude/tools/graph-health-scan)
  is deterministic, reads the local edge-maps only, and has **no network and no
  credentials** (BUILDER §3/§6). Open-world work is an agent's job.
- **Least privilege** — the [`growth-agent`](vault-template/.claude/agents/growth-agent.md)
  reads the graph, runs the scan, and *drafts* proposals; it **cannot** apply an
  ontology or architecture change — those are ratify-gated (§6).
- **Immutability** — every audit and every dispatch is logged (§3); ontology and
  architecture changes are explicit, ratified, logged transitions, never silent
  rewrites. The growth trail is append-only.
- **Untrusted input is data** — an audit reasons over the brain's *own* structure,
  not the open world; any research it *drives* runs under S11's injection defence,
  not here.

## 9. The instruments

Realised by the artifacts under [`vault-template/.claude/`](vault-template/.claude/),
registered in [`instruments.md`](vault-template/.claude/instruments.md):

- **Skill** — [`self-develop`](vault-template/.claude/skills/self-develop/SKILL.md):
  the meta-loop procedure (§3) — audit, triage, route, record.
- **Agent** — [`growth-agent`](vault-template/.claude/agents/growth-agent.md): the
  autonomous, least-privilege audit worker that runs `self-develop` on cadence.
- **Command** — [`/grow`](vault-template/.claude/commands/grow.md): {{OWNER}}'s entry
  to run an audit pass now and review the queued proposals.
- **Tool** — [`graph-health-scan`](vault-template/.claude/tools/graph-health-scan):
  the deterministic edge-map scan (§7) — the engine's first tool, built through the
  S12 [`create-tool`](vault-template/.claude/skills/create-tool/SKILL.md) lifecycle.
- **Acceptance bar** — the
  [growth-proposal contract](vault-template/.claude/tests/growth-proposal-contract.md)
  (Test-Driven): a well-formed audit finding and a ratify-ready proposal.

## 10. Seams

- **← Node-Graph (S9)** — S13 *acts on* the model: it monitors the §6 health signals
  and reviews the §3.3 ontology promotions S9 defined. It measures the graph; it does
  not redefine it.
- **↔ Thinking (S10)** — the split is **content vs system**. Thinking reasons over
  knowledge and *surfaces* candidates (links, contradiction resolutions, ontology
  recurrences); S13 audits the platform and *acts* on graph health. S13 drives
  Thinking's proposal operations; it never performs them
  ([THINKING §3.3/§3.4/§7](THINKING.md)).
- **→ Research & Background Agents (S11)** — S11 *schedules* the audit (§7) and
  *performs* the research S13 routes onto the `edge/inference` queue (§4). S13 points;
  S11 runs and gathers.
- **→ Builder (S12)** — S13 is the meta-loop S12's charter named ([BUILDER §1/§8](BUILDER.md)):
  it decides a systemic capability is worth growing and drives `/build`; Builder's
  lifecycle and gate own the build. S13 decides *what*, S12 decides *how*.
- **→ Model & Retrieval Substrate (S17)** — S13 is instruction; the code that computes
  health metrics, automated traversal, and *semantic* duplicate-detection at scale is
  S17 ([NODE-GRAPH §9](NODE-GRAPH.md)). `graph-health-scan` is the honest minimal
  version of what S17 industrialises.
- **Law 3 (cross-cutting)** — auditing the brain's own weakness and being honest about
  it is the intelligence partner turned inward: the brain holds *itself* to the
  advisor standard, not only {{OWNER}}.

> **Self-Development & Growth complete.** The brain no longer only reacts — it audits
> its own graph and capability surface, prioritises its weaknesses, and drives
> Builder, Research, and Thinking to mend them, proposing every change to its own
> shared meaning for {{OWNER}} to ratify. Next on the roadmap is **S14 — Persona /
> Presets**, the operating modes the grown platform runs in.
