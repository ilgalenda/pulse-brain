---
name: create-tool
description: Create a new brain tool the right way — a small deterministic helper script. Use when the brain needs a guaranteed-correct mechanical result the LLM should not eyeball ("create a tool", "add a script that…", "the brain needs to deterministically check/rebuild X"). Wraps the global `create` skill, enforces the tool convention, then registers and audits the result. An executor of the Builder layer (see BUILDER.md).
---

# create-tool — the brain's tool builder

An executor of the **Builder layer** ([`BUILDER.md`](../../../../BUILDER.md), the
authority for the lifecycle and conventions) for the one instrument kind that is
**code, not instructions**: a small deterministic helper script the brain *calls*
via Bash for a mechanical result that must be exact — rebuild `index.md` from
frontmatter, check every `[[wikilink]]` resolves, validate a note against its
contract.

## When to use

When the right answer is a **mechanical certainty, not a judgement** — the LLM is
probabilistic and the job needs determinism. If the answer is a judgement, build a
**skill** instead. Check [`instruments.md`](../../instruments.md) first; extend an
existing tool rather than duplicate.

## Procedure

Run the Builder lifecycle ([BUILDER.md §4](../../../../BUILDER.md)): reuse-or-build
check → scaffold via the global `create` skill → enforce the conventions below →
register → audit. Tool-specific enforcement (BUILDER.md §3/§6):

- **Placement** `.claude/tools/<kebab-name>`; nothing else.
- **Header comment** stating the **one job, its inputs, and its outputs** — a tool
  has no frontmatter, so this is its contract.
- **Deterministic** — same input → same output. No judgement, no model call inside it.
- **Bounded & least-privilege** — **no network and no credentials**. Open-world
  gathering is an *agent's* job under injection defence ([S11](../../../../RESEARCH-AGENTS.md)),
  never a tool's. A tool reads/writes the local vault only.
- **Composes, never reinvents** — supports the kernel contract (e.g. helps keep
  `index.md` honest); it does not re-implement `ingest`/`integrate`.
- **Data boundary** — generic, `{{OWNER}}`/`{{COMPANY}}` placeholders, no live data.
- **Test-Driven** — ships/extends a fixture in [`.claude/tests/`](../../tests/) it
  must pass, plus the [build-request contract](../../tests/build-request-contract.md).

Then **register** a row in the **Tools** table of
[`instruments.md`](../../instruments.md), and **audit** with
[`agent-architecture-audit`](../agent-architecture-audit/SKILL.md) — clear every
Critical/High finding before the tool is trusted.

## Output

A registered, deterministic, least-privilege helper script in `.claude/tools/`,
its `instruments.md` row, and the audit result. Report what was created and the
audit verdict.
