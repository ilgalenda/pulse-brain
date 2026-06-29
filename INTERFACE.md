# Pulse_Brain — Interface

Brain-OS **layer 9**: how {{OWNER}} interacts with the brain day to day. It is the
set of **surfaces** through which {{OWNER}} *enters*, *feeds*, and *reviews* the
brain — not a new operation surface replacing the CLI, but the shape of the
interaction around it.

This is a **code (UX)** layer ([BRAIN-OS instruction-vs-code map](BRAIN-OS.md)),
built **lean and design-first**: it defines the interaction surfaces, realises the
ones that work against the local vault today, and **defers** the parts whose value
needs a live instance (S19) or a later substrate (S18). It introduces **no new kernel
primitive** — the surfaces compose `load` and the existing capture front-door
([OPERATIONS-KERNEL §1/§7](OPERATIONS-KERNEL.md)).

## 1. What this layer is — surfaces over one brain

The brain is operated **primarily through Claude Code on the CLI**
([ARCHITECTURE §4](ARCHITECTURE.md)). Four surfaces frame that interaction:

- **Boot / entry (CLI)** — the deliberate *"wake the brain"* act. **Realised now:**
  [`/pulse`](vault-template/.claude/commands/pulse.md) (§2).
- **Capture (channel-agnostic)** — getting material into the Inbox pillar from
  wherever {{OWNER}} is. **Designed; realised progressively** (§3).
- **Review (Obsidian)** — reading the compiled wiki and clearing flags. Obsidian is
  the IDE; **lean conventions now, richer at instance** (§4).
- **Output (deliverables)** — how the brain presents what it hands back: briefings,
  reports, exported documents. **Defined now as a standard** (§5).

The principle: the layer is **designed in full, built only where building is honest**.
A UX layer's worth lives in the lived experience, which arrives with the live vault
(S19) — so the experiential parts are specified now and matured then, not gold-plated
against a vault that does not yet exist.

## 2. Boot / entry — `/pulse` (realised)

The brain does **not** assume every terminal session is a Pulse session — opening a
CLI is not the same as using the brain. The brain is **summoned**.
[`/pulse`](vault-template/.claude/commands/pulse.md) wakes it:

1. **Paints the boot banner** — the PULSE wordmark, shipped byte-exact as
   [`pulse-banner.txt`](vault-template/.claude/pulse-banner.txt) so the art is never
   re-typed.
2. **Wakes the brain** — runs read-routing ([kernel §7](OPERATIONS-KERNEL.md)):
   loads core memory (`active_preset`, current focus, live threads, the Needs-review
   flags) + `index.md`. This *is* the kernel's session-start read, made explicit.
3. **Greets and reports state** — `Hi {{OWNER}}`, then a compact status: active
   preset · current focus · items needing review · last activity.
4. **Stands ready** in that context.

It **composes `load`** and adds no primitive — the banner is presentation, the status
is read-routing surfaced. `/pulse <preset>` optionally wakes straight into a lens
(composing [`/preset`](vault-template/.claude/commands/preset.md)). Gated by the
[`interface-contract`](vault-template/.claude/tests/interface-contract.md) fixture.

Why a command, not a `SessionStart` hook: a hook's output is injected into context,
not displayed, and would fire on every session whether or not {{OWNER}} means to use
the brain. A command renders visibly and is **summoned on purpose** — the correct
model for entering the brain.

## 3. Capture — channel-agnostic (designed; realised later)

The Inbox pillar accepts material from whatever channel fits — **no bespoke app
required**. The channels, by reach:

- **CLI capture** — the desk channel; already exists (the ingestion front-door,
  [kernel §1](OPERATIONS-KERNEL.md); Inbox, [CONTEXT-ENGINE](CONTEXT-ENGINE.md), S8).
- **Remote Control** — operate/capture from the phone **with the Mac awake**. It runs
  the session *on the local machine* (a tunnel, not the cloud), so it captures into
  the real vault and **does not cross the data boundary**. It is research-preview, so
  the **preferred but not required** phone channel.
- **Synced drop-folder** — the **async** channel for when the Mac is asleep: a watched
  folder (iCloud / Dropbox / Obsidian Sync) the Inbox ingests when next awake. The
  sync provider is the always-on intermediary, so this needs **no app and no backend**
  — only a light watch-folder ingest. This is the one piece of code §3 will add, built
  when capture friction is real.
- **Hosted endpoint** — the fully-remote channel (a URL the outside posts to). This is
  S18's sync backend; **deferred**.

**Decided with {{OWNER}}:** no bespoke mobile app — Remote Control (Mac awake) plus the
synced drop-folder (Mac asleep) cover on-the-go capture between them, at a fraction of
an app's cost. **Claude Code on the web is *not* a Pulse channel** — it runs the vault
in a cloud VM, which crosses the data boundary; Remote Control is the local-only
alternative (§6).

## 4. Review — the Obsidian surface (lean now; matures at instance)

Obsidian is the **IDE** where {{OWNER}} reads the compiled wiki and clears the
**Needs-review** queue. For now this surface is **convention, not code**: the review
queue lives in `core.md`'s `## Needs review` ([kernel §10](OPERATIONS-KERNEL.md)) and
`index.md` is the map-of-content ([kernel §6](OPERATIONS-KERNEL.md)) — `/pulse`
surfaces the queue count on boot (§2). Richer review dashboards are **deliberately
deferred**: their value is in how they feel against real, populated knowledge, so they
mature with the live vault (S19) rather than being designed blind now.

## 5. Output: the deliverable presentation standard

The brain does not only hold knowledge. It produces things {{OWNER}} reads and acts
on: briefings, reports, documents to share. How those are presented is an Interface
concern, and the bar is high. This section governs **outbound deliverables only**. The
structure of internal knowledge artifacts (canon pages, source notes, the log) is owned
by the Context Engine and Taxonomy, and this layer neither repeats nor overrides it.

### 5.1 It must not read as machine-written

Every deliverable is written to the standard of {{OWNER}}'s own hand, in **British
English**, with a genuine voice. The tells of generated text are treated as defects to
be removed before anything reaches {{OWNER}}:

- The em-dash is not used as a connective tic. Where a break is needed, the sentence
  takes a full stop, a comma, a colon, or a semicolon, whichever the meaning calls for.
- Ideas are not padded into tidy triplets for rhythm. A list runs as long as the truth
  is, whether that is two items or seven.
- Templated scaffolding is absent. There is no throat-clearing opener, no symmetrical
  paragraph shape, no closing flourish that restates without adding.
- Filler earns nothing and is cut. Every sentence carries information or it goes.

This inherits the global writing-craft standard and holds the brain's output to it
without exception.

### 5.2 Briefings: written for a Prime Minister

A briefing assumes its reader is {{OWNER}} as Prime Minister or chief executive:
someone who must be wholly across a matter in the time it takes to read a page, and who
will decide on the strength of it. The standard is government-grade.

- **The judgement leads.** The opening states what matters and what {{OWNER}} should
  decide or do, ahead of any background, so that stopping after the first lines still
  leaves {{OWNER}} holding the essentials.
- **Complete, not padded.** Everything bearing on the decision is present and nothing
  that does not bear on it. Length is never the measure; exposure is. {{OWNER}} is left
  uncovered on nothing.
- **Sourced.** Each claim traces to the canon and the sources it was compiled from, so
  the ground beneath it is visible and can be challenged.
- **Exact about certainty.** Figures sit where figures belong, terms are defined,
  confidence is stated plainly, and what is not known is named rather than smoothed over.

The existing `execbrief` capability is the nearest precedent. This standard is its
discipline applied to everything the brain briefs.

### 5.3 PDFs and exported documents

A document rendered to PDF or another portable format carries the same intent as a
briefing: {{OWNER}} stays on top of the material at a glance and in depth. The
presentation is clean and authoritative, the kind of paper a cabinet or a board would
receive. It uses a clear hierarchy of headings, room to breathe, figures and tables
where they carry a point better than prose, and provenance kept intact so the document
stands on its sources.

The style is set here. The generation is not built here. Emitting a styled PDF needs a
renderer with templates and a conversion step, which is code and belongs with the
substrate and tooling rather than this lean pass. The engine states what a Pulse
document should look like now, and the mechanism that produces it is built when it is
needed, the same way the schedule template precedes the live cron.

### 5.4 The owner's voice: a sample the brain asks for at setup

So that output sounds like {{OWNER}} rather than a generic register, setup (S19)
**asks {{OWNER}} for a sample of their own writing**: a document, a handful of their
briefings or notes, anything that shows how they write. It is **not mandatory, but
strongly suggested**, because it is the cheapest way to make every later deliverable
read in {{OWNER}}'s voice.

The sample lives at a known location, [`memory/owner-voice.md`](vault-template/memory/owner-voice.md),
and the deliverable standard reads it before producing a briefing or a report, mirroring
the vocabulary, sentence length, and register captured there. With no sample provided,
the brain falls back to the defaults in this section and says so, so the absence is
visible rather than guessed at.

## 6. Security & the engine/instance boundary

- **Generic and placeholdered.** The banner and command name no real person — `Hi
  {{OWNER}}` fills at instantiation (S19), like every placeholder. No live data.
- **Capture is inbound.** A capture channel *deposits new material*; it never reads or
  exposes existing canon — so the data-boundary risk of capturing from outside is
  minimal by construction.
- **Local-only phone access.** Remote Control keeps files on the machine (only prompts
  and outputs transit, encrypted); **Claude Code on the web** clones the vault into an
  Anthropic VM and is therefore excluded as a Pulse channel. The boundary holds.
- **The owner-voice sample is instance content.** The writing sample (§5.4) is filled at
  setup and never committed, exactly like core memory and the log; the engine ships only
  the placeholdered template.

## 7. Seams

- **→ Operations Kernel** — every surface composes `load` / the ingestion front-door;
  `/pulse` is read-routing ([§7](OPERATIONS-KERNEL.md)) made explicit. No primitive.
- **→ Context Engine / Inbox (S8)** — the capture channels feed the Inbox pillar; this
  layer routes *into* it, it does not redefine it.
- **↔ Persona / Presets** — `/pulse` reports the `active_preset` and can wake into one
  (composing [`/preset`](vault-template/.claude/commands/preset.md)).
- **→ S18 (MCP hosting)** — the hosted capture endpoint and external MCP surface.
- **→ S19 (instantiation)** — the experiential UX (review dashboards, boot polish, the
  drop-folder ingest) realises and matures against the live vault; setup also runs the
  owner-voice ask (§5.4).
- **↔ global writing-craft standard** — the output standard (§5.1) inherits it; the
  brain's deliverables hold to British English and a genuine, non-templated voice.
- **→ tooling / substrate** — the PDF renderer (§5.3) is deferred code, not built in
  this lean pass.
- **Identity (cross-cutting)** — the greeting, status, and house voice are presentation;
  one voice to {{OWNER}}, beneath the director.

> **Interface — boot/entry and the output standard shipped.** The brain is now
> **summoned** with `/pulse`, which wakes it, greets {{OWNER}}, and reports where they
> left off; and the deliverable standard (§5) sets how it presents what it hands back:
> government-grade briefings in {{OWNER}}'s own British-English voice, sourced and free
> of the machine-written tells, calibrated to a writing sample the brain asks for at
> setup. The capture channels and the Obsidian review surface are designed here and
> realise progressively as real use, and the live vault (S19), make them honest to build.
