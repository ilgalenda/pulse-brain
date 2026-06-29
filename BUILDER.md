# Pulse_Brain — Builder

Brain-OS **layer 5**: the brain's **reactive self-extension**. When a task needs a
capability that does not exist, this layer creates a new **instrument** — a skill,
agent, command, or tool — to solve *that* problem, built to the engine's
standards, registered, and audited for reuse. Where Thinking reasons over the
graph and Research gathers into it, Builder grows *the brain's own capability
surface*: it is how Pulse turns the director's "create one to standard
rather than forcing a poor fit" into a disciplined, repeatable act.

This layer is **instruction that produces instruments** in the Brain-OS sense
([BRAIN-OS §"instruction vs code"](BRAIN-OS.md)): the lifecycle is markdown the
LLM follows, and what it produces *may itself be code* (a tool). S11 shipped a
**seed** — three `create-*` wrappers, the `instruments.md` registry, and the
`agent-architecture-audit` QA. This document is the **authority for the layer**;
those seeds, generalised here, are its executors.

## 1. What this layer is — reactive, not the meta-loop

Builder is **reactive**: it answers a *present* need with *one* instrument. It does
not decide *when* or *what* the brain should grow on its own — that is the
**Self-Development & Growth** meta-loop ([S13](BRAIN-OS.md)), which audits the
brain for gaps and *drives* Builder, Research, and Thinking toward system-wide
growth. The line is sharp:

- **Builder (S12):** "this task needs a capability that isn't here — build it now."
- **Self-Development (S13):** "the brain is weak *here* — Builder, go build."

S12 is the *hands*; S13 is the *judgement that points them*. Keeping them separate
means the act of building is identical whether {{OWNER}} asks or the meta-loop
asks — one lifecycle, two callers.

## 2. Lanes — what this layer owns, and what it doesn't

- **Owns** on-demand instrument creation: the build lifecycle (§4), the four
  instrument kinds (§3), the reuse-or-build decision, and registration.
- **Wraps** the global `create` skill for scaffolding — it does not hand-roll
  instrument structure (reuse over reinvention).
- **Composes** the kernel **capability contract**
  ([OPERATIONS-KERNEL §12](OPERATIONS-KERNEL.md)) — a built instrument calls
  `ingest`/`integrate`/`load`/`flag`/`update-*`; Builder **adds no new primitive**.
- **Invokes** `agent-architecture-audit` as the QA gate — it does not define the
  audit.
- **Inherits** the instrument conventions from [`instruments.md`](vault-template/.claude/instruments.md)
  §1 and the five principles from [`PRINCIPLES.md`](PRINCIPLES.md).
- **Does not** own the meta-loop (S13), the kernel contract (composes it), the page
  editorial standard (Context Engine), the graph model (S9), or the heavy code
  substrate — MCP hosting and embeddings/ML are **S17/S18**, not Builder.

## 3. The four instrument kinds

The brain extends itself in exactly four shapes, split on **instruction vs code**:

| Kind | What it is | Instruction or code | Placement |
|---|---|---|---|
| **Skill** | A *procedure* the LLM reads and follows | Instruction | `.claude/skills/<name>/SKILL.md` |
| **Agent** | An autonomous *worker* — own context + least-privilege tools — that runs skills | Instruction | `.claude/agents/<name>.md` |
| **Command** | An {{OWNER}}-facing slash *entry point* | Instruction | `.claude/commands/<name>.md` |
| **Tool** | A small **deterministic helper script** the brain *calls* for a guaranteed-correct mechanical result | **Code** | `.claude/tools/<name>` |

The first three are the brain's instruction surface. **A tool is the one kind that
is code** — it exists because the LLM is probabilistic and some jobs must be
*exact*: rebuild `index.md` from frontmatter, check every `[[wikilink]]` resolves,
validate a note against its contract. The dividing line: if the right answer is a
judgement, it is a skill; if it is a mechanical certainty, it is a tool. This is
the kernel's "optional small determinism helpers" made a first-class kind — the
fourth kind named in BRAIN-OS §5, built through Builder *against* the kernel
contract ([OPERATIONS-KERNEL §12](OPERATIONS-KERNEL.md)), which owns
`update-index`/`update-log`; the tool composes them, never reinvents them. A tool
is **bounded**:
one mechanical job, deterministic, **no network and no credentials** — open-world
gathering is an *agent's* job under injection defence (§6, [S11](RESEARCH-AGENTS.md)).

## 4. The build lifecycle

Every build — whichever kind, whoever the caller — runs the same disciplined cycle.
The `create-*` seeds are this lifecycle specialised per kind:

```
detect gap  →  reuse-or-build?  →  choose kind  →  scaffold (global `create`)  →
enforce conventions  →  register  →  audit  →  trust
```

- **Detect gap** — a task needs a capability no instrument provides (§5).
- **Reuse-or-build** — read [`instruments.md`](vault-template/.claude/instruments.md)
  **first**. If an instrument covers the job, use it; if a near one exists, **extend
  it** rather than create a duplicate. A new instrument is the *exception*, justified.
- **Choose kind** — skill / agent / command / tool, by the §3 split.
- **Scaffold** — delegate file generation to the global `create` skill; never
  hand-roll structure.
- **Enforce conventions** — apply [`instruments.md`](vault-template/.claude/instruments.md)
  §1 to the result: placement · naming · frontmatter · kernel-framing · the five
  principles · the data boundary (§6).
- **Register** — add a row to the correct table in `instruments.md` (name · lane ·
  one-line purpose), so the brain knows what it can now do.
- **Audit** — run [`agent-architecture-audit`](vault-template/.claude/skills/agent-architecture-audit/SKILL.md);
  resolve every Critical/High finding **before** the instrument is trusted.
- **Trust** — only a registered, audited, convention-clean instrument is live.

The acceptance bar for the whole cycle is the
[build-request contract](vault-template/.claude/tests/build-request-contract.md)
(Test-Driven): it gates both a well-formed *request* and a compliant *instrument*.

## 5. The reactive trigger & the dual-role gate

The trigger is **gap-detection**: mid-task, the mind (Claude) finds that no
instrument fits and that forcing an existing one would be a poor fit. Per the
project director, the right move is to **create one to standard** — but not
silently. The dual role governs it (project `.claude/CLAUDE.md`):

- **Claude detects** the capability gap while working and names it as a **Pulse
  decision** (project `.claude/CLAUDE.md`) — the gap, why no existing instrument
  fits, and the kind it would build.
- **Pulse decides** whether to build. **Build-then-record, not ask-then-build:** a
  new instrument is **local, sanitised, and reversible** (a markdown/script file in
  `vault-template/.claude/`), so it is *not* the "consequential outward action" the
  no-silent-execution rule gates — Builder may proceed and **record** rather than
  block for pre-approval. What *is* gated outward (a commit, a push, anything
  beyond the repo) still waits per the project director.
- **The record sink is concrete** — a reactive build is written to
  [`log.md`](OPERATIONS-KERNEL.md) (the append-only audit tier) and flagged in
  `core.md`'s review-flags, so {{OWNER}} reviews it after the fact. Recorded, never
  shipped behind {{OWNER}}'s back.
- **Bounded autonomy** — Builder *scaffolds, registers, stamps, and records*; it
  builds to the conventions (§4/§6) or not at all, and a build that cannot clear
  the audit is not trusted.

Two callers, one gate: an {{OWNER}} request (via `/build`) and the brain's own
reactive detection both run §4 and both pass through this gate — the difference is
only that the reactive path **records to `log.md`** what {{OWNER}} asked for
directly.

## 6. Security & immutability

Builder ships artifacts that land in **every instance** — so the data boundary is
absolute and the discipline is non-negotiable:

- **Data boundary** — every instrument is generic and placeholdered
  (`{{OWNER}}`/`{{COMPANY}}`); **no live data, URLs, feeds, or credentials** ever
  enter an instrument or the repo. Secrets follow the global credential map,
  referenced via `.env`, never hardcoded.
- **Least privilege** — a built agent holds only the tools its job needs, never
  `["*"]`. A built tool is deterministic with **no network and no credentials**.
- **Untrusted input is data** — any instrument that reads the open world defends
  against injection ([the red-team fixture](vault-template/.claude/tests/injection-redteam.md)
  is the bar); Builder never produces one that treats fetched content as instructions.
- **Immutability** — the registry grows by **appended rows**; a superseded
  instrument is replaced by an explicit, recorded transition, not a silent rewrite.
  The audit verdict and a reactive build decision are logged.

## 7. The instruments

This layer is realised by the artifacts under
[`vault-template/.claude/`](vault-template/.claude/), registered in
[`instruments.md`](vault-template/.claude/instruments.md):

- **Skills (the per-kind executors of §4)** — `create-skill`, `create-agent`,
  `create-command`, `create-tool`: each specialises the build lifecycle for its
  kind, wrapping the global `create` and enforcing the kind-specific conventions.
- **Command** — `/build [what the brain should be able to do]`: {{OWNER}}'s unified
  entry. It runs the lifecycle — reuse-or-build check, infer the kind, route to the
  matching `create-*` — and reports what was created and the audit result. It is
  also the entry the reactive trigger (§5) composes.
- **QA** — `agent-architecture-audit` (shipped S11): the gate every build clears.
- **Acceptance bar** — the [build-request contract](vault-template/.claude/tests/build-request-contract.md).

## 8. Seams

- **← Builder seed (S11)** — the three `create-*` skills, the registry, and the
  audit shipped as a seed; this layer generalises them into the lifecycle (§4) they
  now compose, and adds the fourth kind (`create-tool`) and the unified `/build`.
- **→ Operations Kernel** — a built instrument composes the capability contract;
  Builder adds no primitive.
- **→ `agent-architecture-audit`** — the QA gate (§4); no build is trusted until it
  clears Critical/High.
- **↕ Research & Background Agents (S11)** — a new worker (research/monitor or
  beyond) is created *through* this layer, against the same pattern; S11 established
  the seed, S12 generalises it.
- **→ Self-Development & Growth (S13)** — S13 *drives* Builder on graph-health and
  gap signals; it decides when and what to grow, Builder builds it. S12 does not own
  that meta-loop.

> **Builder complete.** The brain now extends itself on demand — one lifecycle,
> four kinds, a unified entry, the reuse-first discipline, and a register-and-audit
> gate — whether {{OWNER}} asks or the brain detects the gap itself. Next on the
> roadmap is **S13 — Self-Development & Growth**, the meta-loop that decides *when*
> to point Builder, Research, and Thinking at the brain's own weaknesses.
