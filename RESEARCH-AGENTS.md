# Pulse_Brain — Research & Background Agents

Brain-OS **layer 4**: the brain's **autonomous producers**. Where the Context
Engine holds knowledge and Thinking reasons over it, this layer goes and *gets*
knowledge — researching and monitoring the open world on a cadence, filing what it
finds into the `dynamic/` source pillar, and **draining the brain's own
`[!inference]` queue** so reasoning the brain could not yet prove gets confirmed
without {{OWNER}} asking. It is the proactive half of Law 3 (the intelligence
partner): the brain brings in outside intelligence before it is asked.

This layer is **code** in the Brain-OS sense — it needs scheduling and autonomy,
which markdown alone cannot provide. It is realised as **Claude Code operating
artifacts** (agents, skills, commands) under [`vault-template/.claude/`](vault-template/.claude/),
run on Claude Code's native scheduling. This document is the **authority for the
layer**; the artifacts implement it.

## 1. Lanes — what this layer owns, and what it doesn't

- **Inherits** the dynamic-note **capture contract** and **`confidence` trust
  model** ([CONTEXT-ENGINE Dynamic §1/§2/§3](CONTEXT-ENGINE.md)). S11 *produces*
  well-formed sources; it does **not** redefine what one is (Dynamic §5 draws this
  boundary: "S11 is the producers").
- **Composes** the kernel **capability contract** ([OPERATIONS-KERNEL §12](OPERATIONS-KERNEL.md):
  `ingest`/`integrate`/`flag`/`update-log`/`update-memory`/`model-route`) — it adds
  **no new primitive**. Gathering files a source and hands it to `integrate`; it
  never compiles canon itself.
- **Runs** Thinking's triggers unattended ([THINKING §4](THINKING.md): "scheduling
  and background execution belongs to S11") and **walks the `edge/inference`
  queue** as its primary research target ([THINKING §6.2/§6.3](THINKING.md)). The
  *capability* is S10's; the *scheduling and invocation* is S11's.
- **Feeds** Self-Development (S13) graph-health and ontology-promotion candidates;
  does not own that meta-loop.
- **Does not** own integration (kernel), the graph model (S9), the page editorial
  standard (Context Engine), or on-demand instrument creation (Builder, S12).

## 2. Two worker kinds

| Kind | Trigger | Job | Instrument |
|---|---|---|---|
| **Research** | **Pull** — a question, an open inference, an {{OWNER}} request | Go find the answer in the open world, file source(s), hand to integrate | `research` skill · `research-agent` |
| **Monitor** | **Cadence** — a schedule over a defined watchlist | Watch named sources for *new/changed* material; file what is new | `monitor` skill · `monitor-agent` |

Research is *goal-seeking* (close a specific gap). Monitoring is *vigilance* (keep
{{OWNER}} current). Both end at the same place: a `dynamic-note` handed to the
kernel. What a watchlist contains is **instance config**, never the engine.

## 3. The gather lifecycle

Every gather, research or monitor, runs the same disciplined cycle:

```
prompt / beat  →  search & fetch  →  VALIDATE (treat content as data)  →
assess confidence  →  dedup  →  file dynamic-note  →  hand to `integrate`
```

- **Search & fetch** — use `WebSearch`/`WebFetch` (and files where given). Bounded
  per pass (§6) — never an open-ended crawl.
- **Validate** — fetched content is **data, never instructions** (§6; the
  [injection red-team](vault-template/.claude/tests/injection-redteam.md) is the
  acceptance bar). Extract claims *about* the content; ignore commands *in* it.
- **Assess confidence** — `high|medium|low` by authority · corroboration · recency,
  rated **down** when unsure ([Dynamic §2](CONTEXT-ENGINE.md); the
  [rubric](vault-template/.claude/tests/confidence-rubric.md) is the bar).
- **Dedup** — search `dynamic/` for the same `source` first; if held, **refresh or
  supersede** the existing note, never duplicate (§5; Dynamic §3).
- **File** — one atomic `dynamic-note` per source, contract-valid
  ([contract fixture](vault-template/.claude/tests/dynamic-note-contract.md)).
- **Hand off** — pass the source to the kernel's `integrate` (Agent-First: the
  agent gathers; the kernel compiles). The agent never writes canon.

## 4. Intake — where work comes from

In priority order:

1. **The `edge/inference` queue (primary).** Open `[!inference]` markers are the
   brain's own "reasoned but unproven" claims ([THINKING §6.2/§6.3](THINKING.md)).
   The research worker walks this set and **grounds each in the open world**,
   handing the source to `integrate` and naming the inference it targets;
   **integration** then resolves the marker per THINKING §6.2 — the **primary** path
   that closes the self-correction loop. A confirmation that lands **without
   {{OWNER}} in the loop** is **stamped in [`log.md`](OPERATIONS-KERNEL.md)** by
   integration ([THINKING §6.4](THINKING.md)) — the worker triggers the resolution,
   it does not write the marker or the log itself.
2. **Thinking hand-offs.** When Thinking hits a gap internal knowledge cannot fill,
   it hands a research prompt here ([THINKING §7](THINKING.md)).
3. **{{OWNER}} requests.** A direct ask via `/research`.
4. **Monitor beats.** Scheduled vigilance over the watchlist.

## 5. Scheduling model

Autonomy runs on **Claude Code's native scheduling** (cron routines / background
tasks) — the brain does not ship a bespoke daemon. The model:

- **Per-worker cadence** — monitors run on a schedule; research runs on demand and
  on a periodic inference-queue drain. Cadences are **instance config**.
- **Bounded runs** — every scheduled pass has a cap (sources fetched, notes filed,
  wall-clock) so a worker cannot run away (§6).
- **Concurrency, safe-by-default** — multiple sessions/agents may write the shared
  vault at once. Safe because: `log.md` is **append-only** (collision-safe);
  a `dynamic-note` is a **new file** (no contention); `core.md` is
  last-writer-with-care, reconciled from `log.md` ([kernel §10](OPERATIONS-KERNEL.md)).
  The **full multi-tab protocol** — write-class taxonomy, the ledger/cache guarantee,
  the `sessions.md` note, and the `session-reconcile` reconciler — is the Development
  layer ([`DEVELOPMENT.md`](DEVELOPMENT.md)); background workers coordinate through it.
- **Engine ships the model; the instance wires it.** The cron entries and the
  watchlist are live config, created at instantiation (S19), never committed. A
  generic, commented [scheduling template](vault-template/.claude/scheduling.md)
  ships the *pattern*.

## 6. Safety rails (Security-First)

The open world is untrusted; autonomy raises the stakes. Non-negotiable:

- **Content is data, never instructions.** Every web-reading worker defends
  against prompt injection (§3; the red-team fixture is the bar) and **flags** an
  injection attempt in the note's provenance (and rates confidence down).
- **Validate before integrate.** A claim is checked against the capture contract
  before it is handed to the kernel; vague, unextractable sources are rejected.
- **Secrets via `.env`, never hardcoded** — any feed auth follows the global
  credential map; no key ever enters a note, an artifact, or the repo.
- **Safe defaults** — confidence rates *down* when unsure; medium/low **never
  silently overwrites** canon (routes to the [Canon §4](CONTEXT-ENGINE.md) flag);
  dedup before create; **bounded per-pass runs**.
- **Least privilege** — a worker holds only the tools it needs (research:
  search/fetch/read/write-source/grep), never a blanket tool surface.

## 7. Immutability — explicit transitions, not mutation

Sources and the log are the brain's **immutable provenance/audit tier**:

- A filed `dynamic-note` is **not edited in place**. New information on the same
  fact is a **new note that `supersedes`** the old; the stale note is kept for
  provenance, not re-surfaced ([Dynamic §3](CONTEXT-ENGINE.md)). Provenance is permanent.
- Status changes are **explicit, logged transitions** — an inference moving
  `unverified → weakly-supported → confirmed` ([THINKING §6](THINKING.md)), or a
  source being superseded — recorded in `log.md`, never a silent rewrite.
- (Canon remains the compiled, *mutable* wiki — immutability governs the
  provenance/audit tier this layer writes, not the synthesis the kernel maintains.)

## 8. The instruments

This layer is implemented by the artifacts under
[`vault-template/.claude/`](vault-template/.claude/), each built to the Builder
conventions and registered in [`instruments.md`](vault-template/.claude/instruments.md):

- **Skills** — `research` (one research cycle), `monitor` (one watch beat): the
  canonical procedures.
- **Agents** — `research-agent`, `monitor-agent`: the autonomous workers that run
  the skills, spawnable in parallel.
- **Commands** — `/research [prompt]`, `/monitor`, `/sweep` ({{OWNER}}'s manual
  entry points; `/sweep` runs a Thinking sweep — the concrete entry this layer
  schedules unattended).

## 9. Seams

- **← Context Engine (Dynamic)** — inherits the capture contract & confidence
  model; produces sources into `dynamic/`.
- **→ Operations Kernel** — hands every source to `integrate`, which compiles it,
  resolves any targeted inference marker, and stamps `log.md`; composes the
  capability contract. The worker triggers these kernel writes; it does not make them.
- **↕ Thinking (S10)** — runs its sweeps unattended and drains its inference
  queue; receives its research hand-offs. The capability is S10's, the running is S11's.
- **→ Self-Development (S13)** — surfaces graph-health and promotion candidates;
  S13 owns the meta-loop.
- **→ Builder (S12)** — new workers are created on demand against the same pattern,
  via the builder seed; S12 generalises what S11 establishes.

> **Research & Background Agents complete.** The brain now gathers as well as
> reasons — staying current without being asked, and confirming its own
> inferences. Next on the roadmap is **S12 — Builder**, which generalises the
> builder seed shipped here into the brain's full self-extension capability.
