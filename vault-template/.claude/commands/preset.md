---
description: Switch the brain's active operating preset — the role-shaped lens (focus, default domains, tone, lead instruments) it reads the vault through. With no argument, show the current preset and the available ones.
argument-hint: [preset name, e.g. gtm-lead | ai-orchestrator — omit to show current]
---

Set or show the **active operating preset** (the S14 capability — see
[`PERSONA-PRESETS.md`](../../../PERSONA-PRESETS.md)).

A preset is a **lens, not a store**: it biases focus, default domains, tone, and
which instruments lead, **without changing the knowledge, the identity, or the laws
beneath it** (PERSONA-PRESETS §1/§7).

**With a name (`$ARGUMENTS`):**
1. Resolve it to a preset file in [`presets/`](../../presets/) whose `preset:`
   field matches; if none matches, say plainly **"`<name>` is not a preset"**, then
   show the current preset and the available ones, and stop — do not guess or
   switch.
2. Set **`active_preset`** in [`memory/core.md`](../../memory/core.md) to that
   value — via the kernel's `update-memory` ([OPERATIONS-KERNEL §10/§12](../../../OPERATIONS-KERNEL.md)).
   This is a logged **setting** change, not a knowledge edit — touch no canon page.
3. Apply the lens for the session: lead read-routing with the preset's
   `default_domains` (biased, never exclusive — PERSONA-PRESETS §6), foreground its
   `lead_instruments`, and adopt its `tone` (register and emphasis — still one voice).

**With no argument:** report the current `active_preset` and the available presets
(name · one-line description) from `presets/`. Change nothing.

Discipline (PERSONA-PRESETS §6/§7):
- **Lens, not filter** — `default_domains` *lead*; a task that clearly needs another
  domain still loads it. Never go blind to an off-role matter or a `core.md` flag.
- **One voice** — `tone` colours the single voice to {{OWNER}}; it is not a character.
- **No knowledge change** — switching reconfigures behaviour only; the vault is untouched.

Report back: the preset now active (or shown), the domains it leads with, the
instruments it foregrounds, and that the switch was recorded as a setting change.
