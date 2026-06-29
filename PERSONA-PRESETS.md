# Pulse_Brain — Persona / Presets

Brain-OS **layer 7**: selectable **operating presets** for {{OWNER}}'s roles. A
preset is a **lens** the whole stack is read through — it biases *focus, default
domains, tone, and which instruments lead* for one role (GTM Lead, AI Orchestrator,
and others), and switching it reconfigures how the brain *behaves* **without
changing the knowledge, the identity, or the laws beneath it**.

This is an **instruction (config)** layer ([BRAIN-OS instruction-vs-code map](BRAIN-OS.md)):
a preset is a small markdown config file the LLM reads, not code and not a running
process. It introduces **no new kernel primitive** — switching a preset is updating
the **`active_preset`** anchor the kernel already reads ([OPERATIONS-KERNEL §7/§10](OPERATIONS-KERNEL.md)).
It is the formal expression of the project director's *"scoped roles beneath the
director"* ([`.claude/CLAUDE.md`](.claude/CLAUDE.md)): operating modes that inherit
the identity above them and never claim a new one.

## 1. What a preset is — a lens, not a mask

A preset answers one question: *"which of {{OWNER}}'s roles is the brain operating in
right now?"* — and tunes the stack accordingly. The same vault, the same dual-role
identity, the same laws; a different **emphasis**.

The defining contrast:

| | **The vault** (Context Engine) | **A preset** (this layer) |
|---|---|---|
| Holds | the knowledge | nothing — it holds no knowledge |
| Changes when | a source is integrated | {{OWNER}} switches role |
| Effect | what the brain *knows* | how the brain *reads and prioritises* what it knows |
| Persistence | permanent (the wiki) | a session setting (the `active_preset` anchor) |

A preset is a **read-time configuration**, not a store. Deleting every preset would
lose no knowledge; it would only remove the role-shaped defaults.

## 2. Lanes — what this layer owns, and what it doesn't

- **Owns** the preset concept: the four levers (§3), the preset contract (§4), the
  switching mechanism (§5), and the two exemplar presets the engine ships.
- **Composes** the kernel: it sets the `active_preset` anchor that
  [read-routing §7](OPERATIONS-KERNEL.md) already consumes, via the existing
  `update-memory` capability ([§12](OPERATIONS-KERNEL.md)). **No new primitive.**
- **References** — never redefines — the domains ([TAXONOMY](TAXONOMY.md)), the
  instruments ([`instruments.md`](vault-template/.claude/instruments.md)), and the
  identity ([`.claude/CLAUDE.md`](.claude/CLAUDE.md)). A preset *selects among* them.
- **Does not** change knowledge (no canon edits), identity (the dual-role and the
  project director are constant), the laws, the domain taxonomy, or any instrument. It
  is a lens over all of those.
- **Defers** background/scheduled behaviour to S11 and capability growth to S12/S13 —
  a preset only *foregrounds* existing instruments, it never builds or runs one.

## 3. The four levers

A preset tunes exactly four things ([BRAIN-OS layer 7](BRAIN-OS.md)):

- **Focus** — the role's default priorities; what the brain leads with when {{OWNER}}
  has not named a task. Seeds `core.md`'s "Current focus" framing, never overwrites
  {{OWNER}}'s live focus.
- **Default domains** — which of the seven [TAXONOMY](TAXONOMY.md) domains lead
  read-routing. This is the concrete read effect: a preset's `default_domains` are the
  **set of active domains** [kernel §7.2](OPERATIONS-KERNEL.md) loads *absent a more
  specific task signal*, and a [§7.5](OPERATIONS-KERNEL.md) tie-break ranking signal
  (§6 — the lens-not-filter rule). They bias loading and ranking; they do not touch
  the topological traversal (§7.4).
- **Tone** — the role's **register and emphasis**: what to foreground, how much to
  challenge, the working vocabulary. **Not a different voice or personality** —
  there is one voice to {{OWNER}} (§7).
- **Lead instruments** — which agents/skills are foregrounded for the role (e.g. the
  research workers for a sales role, the Builder/audit instruments for an engineering
  role). It biases *which* instrument the brain reaches for first; it never grants or
  removes one.

## 4. The preset contract

A preset is a markdown file in [`presets/`](vault-template/presets/), one per role,
following [`_templates/preset.md`](vault-template/_templates/preset.md). Its
frontmatter declares the four levers so they are machine-readable at load:

```
---
preset: gtm-lead                 # the active_preset value that selects this file
title:                           # human name of the role
description:                     # one sentence — when this preset is the right lens
default_domains: []              # TAXONOMY domains that lead read-routing (biased, not exclusive)
lead_instruments: []             # instruments foregrounded for this role, by their registry name — skills/agents bare (research-agent), commands with the slash (/build)
tone:                            # one line — the role's register/emphasis (not a new voice)
updated:                         # YYYY-MM-DD
---
```

The body states, in prose, the role's **focus** and how the levers play together —
the texture an instance refines against real use (§8). The contract is generic and
placeholdered; it ships in every instance.

## 5. The switching mechanism

Switching is deliberately lightweight — config, not machinery:

1. **The anchor is the source of truth.** `memory/core.md` carries
   **`active_preset`** ([OPERATIONS-KERNEL §10](OPERATIONS-KERNEL.md)); whichever
   preset it names is live. There is exactly one active preset at a time.
2. **The kernel applies it on load.** [Read-routing §7.1](OPERATIONS-KERNEL.md)
   already reads the active preset from core memory; §7.2 loads the **active
   domain(s)**. This layer specifies that the active domain(s) default to the
   preset's `default_domains` (a set) when the task names none — biased, not
   exclusive (§6).
3. **`/preset` is {{OWNER}}'s entry.** [`/preset <name>`](vault-template/.claude/commands/preset.md)
   sets the anchor (via the kernel's `update-memory`) and reconfigures the session;
   `/preset` with no argument reports the current preset and the available ones.
4. **A switch is a logged setting change**, not a knowledge edit — recorded like any
   `core.md` update (kernel §10). It touches no canon page.

No agent and no skill: applying a preset is reading config and biasing the session,
which the kernel-load and `/preset` cover between them. A preset is config the brain
*reads*, not a procedure it *runs*.

## 6. Lens, not filter — the load-bearing rule

A preset sets **defaults**, never **blinkers**. The discipline:

- **The task overrides the preset.** Under the GTM Lead preset, a question about a
  `people` or `product` matter still loads those domains — the preset biases routing
  when the task is unspecified; it never suppresses a domain the task clearly needs.
- **Default domains *lead*, they do not *limit*.** `default_domains` are the set
  [§7.2](OPERATIONS-KERNEL.md) loads and a [§7.5](OPERATIONS-KERNEL.md) tie-break
  ranking signal for the role's domains; they do not remove the others from reach, and
  they do not touch the topological traversal (§7.4). Precision over recall — but never
  blindness.
- **A preset cannot hide a flag.** Contradictions and review items in `core.md` are
  always-loaded regardless of preset (kernel §10) — the brain never goes blind to its
  own open questions because of the lens it is wearing.

This is what keeps a preset an *operating mode* rather than a context cage.

## 7. Identity boundary — one voice, scoped modes

A preset is a focus mode **within** the constant identity, never a second identity:

- The **project director** ([`.claude/CLAUDE.md`](.claude/CLAUDE.md)) and the
  project **dual-role** (Pulse = brain, Claude = mind) are unchanged by any preset.
- **"Not a roleplay."** A preset's `tone` lever is register and emphasis — what to
  foreground and how hard to push — **not** a character. There is one voice to
  {{OWNER}} (project `.claude/CLAUDE.md`); a preset colours it, it does not replace it.
- A preset is a **scoped operating role beneath the project director**, exactly what
  the director sanctions: it inherits the standards, the laws, and the security boundary,
  and overrides none of them.

If a "preset" ever changed the voice, the standards, or the laws, it would have
stopped being a preset and started being an identity — which this layer forbids.

## 8. Security & the engine/instance boundary

- **Generic config, no live data.** A preset names *domains, instruments, tone, and
  focus* — all generic. It hardcodes **no real accounts, names, URLs, or metrics**;
  the role is generic to {{OWNER}}'s work, the specifics live in the vault the lens
  reads. `{{OWNER}}`/`{{COMPANY}}` placeholders throughout.
- **The engine ships exemplars.** `gtm-lead` and `ai-orchestrator` ship as the two
  named roles; an instance adds its own presets via the contract (§4). The engine
  states the capability and the levers, not the lived texture of a role — that
  matures at instance time against real data, like the Thinking voice (S10).
- **A switch is reversible and logged** — a setting change, never a content mutation.
  Immutability is untouched: no provenance tier is rewritten, only the `active_preset`
  anchor is set (recorded in `log.md`, kernel §8).

## 9. Seams

- **→ Operations Kernel** — a preset sets the `active_preset` anchor (§10) that
  read-routing (§7) consumes; it composes `update-memory` and adds no primitive.
- **→ Context Engine / TAXONOMY** — `default_domains` selects among the seven domains;
  the preset references the taxonomy, never extends it.
- **→ the instruments (S11/S12)** — `lead_instruments` foregrounds existing skills and
  agents; a preset never builds, grants, or runs one.
- **↔ Self-Development (S13)** — S13 may *notice* that a recurring need is unmet under
  a role and drive Builder to fill it, or surface that a new preset is warranted; the
  preset itself stays config. S14 is the lens, S13 is the growth that may reshape it.
- **→ Development (S15)** — concurrent tabs may each run under a different preset over
  the one shared vault; how sessions coordinate without colliding on `core.md` is the
  Development layer's ([`DEVELOPMENT.md`](DEVELOPMENT.md)) — the `active_preset` anchor
  is a derivable cache field the kernel reconciles from the log.
- **Identity (cross-cutting)** — every preset sits beneath the project director and the
  dual-role and inherits both (§7).

> **Persona / Presets complete.** The brain now operates as the role {{OWNER}} is in —
> GTM Lead, AI Orchestrator, or another — reading the same knowledge through a
> role-shaped lens of focus, domains, tone, and lead instruments, switchable in one
> command and never at the cost of the knowledge or the one voice beneath it. Next on
> the roadmap is **S15 — Development**, concurrent multi-tab operation over the shared
> vault.
