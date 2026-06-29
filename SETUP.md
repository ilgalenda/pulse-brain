# Setting up your own Pulse brain

Pulse_Brain is an **engine** — sanitised architecture, templates, and code, with no live
data. You turn it into a working brain by **instantiating** it: stamping out your own
private instance (`Pulse-<you>-Brain`) in a separate directory, which you then populate
and use daily. This page is the procedure. (For what Pulse *is* and how it works, see
[`README.md`](README.md) and [`ARCHITECTURE.md`](ARCHITECTURE.md).)

> **The data boundary.** Your instance is a **separate directory, outside this engine, and
> is never committed back to it.** The engine stays generic (templates + code only); your
> knowledge lives only in your instance. The instantiation tool enforces this — it refuses
> to scaffold anywhere inside the engine.

## Prerequisites

- **[Claude Code](https://claude.com/claude-code)** — Pulse is driven through it on the
  CLI (and the desktop app), including multiple concurrent sessions. This is the runtime.
- **Python 3** — for the engine's deterministic tools and the retrieval substrate
  (stdlib only for the core; the optional local embedding model adds dependencies at S19).
- **[Obsidian](https://obsidian.md)** (recommended) — the instance is an Obsidian vault;
  Obsidian is the human view onto it. Optional but the intended editor.
- **Optional:** an embedding model (local, no key — the default) or an embedding API key,
  only if you turn on semantic retrieval. Pulse runs without either.

## Instantiate

1. **Clone the engine** and open it in Claude Code:
   ```
   git clone <your-clone-of-Pulse_Brain> && cd Pulse_Brain
   ```
2. **Run `/setup`.** It interviews you — your name and organisation, your **own domains**
   (the shipped `gtm`/`ai-orchestration`/… are just examples to edit), which **presets**
   (operating lenses) to keep or author, an optional **writing sample**, your **embedding**
   choice, and the **target path** for your instance (a directory *outside* the engine,
   e.g. `~/Developer/Pulse-<you>-Brain`). It then scaffolds the instance for you.

   Under the hood `/setup` calls the deterministic
   [`instantiate`](vault-template/.claude/tools/instantiate) tool, which copies the engine
   tree (keeping the structure so every internal link resolves), stamps your identity onto
   the operational files, scaffolds your domains, seeds the starting state, and verifies no
   placeholder is left. You can preview it without writing anything:
   ```
   python3 vault-template/.claude/tools/instantiate --target ~/Developer/Pulse-you-Brain \
     --owner "You" --company "YourOrg" --domains work,people,reference --dry-run
   ```
3. **Wire the machine-specific bits** `/setup` walks you through — the embedding adapter,
   the background schedules and the `SessionEnd` hook, the watchlist, and `.env` (copy from
   [`.env.example`](.env.example); everything in it is optional). None of this is required
   to start; the brain runs with none of it.

## First boot

Your instance has this shape (the authority docs sit at the instance root so the
instruments' links resolve; your live vault is the `vault/` subfolder):

```
Pulse-<you>-Brain/
├── (the authority docs — your reference copies)
├── .claude/CLAUDE.md        the dual-role director
└── vault/                   ← open THIS in Obsidian
```

- **Launch Claude Code from the instance root** (`Pulse-<you>-Brain/`).
- **Open `vault/` in Obsidian** as your vault.
- Run **`/pulse`** — the brain wakes, reads its state, and greets you.
- Add your first sources (drop notes/URLs into `inbox/`, or just talk to it), and run
  **`/reindex`** once you want semantic retrieval over what you've compiled.

That's it — you have a living brain. It is yours, local, and private; nothing you put in it
travels back to the engine.

## Updating the engine later

The engine evolves. To take updates, pull the engine in your clone and re-apply the parts
you want — your instance is separate, so engine updates never touch your data. (A guided
upgrade path is future work.)
