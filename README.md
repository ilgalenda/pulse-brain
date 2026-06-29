# Pulse_Brain

A persistent, file-based **brain that powers Claude**. Instead of answering from raw notes
each time, it maintains a **living wiki** — compiling what you give it into entity pages,
topic summaries, and synthesis, kept current as it learns. It is also an **intelligence
partner**: it thinks *with* you, surfaces connections, brings in outside research, and
pushes back rather than just agreeing.

You run it through **Claude Code**, over a local **Obsidian** vault that is yours and
private. This repository is the **engine** — the architecture, templates, and code. You
turn it into a working brain by instantiating your own private copy (see *Get started*).

## How it works

- **Three pillars.** `canon/` is the living wiki; `inbox/` holds the sources you add and
  `dynamic/` the sources agents gather. Sources are **compiled into** the wiki, not
  re-read per query — *compile, don't retrieve*.
- **A growing graph.** The brain develops by growing the links between pages, sources, and
  entities. That node-graph is the thing that compounds; the frontier model stays
  pluggable underneath it.
- **It extends itself.** When a recurring need has no tool, the brain builds one — a skill,
  agent, command, or helper — to its own standards, and audits it. It monitors its own
  health and proposes fixes for you to ratify.
- **Layered, by design.** A kernel, a context engine, and active layers for thinking,
  research, building, and self-development sit under a UX and a model/retrieval substrate.
  The whole design is in [`ARCHITECTURE.md`](ARCHITECTURE.md).

## Engine and instance — and the data boundary

Pulse is split in two so the architecture is shareable and your knowledge stays private:

| Tier | What it is | Holds your data? | In this repo? |
|---|---|---|---|
| **Engine** (this repo) | Sanitised architecture, templates, and code. The reusable model. | No | Yes |
| **Instance** (`Pulse-<you>-Brain`) | Your live Obsidian vault, instantiated from the engine, used daily. | Yes | No — separate, local, private |

**The data boundary is absolute.** The engine ships templates and code only; your live
knowledge lives only in your instance, in a separate directory, and is never committed back
here. The instantiation tool enforces this — it refuses to scaffold anywhere inside the
engine.

## Get started

**Prerequisites:** [Claude Code](https://claude.com/claude-code) (the runtime), Python 3
(for the engine's tools), and [Obsidian](https://obsidian.md) (recommended, the human view
onto your vault). An embedding model or API key is optional — semantic retrieval defaults
to local, and the brain runs without it.

1. **Clone** this repo and open it in Claude Code.
2. Run **`/setup`** — it interviews you (your name, your own domains, operating presets,
   a writing sample, embedding choice) and scaffolds your private instance in a separate
   directory *outside* the engine.
3. Launch Claude Code from your instance, open its `vault/` in Obsidian, and run **`/pulse`**
   to wake the brain.

The full walkthrough — including the optional wiring (schedules, watchlist, credentials) —
is in [`SETUP.md`](SETUP.md).

## Status

Built section by section, each planned before it was implemented (see
[`ARCHITECTURE.md`](ARCHITECTURE.md) for the design and the roadmap). The architecture is
**complete** — all ten layers, the instantiation kit, and the data boundary are in place.

## Author & licence

A personal, Claude-native brain by **Ivan Luca Galenda**, shared as-is for others to use and
adapt. Licensed under the **MIT License** ([`LICENSE`](LICENSE)). It's a personal project,
not a supported product — but if you build your own brain from it, that's exactly the point.
