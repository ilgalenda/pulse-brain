# Fixture — the preset contract

The acceptance checklist the **Persona / Presets layer**
([`PERSONA-PRESETS.md`](../../../PERSONA-PRESETS.md)) must pass. It has two halves: a
preset **file** is well-formed, and a preset **switch** behaves as a lens — biasing
without changing knowledge or identity. This restates the four levers (§3), the
contract (§4), the switching mechanism (§5), and the lens-not-filter and identity
boundaries (§6/§7) as a *test*, not a new authority. If any item fails, the layer is
not yet correct.

## Part A — a well-formed preset file

A file in [`presets/`](../../presets/) ([`_templates/preset.md`](../../_templates/preset.md)):

- [ ] **`preset`** — a kebab-case id that matches the `active_preset` value selecting it.
- [ ] **`title` + `description`** — the role's human name and a one-line "when this lens".
- [ ] **`default_domains`** — only real [TAXONOMY](../../../TAXONOMY.md) domains
      (`gtm`/`ai-orchestration`/`product`/`people`/`operating`/`glossary`/`entities`);
      they *lead* routing, and the file/contract says so (not "exclusive").
- [ ] **`lead_instruments`** — instruments that exist in
      [`instruments.md`](../instruments.md), by their registry name (skills/agents
      bare, e.g. `research-agent`; commands with the slash, e.g. `/build`); the preset
      *foregrounds* them, it does not grant or define any.
- [ ] **`tone`** — register and emphasis in one line; **not** a character or a new voice.
- [ ] **Generic & placeholdered** — `{{OWNER}}`/`{{COMPANY}}`; **no** real accounts,
      names, URLs, or metrics. It ships in every instance.
- [ ] **Holds no knowledge** — focus and texture only; no canon claims, no source data.

A file that invents a domain, references a non-existent instrument, or hardcodes real
data is **rejected**.

## Part B — a correct preset switch (the lens behaviour)

When `/preset <name>` runs:

- [ ] **Anchor set, nothing else** — `active_preset` in
      [`core.md`](../../memory/core.md) is updated via the kernel's `update-memory`;
      **no canon page is touched**. It is a logged setting change, not a knowledge edit.
- [ ] **Exactly one active preset** — the switch replaces the prior value; presets do
      not stack.
- [ ] **Default domains lead, do not limit** — read-routing raises the preset's
      domains; a task that names another domain **still loads it** (lens, not filter,
      §6).
- [ ] **Flags survive the lens** — `core.md` "Needs review" / contradictions remain
      always-loaded regardless of preset; the brain never goes blind to its open
      questions.
- [ ] **One voice** — `tone` colours emphasis and register; the dual-role identity and
      the project director are unchanged (§7). No standard, law, or voice shifts.
- [ ] **Unknown name is refused** — `/preset wrong-name` reports the available presets
      and changes nothing; it does not guess.
- [ ] **No-arg shows, never sets** — `/preset` reports the current and available
      presets and changes nothing.

## Worked PASS example

> **File.** `presets/gtm-lead.md`: `preset: gtm-lead`, `default_domains: [gtm,
> people]`, `lead_instruments: [research, research-agent, monitor, /sweep]` (skills
> bare, command slashed), `tone:` "direct and commercial". Generic, no real accounts.
> **Valid.**
>
> **Switch.** `/preset gtm-lead` sets `active_preset: gtm-lead` in `core.md` (logged
> setting change, no canon touched). The session now leads with `gtm`/`people` and
> foregrounds the research workers. {{OWNER}} then asks a `product` positioning
> question — the brain **still loads `product`** (task overrides the lens). A
> contradiction flag in `core.md` stays visible. The voice is unchanged; only the
> emphasis shifted.

## FAIL examples the layer must NOT produce

- **A preset that filters** — suppressing a domain the task clearly needs, or hiding a
  `core.md` flag because of the active lens (a context cage, not an operating mode).
- **A preset that re-identifies** — changing the voice, the standards, the laws, or
  the Pulse/Claude dual-role (§7 — that is an identity, not a preset).
- **A switch that writes knowledge** — editing a canon page, or recording the
  preset's focus as a source/claim, instead of only setting the anchor.
- **A preset with live data** — a hardcoded account, person, URL, or metric.
- **A new primitive** — inventing a switching mechanism instead of setting
  `active_preset` via `update-memory`.
