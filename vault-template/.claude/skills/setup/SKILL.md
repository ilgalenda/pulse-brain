---
name: setup
description: The one-time instantiation flow that stands up a live Pulse instance from a fresh clone of the engine. It interviews the owner (identity, owner-defined domains, presets, writing voice), scaffolds the instance OUTSIDE the engine via the deterministic instantiate tool, then guides the machine-specific wiring (embedding adapter, schedules, watchlist, .env) and first boot. Use when someone runs /setup or asks to create or instantiate their brain.
---

# setup: instantiate a live brain

This is the judgement half of the instantiation kit. The deterministic half is the
[`instantiate`](../../tools/instantiate) tool, the procedure is
[`SETUP.md`](../../../../SETUP.md), and the boundary is set in
[`ARCHITECTURE.md` §1](../../../../ARCHITECTURE.md). Run it **once**, in a fresh clone of the
engine, to create the owner's own private instance. It composes the kernel and the tool, adding
**no new primitive**. The deterministic filesystem act belongs to the tool; this skill owns the
**interview** and the **machine-specific wiring** the tool deliberately does not touch
(network, credentials, cron, hooks), none of which a tool may do (BUILDER.md §3).

## The one rule

The instance is **created outside the engine and never committed to it**. The tool
enforces this: it refuses any target inside the engine. Never work around it by scaffolding
into the engine's own `vault-template/`. The engine stays sanitised, holding templates and code
only, with no live data, ever.

## 1. Interview (collect, do not assume)

Ask the owner, one focused question at a time:

- **Identity.** Their name (`owner`) and organisation (`company`). These stamp the
  instance (for example, `/pulse` greets them, and they appear in `core.md`, presets, and instruments).
- **Domains.** The pillars are organised by domain ([`TAXONOMY.md`](../../../../TAXONOMY.md)).
  The shipped `gtm`/`ai-orchestration`/`product`/`people`/`operating`/`glossary` are
  **examples** modelled on one owner's roles. Propose them as a starting menu and let the
  owner **edit, add, or replace** them, because these are *their* domains. (`entities` is always added
  to `canon/` only; it is not chosen.) Names are kebab-case.
- **Presets.** A preset is a selectable operating lens ([`PERSONA-PRESETS.md`](../../../../PERSONA-PRESETS.md)).
  The shipped `gtm-lead`/`ai-orchestrator` are **examples**. Ask which (if any) the owner
  wants to keep, and whether to author one for their own role(s).
- **Writing voice.** Ask for a short writing sample (optional but strongly suggested,
  [`INTERFACE.md` §5](../../../../INTERFACE.md)); it calibrates deliverables to their hand.
- **Embedding.** The local default (no key, on-device, recommended) or the API adapter
  (needs a key; canon text leaves the device). Default to local unless they choose API.
- **Target path.** Where the instance directory lives, OUTSIDE the engine. Suggest a sibling,
  for example `~/Developer/Pulse-<owner>-Brain`, and confirm it is not inside the engine.

## 2. Author any owner presets first

The `instantiate` tool validates `--preset` against the instance's `presets/`, so any
preset the owner wants that isn't shipped must exist first. For each, write a file from
[`_templates/preset.md`](../../../_templates/preset.md) into `presets/` (in the engine
clone, before scaffolding), filling in `preset`, `title`, `description`, `default_domains` (from
their chosen domains), `lead_instruments`, and `tone`. Keep or delete the example presets per
their answer.

## 3. Scaffold: call the tool

Run the deterministic scaffolder with the collected answers:

```
python3 vault-template/.claude/tools/instantiate \
  --target <target> --owner "<owner>" --company "<company>" \
  --domains <d1,d2,…> [--preset <name>]
```

It lays out a flat instance — authority docs unstamped in `<target>/docs/`, the dual-role
director and the operating layer in `<target>/.claude/`, and the knowledge folders at
`<target>/` itself — repoints each instrument's (and the director's) authority-doc links to
`docs/`, scaffolds the owner's domain subdirectories, stamps the operational surfaces, seeds
`core.md`/`index.md`/`log.md`, and **verifies no placeholder survives** (it fails closed if
one does). Read its report; on a non-zero exit, fix the cause and re-run. Do not proceed on a
failed scaffold.

## 4. Fill instance content (in the new instance, not the engine)

Switch to the instance. Write the owner's writing sample into
`<target>/memory/owner-voice.md` (or leave it for the owner to paste). Everything
from here is the owner's private data and lives only in the instance.

## 5. Guide the machine-specific wiring

Walk the owner through the wiring the tool cannot do (it is environment-specific, and a
tool may not touch network or credentials):

- **Embedding adapter.** For local, install the substrate dependencies and pull then checksum-pin the
  model ([`MODEL-RETRIEVAL.md` §3.6](../../../../MODEL-RETRIEVAL.md)). For API, set the key in
  `.env` (from `.env.example`). Then set the role-to-model bindings in
  [`model-bindings.md`](../../model-bindings.md).
- **Credentials.** Copy `.env.example` to `.env` in the instance, and fill only what the owner
  opts into. Never commit `.env`.
- **Schedules and hooks.** Wire the background routines and the `SessionEnd` and
  periodic `session-reconcile` triggers per [`scheduling.md`](../../scheduling.md), at the
  owner's chosen cadences, via Claude Code's scheduler.
- **Watchlist.** Populate the `monitor` watchlist (instance config; feed credentials via `.env`).

## 6. First boot and activation

Launch Claude Code **from the instance root** (its `.claude/` holds the director and the
commands), then open `<target>` itself in Obsidian. Then:

- run [`/pulse`](../../commands/pulse.md), so the brain wakes and reads its (now real) state;
- run [`/reindex`](../../commands/reindex.md) to build the first semantic index;
- once there is real content, calibrate the retrieval thresholds and turn re-ranking on in
  read-routing ([`MODEL-RETRIEVAL.md` §6](../../../../MODEL-RETRIEVAL.md)).

## 7. Record

Surface a short **Pulse decision** summarising what was instantiated (owner, domains,
presets, embedding adapter, schedules) so the choices are visible and reviewable. The
instance's own `log.md` already carries the "Brain instantiated" entry the tool seeded.

Gated by [`tests/instantiation-contract.md`](../../tests/instantiation-contract.md).
