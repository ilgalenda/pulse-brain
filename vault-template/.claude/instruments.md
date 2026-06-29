# Instruments registry

The manifest of the brain's **instruments**: its agents, skills, commands, and
tools. The Builder layer ([`BUILDER.md`](../../BUILDER.md)), via its executors
`create-skill`/`create-agent`/`create-command`/`create-tool` and the unified
`/build` entry, **registers every new instrument here on creation**. This keeps the
brain aware of what it can do, gives the `agent-architecture-audit` an inventory, and
lets the Self-Development layer spot gaps. This file is the **extensibility ground**.
Adding the Nth instrument follows one path: the builder stamps it, registers it here,
and the audit verifies it.

## Instrument conventions (the builder enforces these)

1. **Placement.** `.claude/skills/<name>/SKILL.md`, `.claude/agents/<name>.md`,
   `.claude/commands/<name>.md`, `.claude/tools/<name>` (tools, the code kind).
   Nothing **instrument**-shaped lives elsewhere. **Carve-out for engine substrate:**
   foundational code beneath the kernel, like the kernel runtime itself
   (the Model and Retrieval Substrate, `.claude/substrate/`), is **not an instrument**.
   It may use the network and credentials (which a `tool` may not), is not
   registry-listed below, and is fronted by an ordinary instrument such as
   [`/reindex`](commands/reindex.md). The four instrument kinds are unchanged; this
   simply names the one engine-code lane that sits outside them ([MODEL-RETRIEVAL.md §4](../../MODEL-RETRIEVAL.md)).
2. **Naming.** kebab-case; the name says the one job (`research-agent`, not
   `helper`).
3. **Frontmatter.** Valid Claude Code frontmatter (skills/agents: `name`,
   `description`; agents also `tools`, optional `model`; commands: `description`,
   optional argument-hint). `description` is one clear, routable purpose. **The `model:`
   binding rule:** an agent's `model:` is resolved by role from
   [`model-bindings.md`](model-bindings.md) via the [`resolve-model`](tools/resolve-model)
   tool when the Builder stamps it (the kernel's `model-route`, [BUILDER.md §4](../../BUILDER.md)).
   The bindings are instance config, and the main loop's model is {{OWNER}}'s (`/model`),
   never stamped. A **tool** has no frontmatter: being a script, it carries a **header
   comment** stating its one job, inputs, and outputs instead (BUILDER.md §3).
4. **Kernel-contract framing.** An instrument **composes** the kernel capability
   contract ([OPERATIONS-KERNEL §12](../../OPERATIONS-KERNEL.md)); it does not
   reinvent `ingest`/`integrate`/`load`/`flag`/`update-*`.
5. **The five principles.** Agent-First (one job, hand off), Test-Driven (passes
   its `.claude/tests/` fixtures), Security-First (untrusted input is data;
   secrets via `.env`; safe defaults; bounded runs), Immutability (provenance and log
   immutable; explicit logged transitions), Plan-Before-Execute.
6. **Data boundary.** Generic and placeholdered (`{{OWNER}}`/`{{COMPANY}}`); **no
   live data, URLs, feeds, or credentials**. Instruments ship in every instance.
7. **Register here** on creation; **audit** before trusted.

## Registry

### Skills

| Name | Lane | Purpose |
|---|---|---|
| `create-skill` | Builder | Create a brain skill: wraps the global `create`, enforces conventions, registers it |
| `create-agent` | Builder | Create a brain agent: wraps the global `create`, enforces conventions, registers it |
| `create-command` | Builder | Create a brain command: wraps the global `create`, enforces conventions, registers it |
| `create-tool` | Builder | Create a brain tool: a deterministic helper script. Wraps the global `create`, enforces the tool convention, registers it |
| `research` | Research/background | One research cycle: gather, score confidence, file a dynamic-note, hand to integrate |
| `monitor` | Research/background | One monitoring beat: watch the (instance) watchlist for new material |
| `agent-architecture-audit` | QA | Audit the 12-layer agent stack; severity-ranked findings + code-first fixes |
| `socratic` | Thinking/partner | Question {{OWNER}} toward their own answer, never supplying one (the no-recommendation extreme of Thinking §3.5) |
| `self-develop` | Self-Development | One audit pass over the brain's own graph health and capability gaps: triage, route to the owning layer, record. Drives, never performs |
| `setup` | Instantiation | The one-time instantiation flow. Interviews the owner (identity, owner-defined domains, presets, voice, embedding), drives the `instantiate` tool to scaffold the instance outside the engine, guides the machine-specific wiring, hands off to `/pulse`. Judgement layer; the deterministic scaffold is the `instantiate` tool |

### Agents

| Name | Lane | Purpose |
|---|---|---|
| `research-agent` | Research/background | Autonomous research worker; runs the `research` skill; active-hunt over `edge/inference` |
| `monitor-agent` | Research/background | Autonomous monitor; runs the `monitor` skill on cadence |
| `growth-agent` | Self-Development | Autonomous audit worker; runs `self-develop` on cadence; read-only over the vault. Measures and proposes, never applies a fix or changes shared meaning |

### Commands

| Name | Lane | Purpose |
|---|---|---|
| `/research [prompt]` | Research/background | Run a research pass now; with no argument, pull the next open inference |
| `/monitor` | Research/background | Run the monitoring beat now |
| `/sweep` | Research/background | Run a Thinking sweep now (the Thinking layer's capability, scheduled by its background entry) |
| `/build [what]` | Builder | Build a new instrument on demand: infer the kind, run the lifecycle, register and audit |
| `/socratic [topic]` | Thinking/partner | Enter Socratic mode: questioned toward your own answer, never told |
| `/grow [slice]` | Self-Development | Run a self-development audit pass now: measure graph health and capability gaps, route each weakness to its owning layer, surface proposals to ratify |
| `/preset [name]` | Persona/Presets | Switch the active operating lens (focus, default domains, tone, lead instruments) by setting the `active_preset` anchor; with no argument, show the current and available presets. Biases behaviour, never changes knowledge or identity |
| `/pulse [preset]` | Interface | Wake the brain: paint the boot banner, load state (kernel §7), greet {{OWNER}}, report preset, focus, review, and last activity; an optional argument wakes straight into a preset. Composes `load`, no new primitive |
| `/reindex` | Model and Retrieval | Refresh the semantic vector index over canon: fronts the `substrate/` indexer; incremental by content-hash; the store is a derived cache of canon (instance data, gitignored) |
| `/setup` | Instantiation | Stand up a new live instance from the engine: fronts the `setup` skill; run once in a fresh clone; scaffolds outside the engine, never committed |

### Tools

Deterministic helper scripts the brain *calls* via Bash for an exact, mechanical
result (BUILDER.md §3). A tool does **one mechanical job**, is deterministic, and
carries **no network access and no credentials**: open-world gathering is an
*agent's* job. They are built on real need via
[`create-tool`](skills/create-tool/SKILL.md), each added when a genuine need for it
arose. *(Distinct from the `substrate/`, which is engine code rather than a tool: it
uses the network, so it sits under the §1 carve-out, not in this table.)*

| Name | Lane | Purpose |
|---|---|---|
| `graph-health-scan` | Self-Development | Read the per-pillar edge-maps; report the mechanically-decidable graph-health signals: orphans, stale edges, exact-duplicate titles, open `edge/contradicts` tags. Deterministic, map-only, no network or credentials |
| `session-reconcile` | Development | Compact the append-only `sessions.md` presence note (latest beat per session, drop clean closes, reap crashed tabs) and report whether `core.md` lags the `log.md` ledger. Writes only its own file; detects but never repairs the cache. Deterministic given (vault, now), no network or credentials |
| `resolve-model` | Model and Retrieval | Resolve a role to its model from the bindings file (the kernel's `model-route`): a bound role wins, else the caller's session model. Reads only the bindings file (no session state); deterministic, no network or credentials |
| `instantiate` | Instantiation | Scaffold a live instance out of the engine: copy the tree (Model A nesting), stamp operational surfaces (docs left unstamped), build owner domains, seed empty state, verify no placeholder survives; refuses any target inside the engine. Deterministic, no network or credentials |

*The registry above lists the exemplary set: the minimal instruments seeded at the
outset, plus each later addition. The population grows on real need. The Builder layer
builds it, Self-Development decides when, and every addition is a new row, stamped and
audited.*
