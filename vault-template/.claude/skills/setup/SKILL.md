---
name: setup
description: The one-time instantiation flow — stand up a live Pulse instance from a fresh clone of the engine. Interviews the owner (identity, owner-defined domains, presets, writing voice), scaffolds the instance OUTSIDE the engine via the deterministic instantiate tool, then guides the machine-specific wiring (embedding adapter, schedules, watchlist, .env) and first boot. Use when someone runs /setup or asks to create / instantiate their brain.
---

# setup — instantiate a live brain

The judgement half of the instantiation kit (the deterministic half is the
[`instantiate`](../../tools/instantiate) tool; the procedure is
[`SETUP.md`](../../../../SETUP.md), the boundary is
[`ARCHITECTURE.md` §1](../../../../ARCHITECTURE.md)). Run **once**, in a fresh clone of the
engine, to create the owner's own private instance. It composes the kernel and the tool —
**no new primitive**. The deterministic filesystem act is the tool's; this skill owns the
**interview** and the **machine-specific wiring** the tool deliberately does not touch
(network, credentials, cron, hooks — none of which a tool may do, BUILDER.md §3).

## The one rule

The instance is **created outside the engine and never committed to it**. The tool
enforces this (it refuses any target inside the engine); never work around it by scaffolding
into the engine's own `vault-template/`. The engine stays sanitised: templates and code
only, no live data, ever.

## 1. Interview (collect, do not assume)

Ask the owner, one focused question at a time:

- **Identity** — their name (`owner`) and organisation (`company`). These stamp the
  instance (e.g. `/pulse` greets them; `core.md`, presets, instruments).
- **Domains** — the pillars are organised by domain ([`TAXONOMY.md`](../../../../TAXONOMY.md)).
  The shipped `gtm`/`ai-orchestration`/`product`/`people`/`operating`/`glossary` are
  **examples** modelled on one owner's roles. Propose them as a starting menu and let the
  owner **edit, add, or replace** — these are *their* domains. (`entities` is always added
  to `canon/` only; it is not chosen.) Names are kebab-case.
- **Presets** — a preset is a selectable operating lens ([`PERSONA-PRESETS.md`](../../../../PERSONA-PRESETS.md)).
  The shipped `gtm-lead`/`ai-orchestrator` are **examples**. Ask which (if any) the owner
  wants to keep, and whether to author one for their own role(s).
- **Writing voice** — ask for a short writing sample (optional but strongly suggested,
  [`INTERFACE.md` §5](../../../../INTERFACE.md)); it calibrates deliverables to their hand.
- **Embedding** — local default (no key, on-device — recommended) or the API adapter
  (needs a key; canon text leaves the device). Default to local unless they choose API.
- **Target path** — where the instance dir lives, OUTSIDE the engine (suggest a sibling,
  e.g. `~/Developer/Pulse-<owner>-Brain`). Confirm it is not inside the engine.

## 2. Author any owner presets first

The `instantiate` tool validates `--preset` against the instance's `presets/`, so any
preset the owner wants that isn't shipped must exist first. For each, write a file from
[`_templates/preset.md`](../../../_templates/preset.md) into `presets/` (in the engine
clone, before scaffolding) — `preset`, `title`, `description`, `default_domains` (from
their chosen domains), `lead_instruments`, `tone`. Keep or delete the example presets per
their answer.

## 3. Scaffold — call the tool

Run the deterministic scaffolder with the collected answers:

```
python3 vault-template/.claude/tools/instantiate \
  --target <target> --owner "<owner>" --company "<company>" \
  --domains <d1,d2,…> [--preset <name>]
```

It copies the engine tree (authority docs unstamped at the instance root, the dual-role
`.claude/CLAUDE.md` stamped, `vault-template/` → `<target>/vault/`), scaffolds the owner's
domain subdirs, stamps the operational surfaces, seeds `core.md`/`index.md`/`log.md`, and
**verifies no placeholder survives** (it fails closed if one does). Read its report; on a
non-zero exit, fix the cause and re-run — do not proceed on a failed scaffold.

## 4. Fill instance content (in the new instance, not the engine)

Switch to the instance. Write the owner's writing sample into
`<target>/vault/memory/owner-voice.md` (or leave it for the owner to paste). Everything
from here is the owner's private data and lives only in the instance.

## 5. Guide the machine-specific wiring

Walk the owner through the wiring the tool cannot do (it is environment-specific, and a
tool may not touch network/credentials):

- **Embedding adapter** — local: install the substrate deps and pull + checksum-pin the
  model ([`MODEL-RETRIEVAL.md` §3.6](../../../../MODEL-RETRIEVAL.md)); API: set the key in
  `.env` (from `.env.example`). Then set the role→model bindings in
  [`model-bindings.md`](../../model-bindings.md).
- **Credentials** — copy `.env.example` to `.env` in the instance; fill only what the owner
  opts into. Never commit `.env`.
- **Schedules + hooks** — wire the background routines and the `SessionEnd` +
  periodic `session-reconcile` triggers per [`scheduling.md`](../../scheduling.md), at the
  owner's chosen cadences, via Claude Code's scheduler.
- **Watchlist** — populate the `monitor` watchlist (instance config; feed creds via `.env`).

## 6. First boot + activation

Launch Claude Code **from the instance root** (so the root `.claude/CLAUDE.md` and the
authority-doc links resolve); open `<target>/vault` in Obsidian. Then:

- run [`/pulse`](../../commands/pulse.md) — the brain wakes, reads its (now real) state;
- run [`/reindex`](../../commands/reindex.md) to build the first semantic index;
- once there is real content, calibrate the retrieval thresholds and turn re-ranking on in
  read-routing ([`MODEL-RETRIEVAL.md` §6](../../../../MODEL-RETRIEVAL.md)).

## 7. Record

Surface a short **Pulse decision** summarising what was instantiated — owner, domains,
presets, embedding adapter, schedules — so the choices are visible and reviewable. The
instance's own `log.md` already carries the "Brain instantiated" entry the tool seeded.

Gated by [`tests/instantiation-contract.md`](../../tests/instantiation-contract.md).
