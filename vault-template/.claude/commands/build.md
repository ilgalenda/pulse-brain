---
description: Build a new brain instrument on demand — infer the kind (skill/agent/command/tool), run the Builder lifecycle, register and audit it.
argument-hint: [what the brain should be able to do]
---

Run the **Builder layer** ([`BUILDER.md`](../../../BUILDER.md)) for a capability
the brain is missing. This command is {{OWNER}}'s unified entry; it is also the
entry the brain's reactive gap-detection composes (BUILDER.md §5).

Do **not** implement the lifecycle here — route to the per-kind executor.

1. **Reuse-or-build** — read [`instruments.md`](../instruments.md) first. If an
   instrument already covers `$ARGUMENTS`, use or extend it and stop; a new one is
   the exception (BUILDER.md §4).
2. **Choose the kind** (BUILDER.md §3): a procedure → **skill**; an autonomous
   worker → **agent**; an {{OWNER}}-facing trigger → **command**; a deterministic
   mechanical helper → **tool**. If unclear, ask one focused question.
3. **Route** to the matching executor — [`create-skill`](../skills/create-skill/SKILL.md)
   · [`create-agent`](../skills/create-agent/SKILL.md) ·
   [`create-command`](../skills/create-command/SKILL.md) ·
   [`create-tool`](../skills/create-tool/SKILL.md) — which scaffolds, enforces
   conventions, registers, and audits.
4. **Surface it as a Pulse decision** — name the gap, kind, and reason. A
   **reactive** build (the brain's own, not this explicit `/build`) is also
   **recorded to `log.md` and flagged in `core.md` review-flags** (BUILDER.md §5),
   never shipped silently.

Report back: the gap, the kind chosen and why, the instrument created, its
`instruments.md` row, and the audit verdict.
