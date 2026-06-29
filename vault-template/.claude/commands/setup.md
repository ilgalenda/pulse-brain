---
description: Stand up a new live Pulse instance from this engine. This is the one-time instantiation flow. It interviews you for owner / domains / presets / voice, scaffolds the instance OUTSIDE the engine via the instantiate tool, and guides the environment wiring. Run once, in a fresh clone of the engine.
argument-hint: [optional target path for the instance, e.g. ~/Pulse-Ann-Brain]
---

Run the **first-time instantiation** of a live Pulse brain (the instantiation kit; see
[`SETUP.md`](../../../SETUP.md) and [`ARCHITECTURE.md` §1](../../../ARCHITECTURE.md)).

This is the entry to the [`setup`](../skills/setup/SKILL.md) skill. It is run **once**, in
a fresh clone of the engine, to create your own private instance (`Pulse-<you>-Brain`) in
a separate directory **outside** the engine. The data boundary is enforced by
construction: the [`instantiate`](../tools/instantiate) tool refuses any target inside the
engine. If `$ARGUMENTS` gives a target path, use it; otherwise the skill asks.

Run the [`setup`](../skills/setup/SKILL.md) skill, which:
- **interviews** you for your `owner` name, `company`, your **own domains** (the shipped
  `gtm`/`ai-orchestration`/… are just examples to edit), and which **presets** to keep or
  author (the two shipped presets are examples);
- **authors** any preset you want that isn't shipped, before scaffolding;
- **calls `instantiate`** to scaffold, stamp, and seed the instance deterministically;
- **captures** your writing sample into the instance's `memory/owner-voice.md`;
- **guides the environment wiring** that is machine-specific (the embedding adapter, the
  cron cadences plus `SessionEnd` hook, the watchlist, `.env`), then the first `/pulse` and
  `/reindex`.

It never writes inside the engine, and it produces **local instance data that is never
committed** to the engine.
