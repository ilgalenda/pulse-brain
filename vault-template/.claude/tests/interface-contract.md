# Fixture — the interface contract

The acceptance checklist the **Interface layer**
([`INTERFACE.md`](../../../INTERFACE.md)) must pass for its realised surface — the
boot/entry command [`/pulse`](../commands/pulse.md). It has two halves: **Part A** —
the boot artifacts are well-formed (banner byte-exact, generic, placeholdered);
**Part B** — `/pulse` boots correctly (paints the banner, wakes the brain via the
kernel's read-routing, reports state, composes `load` without a new primitive). This
restates INTERFACE §2 as a *test*, not a new authority. If any item fails, the surface
is not yet correct.

## Part A — the boot artifacts are well-formed

- [ ] **Byte-exact banner** — the art lives in
      [`pulse-banner.txt`](../pulse-banner.txt) and the command paints it via `cat`,
      not by retyping; the wordmark renders identically every boot.
- [ ] **Generic and placeholdered** — the greeting is `Hi {{OWNER}}` (filled at
      instantiation, S19); no real name, account, or live data anywhere in the banner
      or command.
- [ ] **Well-formed command frontmatter** — a clear, routable `description` and an
      `argument-hint` for the optional preset; kebab-case name (`pulse`).
- [ ] **Composes, does not reinvent** — the command frames itself against the kernel's
      `load` ([OPERATIONS-KERNEL §7](../../../OPERATIONS-KERNEL.md)); it declares **no
      new primitive**.

## Part B — `/pulse` boots correctly

- [ ] **Paints then wakes** — it `cat`s the banner, then runs read-routing
      ([kernel §7](../../../OPERATIONS-KERNEL.md)): reads `memory/core.md` and
      `index.md`. The banner is presentation; the status is read-routing surfaced.
- [ ] **Reports true state** — the status block reflects the *actual* loaded state:
      `preset` = the `active_preset` anchor (or "none"); `focus` = a line from
      `## Current focus` (or "—"); `review` = the count in `## Needs review` (or
      "clear"); `last` = the newest `log.md` entry, relatively. It does not invent
      state the brain does not hold.
- [ ] **Summoned, not assumed** — `/pulse` is an explicit command; the brain is not
      auto-booted on every CLI session by a hook (INTERFACE §2 — opening a terminal is
      not using the brain).
- [ ] **Wake-into-lens (optional arg)** — given a preset name, it sets the active lens
      via [`/preset`](../commands/preset.md) (`update-memory`) before reporting, so the
      `preset` line reflects it; it does not change knowledge or identity.
- [ ] **Orients, does not work** — it stands ready in loaded context and stops; it does
      not start integrating, researching, or building off the back of the boot.

## Part C — an outbound deliverable meets the house standard

A briefing, report, or exported document the brain produces satisfies (INTERFACE §5):

- [ ] **British English, genuine voice** — it reads as {{OWNER}}'s own hand, not generic
      machine prose.
- [ ] **No machine tells** — no em-dash used as a connective tic, no ideas padded into
      tidy triplets, no templated scaffolding or filler.
- [ ] **Judgement leads (briefings)** — it opens with what matters and what to decide or
      do, ahead of any background, to a Prime-Minister/CEO standard.
- [ ] **Sourced** — claims trace to the canon and the sources they were compiled from;
      provenance is visible and can be challenged.
- [ ] **Voice-calibrated** — it mirrors `memory/owner-voice.md` when a sample is present,
      and falls back to the §5 defaults *and says so* when it is absent.

## Worked PASS example

> {{OWNER}} runs `/pulse` on a fresh session. The command `cat`s the banner (PULSE
> wordmark + block brain + `· intelligence ·` + `Hi {{OWNER}}`, the placeholder filled
> to the owner's name at instantiation), reads `core.md` and `index.md`, and prints:
>
> ```
>   preset  ·  ai-orchestrator
>   focus   ·  S16 Interface — boot surface
>   review  ·  2 items flagged
>   last    ·  updated 3h ago
> ════════════════════════════════════════════════
> ```
>
> Then it stops, ready. `/pulse gtm-lead` would first set the GTM lens via `/preset`,
> so the `preset` line reads `gtm-lead`.

## FAIL examples the surface must NOT produce

- **Retyped banner** — redrawing the wordmark inline instead of `cat`-ing the asset,
  risking a mangled, drifting logo.
- **Invented status** — reporting a focus, preset, or review count the brain does not
  actually hold in `core.md` (status must be read, not imagined).
- **Auto-boot** — wiring `/pulse`'s behaviour into a `SessionStart` hook that fires on
  every terminal session; the brain is summoned, not assumed.
- **Working off the boot** — starting to integrate sources, run research, or build
  after waking, instead of orienting and standing ready.
- **A new primitive** — introducing machinery instead of composing `load` and
  `update-memory`.
- **Live data in the artifacts** — a real name or account baked into the banner or
  command instead of the `{{OWNER}}` placeholder.
- **Machine tells in a deliverable** — em-dash connectors, rule-of-three padding,
  throat-clearing openers, or filler in a briefing or report.
- **An unsourced briefing** — claims presented with no trace back to canon or sources.
- **Ignoring the owner's voice** — generic prose when `owner-voice.md` holds a sample to
  mirror, or failing to flag the fallback when it is empty.
