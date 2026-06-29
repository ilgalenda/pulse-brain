---
name: create-command
description: Create a new brain command the right way. Use when adding an {{OWNER}}-facing entry point ("create a command", "add a slash command", "I want to trigger X with /…"). Wraps the global `create` skill, enforces instrument conventions, then registers and audits the result. An executor of the Builder layer (see BUILDER.md).
---

# create-command — the brain's command builder

An executor of the **Builder layer** ([`BUILDER.md`](../../../../BUILDER.md), the
authority for the build lifecycle §4 and conventions §6) specialised for
**commands**. A thin **wrapper over the global `create` skill** for {{OWNER}}'s
manual entry points. A command is a routable trigger that hands work to a skill or
agent — it holds the *invocation*, not the procedure.

## When to use

When {{OWNER}} should be able to trigger a capability by name (`/research`,
`/monitor`, `/sweep`). Check [`instruments.md`](../../instruments.md) first.

## Procedure

Run the Builder lifecycle ([BUILDER.md §4](../../../../BUILDER.md)): reuse-or-build
check ([`instruments.md`](../../instruments.md) first; confirm the name does not
clash with a Claude Code built-in) → scaffold via the global `create` skill →
enforce the shared conventions ([`instruments.md`](../../instruments.md) §1 and
[BUILDER.md §6](../../../../BUILDER.md)) → register a row in the **Commands** table →
audit. Command-specific enforcement:

- **Placement** `.claude/commands/<kebab-name>.md`.
- **Frontmatter** one-line `description` and an `argument-hint` if it takes input.
- **Thin / routes, does not implement** (Agent-First) — the command **routes** to a
  skill or agent and holds the *invocation*, not the procedure (e.g. `/research`
  routes to the `research` skill / `research-agent`).

Then **audit** with [`agent-architecture-audit`](../agent-architecture-audit/SKILL.md)
if the command carries any logic; clear every Critical/High finding before trusting it.

## Output

A registered, thin, convention-compliant command, its `instruments.md` row, and
(if applicable) the audit result.
