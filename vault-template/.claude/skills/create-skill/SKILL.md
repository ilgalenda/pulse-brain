---
name: create-skill
description: Create a new brain skill the right way. Use when adding a skill to the brain ("create a skill", "add a skill", "the brain needs a skill that…"). Wraps the global `create` skill and enforces the brain's instrument conventions, then registers the result. An executor of the Builder layer (see BUILDER.md).
---

# create-skill: the brain's skill builder

An executor of the **Builder layer** ([`BUILDER.md`](../../../../BUILDER.md), the
authority for the build lifecycle §4 and conventions §6), specialised for **skills**,
that is, a procedure invoked by a command or an agent. It is a thin **wrapper over the global
`create` skill** that adds the brain's conventions and bookkeeping, so every skill
the brain grows is consistent, audited, and registered. Reuse over reinvention: the
global `create` does the scaffolding; this skill makes it *brain-native*.

## When to use

When the brain needs a new reusable capability (a procedure invoked by a command
or an agent). If an existing instrument fits, use it: do not create a near-duplicate
(check [`instruments.md`](../../instruments.md) first).

## Procedure

Run the Builder lifecycle ([BUILDER.md §4](../../../../BUILDER.md)): reuse-or-build
check ([`instruments.md`](../../instruments.md) first, extending an existing skill
over a near-duplicate) → scaffold via the global `create` skill (never hand-roll
structure) → enforce the shared conventions ([`instruments.md`](../../instruments.md)
§1 and [BUILDER.md §6](../../../../BUILDER.md)) → register a row in the **Skills**
table → audit. Skill-specific enforcement:

- **Placement**: `.claude/skills/<kebab-name>/SKILL.md`.
- **Single job + handoff** (Agent-First): a skill is one procedure. It composes
  the kernel contract (`ingest`/`integrate`/`load`/`flag`/`update-*`) and hands
  specialist work off, never reinventing a primitive.
- **A fixture it must pass** (Test-Driven): name or add the
  [`.claude/tests/`](../../tests/) fixture that gates it, plus the
  [build-request contract](../../tests/build-request-contract.md).

Then **audit** with [`agent-architecture-audit`](../agent-architecture-audit/SKILL.md)
and clear every Critical/High finding before the skill is trusted.

## Output

A registered, convention-compliant `SKILL.md`, plus its `instruments.md` row.
Report what was created and the audit result.
