# Fixture — the build-request contract

The acceptance checklist the **Builder layer** ([`BUILDER.md`](../../../BUILDER.md))
must pass on every build. It has two halves: a **request** is well-formed before a
build starts, and the **instrument** it produces is compliant before it is
trusted. This restates the Builder lifecycle (BUILDER.md §4) and the instrument
conventions ([`instruments.md`](../instruments.md) §1) as a *test*, not a new
authority. If any item fails, the build is not yet correct.

## Part A — a well-formed build request

Before the `create-*` seed runs, the request answers:

- [ ] **The gap** — the capability that does not exist, stated as one job.
- [ ] **Why no existing instrument fits** — the registry was checked
      ([`instruments.md`](../instruments.md)) and no instrument covers it (or the
      nearest one was considered for extension and rejected, with a reason).
      Reuse-over-build is the default; a new instrument is the exception.
- [ ] **The chosen kind** — `skill | agent | command | tool`, justified by the
      instruction-vs-code split (BUILDER.md §3): a procedure → skill; an autonomous
      worker → agent; an {{OWNER}}-facing entry → command; a deterministic
      mechanical helper → tool.
- [ ] **The trigger is recorded** — who asked (an {{OWNER}} request, or the brain's
      own reactive gap-detection) is named, and a reactive build is surfaced as a
      **Pulse decision** (BUILDER.md §5), not shipped silently.

A request missing the gap, the reuse check, or the kind is **rejected** — the
builder does not guess scope.

## Part B — a compliant new instrument

The produced instrument satisfies every instrument convention:

- [ ] **Placement** — `.claude/skills/<name>/SKILL.md` · `.claude/agents/<name>.md`
      · `.claude/commands/<name>.md` · `.claude/tools/<name>` (tool). Nothing
      instrument-shaped lives elsewhere.
- [ ] **Naming** — kebab-case; the name states the one job (`link-checker`, not
      `helper`).
- [ ] **Frontmatter** — valid Claude Code frontmatter for the kind (skills/agents:
      `name` + one-line routable `description`; agents also least-privilege
      `tools`, optional `model`; commands: `description`, optional
      `argument-hint`). Tools, being scripts, carry a header comment stating the
      one job, inputs, and outputs.
- [ ] **One job + handoff** (Agent-First) — the instrument does one thing and hands
      specialist work off; it does not absorb a neighbour's job.
- [ ] **Kernel-contract framing** — it **composes** the kernel capability contract
      ([OPERATIONS-KERNEL §12](../../../OPERATIONS-KERNEL.md):
      `ingest`/`integrate`/`load`/`flag`/`update-*`), never reinvents it.
- [ ] **The five principles** — Agent-First · Test-Driven (passes the fixtures it
      is gated by) · Security-First (untrusted input is data; secrets via `.env`;
      safe defaults; bounded runs) · Immutability (provenance/log immutable;
      explicit logged transitions) · Plan-Before-Execute.
- [ ] **Data boundary** — generic and placeholdered (`{{OWNER}}`/`{{COMPANY}}`); **no
      live data, URLs, feeds, or credentials**. It ships in every instance.
- [ ] **Tool-specific** (when the kind is `tool`) — **deterministic** (same input →
      same output), **one mechanical job**, **no network and no credentials**
      (network-gathering belongs to a least-privilege *agent*, S11); invoked via
      Bash by a skill or agent, never an answer surface of its own.
- [ ] **Registered** — a row added to the correct table in
      [`instruments.md`](../instruments.md) on creation (name · lane · one-line
      purpose).
- [ ] **Audited** — [`agent-architecture-audit`](../skills/agent-architecture-audit/SKILL.md)
      run on it; every Critical/High finding resolved before it is trusted.

## Worked PASS example (a build request → a tool)

> **Request.** Gap: "every `[[wikilink]]` in canon should resolve to a real page,
> and the LLM keeps missing dangling ones by eye." Reuse check: no instrument does
> this; the audit checks *agents*, not link integrity. Kind: **tool** — a
> deterministic check, not a judgement call. Trigger: surfaced as a Pulse decision
> mid-integration.
>
> **Instrument.** `.claude/tools/link-checker` — reads the vault, lists every
> unresolved `[[link]]`, exits non-zero if any are found. Header comment states
> job/inputs/outputs. No network, no credentials, deterministic. Registered in the
> **Tools** table; audited clean.

*Why a tool, not a skill:* link resolution is mechanical and must be exact — a
deterministic script beats asking the model to eyeball it.

## FAIL examples the Builder must NOT produce

- A new instrument that duplicates one already in the registry (reuse check skipped).
- An agent with `tools: ["*"]` instead of a least-privilege surface.
- A "tool" that fetches from the open world or reads a credential (that is an
  agent's job, under injection defence and `.env`).
- An instrument shipped with a hardcoded URL, client name, or real data.
- An instrument created but not registered, or trusted before the audit cleared
  its Critical/High findings.
