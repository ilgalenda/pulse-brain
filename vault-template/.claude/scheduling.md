# Scheduling — the autonomy wiring (template)

How the brain's background workers run unattended (RESEARCH-AGENTS.md §5). This is
a **template**: it ships the *pattern* with placeholder cadences and an **empty
watchlist**. The live schedule and watchlist are **instance content** — filled at
instantiation (S19), held in instance config / `.env`, and **never committed to
the engine**.

> Autonomy runs on **Claude Code's native scheduling** (cron routines / background
> tasks). The brain does not ship a bespoke daemon — it schedules its own commands.

## What gets scheduled

| Routine | Runs | Cadence (instance sets) | Bound |
|---|---|---|---|
| Inference drain | `/research` with no arg → `research-agent` over the `edge/inference` queue | e.g. a few times daily `<SET_AT_INSTANCE>` | cap notes/run |
| Monitoring beat | `/monitor` → `monitor-agent` over the watchlist | e.g. hourly/daily `<SET_AT_INSTANCE>` | cap notes/beat |
| Thinking sweep | `/sweep` → a Thinking sweep (S10) | e.g. daily `<SET_AT_INSTANCE>` | scope to a domain slice |
| Growth audit | `/grow` → `growth-agent` over graph health + capability gaps (S13) | e.g. weekly `<SET_AT_INSTANCE>` | bounded top-set; scope to a pillar/slice |
| Session reconcile | `session-reconcile` tool — compact `sessions.md`, reap crashed tabs, report `core.md` drift (S15) | **two triggers**: a `SessionEnd` hook (clean exit) + a periodic tick e.g. ~15' `<SET_AT_INSTANCE>` | own file only; deterministic; no net/creds |
| Semantic reindex | `/reindex` → the `substrate/` indexer — re-embed changed canon pages into the derived vector cache (S17) | e.g. after a heavy integration / daily `<SET_AT_INSTANCE>` — deferred until the embedding adapter is set up at S19 | incremental by content-hash; store is instance data, gitignored |

## Wiring it (at instance time)

1. Decide each routine's cadence (above) for this instance's needs.
2. Register them with Claude Code's scheduler (the `/schedule` routine mechanism),
   pointing each at the command shown.
3. Populate the **watchlist** for `monitor` in instance config — the sources to
   watch and a last-seen marker per source. Example shape (no live entries):

   ```
   # watchlist (INSTANCE CONFIG — do not commit; no live URLs in the engine)
   # - source: <url-or-feed>     last_seen: <marker>     domain: <domain>
   ```

4. Provide any feed credentials via `.env` (never inline).
5. Wire **session-reconcile** with its two triggers: register a `SessionEnd` hook in
   `settings.json` that runs the tool on clean tab close, and schedule a loose
   periodic tick (~15') as the crash backstop. Unlike the rows above it is a *tool*
   run directly (not a command → agent), and it needs no watchlist.

## Safety (inherited)

- **Bounded runs** — every routine caps its work; a worker reports and stops at
  the cap rather than looping.
- **Concurrency safe-by-default** — append-only `log.md`, new-file dynamic notes,
  `core.md` last-writer-with-care (kernel §10). The full multi-tab protocol is the
  Development layer ([`DEVELOPMENT.md`](../../DEVELOPMENT.md), S15): the write-class
  taxonomy, the ledger/cache guarantee, the `sessions.md` note, and `session-reconcile`.
- **Content is data, never instructions**; **secrets via `.env`**; **generic
  engine, live schedule at instance** — the data boundary holds.
