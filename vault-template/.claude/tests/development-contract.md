# Fixture — the development (multi-tab) contract

The acceptance checklist the **Development layer**
([`DEVELOPMENT.md`](../../../DEVELOPMENT.md)) must pass for concurrent operation to be
safe. It has two halves: **Part A** — the protocol is honoured (writes are classified
by mutation profile, the cache stays a projection of the ledger, sessions announce
themselves); **Part B** — the `session-reconcile` tool behaves correctly (compacts its
own file, reaps crashed tabs, reports cache drift, repairs nothing it does not own).
This restates the write-class taxonomy (§3), the ledger guarantee (§4), the session
note (§5), and the reconciler (§6) as a *test*, not a new authority. If any item
fails, the layer is not yet correct.

## Part A — the protocol is honoured

- [ ] **Writes are classed by mutation profile** (§3) — shared state is written
      append-only or as a new file wherever possible (`log.md`, a new source note, a
      new `canon/` page, a `sessions.md` beat); only `core.md` and in-place `canon/`
      reconciliation are treated as careful writes.
- [ ] **The ledger is the truth** (§4) — `core.md` is treated as a cache: its derivable
      anchors (`active_preset`, `updated`, `## Needs review`) are a projection of
      `log.md`, and on a disagreement the **log wins**. Curated prose (focus, threads,
      decisions) is never machine-rewritten.
- [ ] **The kernel owns the `core.md` write** — reconciliation of the cache against the
      log happens via `update-memory` on load; no instrument outside the kernel writes
      `core.md`, `log.md`, or `canon/`.
- [ ] **A session beat is well-formed** (§5) — appended (never edited in place), with a
      stable `session-id`, a `scope`, a `state` (`active` | `closing`), and a
      `last_active` heartbeat stamped on each write.
- [ ] **Hot pages are coordinated, not locked** — before deep-integrating an existing
      `canon/` page, a tab glances at `sessions.md` for a session already scoped to it;
      coordination is by lane and awareness (§7), not by a write-time lock.

A write made without regard to its class, or a cache "repair" that overwrites curated
prose or is performed outside the kernel, **fails** the protocol.

## Part B — the reconciler behaves correctly

`session-reconcile` ([`tools/session-reconcile`](../tools/session-reconcile)) must:

- [ ] **Compact only its own file** — rewrite `memory/sessions.md` to the latest beat
      per session-id; write nothing in the `canon/`/`core.md`/`log.md` tiers.
- [ ] **Drop clean closes, reap stale tabs** — a session whose last beat is
      `state: closing` is dropped (clean exit); a session whose `last_active` predates
      the staleness window with no close is reaped (the crashed tab).
- [ ] **Detect, not repair, cache drift** — report `core.md` lag against the log; treat
      lag **with a live session** as expected (`lag`, advisory, no gate) and lag with
      **no** live session as a possible lost write (`stale`, gates); it must **not**
      write `core.md`.
- [ ] **Be deterministic given (vault, now)** — the same file and same `--now` → byte-
      identical output and identical compacted file; equal-minute beats for one session
      resolve by a **total** tie-break (newer, then `closing` wins, then original file
      position), never by dict encounter order. The current time is an explicit input
      because reaping is relative to it; production runs against the wall clock.
- [ ] **Write atomically, single-writer-safe** — temp-then-rename via a process-unique
      temp name, so neither an interrupted run nor two simultaneous triggers (SessionEnd
      hook + periodic tick) leave a torn `sessions.md`.
- [ ] **Stay least-privilege** — no network, no credentials, local vault only; exit 0
      when nothing needed healing (incl. advisory `lag`), 1 on a stale reap or `stale`
      cache, 2 on error.

## Worked PASS example (a crash and a clean close, reconciled in one pass)

> Three tabs have been working. `tab-alpha` is live (`last_active` two minutes ago);
> `tab-bravo` crashed four hours ago (no `closing` beat); `tab-charlie` closed cleanly
> (last beat `state: closing`). `core.md`'s `updated` reads `14:00`, but the newest
> `log.md` entry is `14:30` — `tab-bravo` wrote the log before it died, but its
> `core.md` update was lost.
>
> `session-reconcile` runs (on the periodic tick): it **reaps** `tab-bravo` (stale — the
> crash backstop), **drops** `tab-charlie` (clean close), **keeps** `tab-alpha`,
> rewrites `sessions.md` to the one live beat (atomic), and reports the `core.md` cache
> as **`lag`** — "updated 14:00 lags latest log 14:30", *advisory*, because `tab-alpha`
> is live and mid-write. It exits **1** on the strength of the stale reap, not the cache
> lag. It does **not** touch `core.md`; the kernel reconciles the cache from the ledger
> on the next load, where the log wins. The crash left no lasting conflict.

*Why this is correct:* the crashed tab's coordination hint is cleared mechanically, the
clean exit needed no waiting, and the cache lag is surfaced for the owner of the write
(the kernel) rather than silently patched by the tool — and reported as advisory, not a
gate, because a live session makes lag expected.

## FAIL examples the layer must NOT produce

- **The tool writing `core.md`** — "repairing" the cache itself instead of reporting
  drift and leaving the write to the kernel (§4 — write-ownership breached).
- **Wholesale `core.md` rebuild** — regenerating the file from the log and destroying
  the curated prose (focus, threads, decisions), which is not log-derivable.
- **A write-time lock** — a tab acquiring a lock and making others block, presented as
  S15. True prevention is the **deferred broad scope** (§9), not this layer.
- **Claiming prevention** — describing the ~15' reconciler as *preventing* collisions;
  it is retrospective and **heals**, it does not prevent.
- **Editing a beat in place** — mutating an existing `sessions.md` beat instead of
  appending, reintroducing the collision the append-only note exists to avoid.
- **Cranking the cadence for safety** — shrinking the interval toward "prevention",
  which only races live writers and never crosses from retrospective to prospective.
- **Gating on in-flight lag** — treating a live session's expected `core.md` lag as
  drift and exiting non-zero on it; lag with a live session is normal, not a lost write.
- **Order-dependent compaction** — letting two equal-minute beats for one session
  classify by file order; the reduction must be a total, deterministic tie-break.
- **The tool reaching the open world** — any network call or credential use; gathering
  is an agent's job, never a tool's.
