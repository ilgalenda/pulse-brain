---
description: Wake the brain. Paint the boot banner, load brain state, greet {{OWNER}}, and report where they left off. The Interface boot/entry surface.
argument-hint: "[preset, optional; wake straight into a lens, e.g. ai-orchestrator]"
---

Wake Pulse. This is the brain's deliberate boot: it is summoned, not assumed
(Interface layer, [`INTERFACE.md`](../../../INTERFACE.md) §2). Compose the kernel's
`load`; add nothing.

Steps:

1. **Paint the banner, byte-exact.** Run `cat .claude/pulse-banner.txt` so the art
   renders exactly as shipped; do not retype or redraw it.
2. **Wake the brain.** Run read-routing ([OPERATIONS-KERNEL §7](../../../OPERATIONS-KERNEL.md)):
   read `memory/core.md` (the `active_preset`, `## Current focus`, `## Needs review`)
   and `index.md` (orientation). This is the session-start read, made explicit.
3. **Report state.** Directly beneath the banner (which already ends with a rule),
   print the status block, then close with a matching rule
   (`════════════════════════════════════════════════`):

   ```
     preset  ·  <active_preset, or "none">
     focus   ·  <one line from ## Current focus, or "—">
     review  ·  <N items flagged in ## Needs review, or "clear">
     last    ·  <relative time of the newest log.md entry, e.g. "updated 2h ago">
   ```

4. **Stand ready** in that loaded context, taking no further action until {{OWNER}} asks.

If an argument is given, treat it as a preset name: set it as the active lens via
[`/preset`](preset.md) (the kernel's `update-memory`) before reporting state, so the
`preset` line reflects the wake-into lens.

Keep it to the banner plus status: `/pulse` orients, it does not start working.
