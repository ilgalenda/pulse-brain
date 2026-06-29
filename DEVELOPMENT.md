# Pulse_Brain: Development

Brain-OS **layer 8**: how the brain is **operated and evolved across multiple
concurrent CLI tabs** over one shared local vault. Several sessions run at once,
each integrating, researching, or building on {{OWNER}}'s behalf against the same
files on disk, and this layer is the discipline that keeps them from colliding,
and the workflow for developing the brain itself.

This is an **instruction (+ light tooling)** layer ([BRAIN-OS instruction-vs-code map](BRAIN-OS.md)):
a protocol the LLM follows, plus one deterministic helper. It introduces **no new
kernel primitive**: it composes `update-memory`, `update-log`, and `load`
([OPERATIONS-KERNEL §12](OPERATIONS-KERNEL.md)) and adds one operational artifact
(`sessions.md`) and one tool (`session-reconcile`). It is the formal protocol that
the kernel's *safe-by-default* concurrency posture ([§10](OPERATIONS-KERNEL.md)) and the
Research layer ([RESEARCH-AGENTS §5](RESEARCH-AGENTS.md)) had deferred to this layer.

## 1. What this layer is: coordinate and heal, don't lock

The working pattern is fixed ([ARCHITECTURE §4](ARCHITECTURE.md)): one shared brain
on one machine, many CLI tabs. This is **local-filesystem coordination**, not
distributed consensus, and the design choice that follows is deliberate:

> Concurrent operation is made **safe by construction and self-healing**, not
> **prevented by locking**.

Genuine *prevention*, where a tab acquires a lock before it writes and another backs
off, needs synchronous, write-time coordination. That is real machinery with real
failure modes (stale locks, deadlock, a crashed holder), and it is **deferred to the
broad scope** (§9). What this layer guarantees instead is weaker and sufficient:
collisions are made **rare** (by how shared state is shaped and how tabs work) and
**recoverable** (because the append-only ledger is the truth, every clobber heals).
The reconciler **heals; it does not prevent**. Naming that honestly matters, because
the one place false confidence is unaffordable is {{OWNER}}'s knowledge.

## 2. Lanes: what this layer owns, and what it doesn't

- **Owns** the write-class protocol (§3), the ledger guarantee (§4), the session
  presence note (§5), the `session-reconcile` tool (§6), and the develop-the-brain
  working discipline (§7).
- **Composes** the kernel: the append-only `log.md` ledger, `update-memory` for
  `core.md`, and graph-first `load`. The kernel still owns every `canon/`, `core.md`,
  and `log.md` write; this layer coordinates around that ownership, it does not take
  it.
- **References** the Research layer's safe-by-default posture
  ([RESEARCH-AGENTS §5](RESEARCH-AGENTS.md)) that it formalises, and `graph-health-scan`
  ([SELF-DEVELOPMENT §7](SELF-DEVELOPMENT.md)), whose lane is *graph/index* integrity
  while this layer's is *session/cache* integrity. They do not overlap.
- **Defers** (the broad seam, §9) write-time leasing (true prevention), automated
  conflict detection, and semantic merge arbitration of two genuinely-divergent
  `canon/` edits.
- **Does not** lock writes, perform any knowledge edit, or write `canon/`/`core.md`/
  `log.md` itself. The one tool writes only its **own** file (`sessions.md`).

## 3. The write-class taxonomy: safety by mutation profile

Concurrency safety is a function of an artifact's **mutation profile**, the same
axis the Immutability principle ([PRINCIPLES.md](PRINCIPLES.md)) and the autonomy
gate ([SELF-DEVELOPMENT §6](SELF-DEVELOPMENT.md)) already turn on. Every write the
brain makes falls into one of three classes:

| Class | Artifacts | Collision profile | Protocol |
|---|---|---|---|
| **Append-only / new-file** | `log.md`, a new `dynamic/` or `inbox/` source note, a brand-new `canon/` page, an appended `sessions.md` beat | collision-free by construction (distinct files, or order-independent appends) | write freely; no coordination |
| **Reconcilable cache** | `core.md` | last-writer-with-care, but a pure projection of the ledger for its derivable fields | never blind-overwrite; the kernel reconciles it against the log (§4) |
| **Co-edited shared meaning** | an existing "hot" `canon/` page two tabs both integrate; the `_index.md` / `index.md` edge-maps | genuine clobber (two reconciliations of the same file) | working-lane discipline (§7) makes it rare; the session note (§5) makes it visible; the ledger makes it recoverable |

The rule that makes the first row hold across the whole brain: **prefer append and
new-file over in-place edit for shared state.** It is why `log.md` was append-only
from the start, why a dynamic-note is always a new file, and why `sessions.md` (§5) is
append-only too. Collision-safety is designed in, not enforced after.

## 4. The ledger guarantee: the log is truth, core is a cache

The load-bearing safety property:

> `log.md` is the **ledger**: append-only, the immutable record of every meaningful
> change. `core.md` is a **cache**, a compact snapshot for fast load. The cache is
> rebuildable from the ledger, so a clobbered `core.md` is always **recoverable,
> never lost**.

This splits `core.md` into two regions with different handling:

- **Derivable anchors:** `active_preset` (the last preset switch in the log),
  `updated` (the newest log timestamp), and the **`## Needs review`** list (the
  review-flags, the flagged-minus-resolved contradictions in the log). These are a
  pure *projection* of the ledger. If they disagree with the log, the **log wins**.
- **Curated prose:** `Current focus`, `Live threads`, `Recent decisions`. These are
  editorial, not mechanically derivable from the log, and are **never machine-
  rewritten**. They are ordinary last-writer-with-care text; a clobber here loses at
  most a session's framing, which {{OWNER}} restores, and which the ledger's recent
  entries inform.

**The kernel owns the repair.** On load, read-routing already reads `core.md` first
([§7.1](OPERATIONS-KERNEL.md)) and the log is available; when the derivable anchors
drift from the log, the kernel reconciles them via `update-memory`, its own
capability, in its own tier. This layer specifies *that* the cache reconciles against
the ledger; it does not move the write out of the kernel. The reconciler tool (§6)
only **detects and reports** that drift; it never writes `core.md`.

## 5. Session presence: the `sessions.md` note

A lightweight, **append-only** note at [`memory/sessions.md`](vault-template/memory/sessions.md)
gives concurrent tabs awareness of one another. Each tab, on start and as it works,
**appends a beat**:

```
## <session-id> — <YYYY-MM-DD HH:MM>
- scope:      the domain / pillar / page this tab is working (e.g. canon/entities, or a slice)
- state:      active | closing
- last_active: <YYYY-MM-DD HH:MM>   # stamped when this session writes; its heartbeat
```

Two disciplines use it:

- **Glance before a hot integration.** Before deep-integrating an existing `canon/`
  page, a tab scans the note for another session already scoped to it, and either
  picks a different page or coordinates. This is how the *co-edited shared meaning*
  class (§3) is kept rare.
- **Heartbeat by activity.** `last_active` is stamped whenever the session writes
  (it is already touching files), so a live tab stays fresh and a dead one goes
  stale. A clean exit appends a final `state: closing` beat. Because the heartbeat is
  coarse (a tab deep in one long integration may not write for many minutes), the
  staleness window is deliberately **generous** (default 60′) and must exceed a
  realistic quiet-but-live span; the clean-exit beat, not the timeout, is the
  authoritative "gone" signal, and the timeout is only the crash backstop.

Concurrent **appends** never collide with one another: the file is the append-only
*ledger* of presence, and its compacted current view is produced by the tool (§6). The
compaction is a full rewrite, so it is **best-effort** against a beat that lands during
the rewrite itself: such a beat may be dropped and is simply re-announced on the tab's
next heartbeat. This costs nothing; like a falsely-stale reap, it clears at most a
coordination *hint*, never state. (Eliminating even that window is the broad-scope
seam, §9; it is not needed for an advisory note.)

## 6. The reconciler: `session-reconcile` (the one tool)

One deterministic helper ([`tools/session-reconcile`](vault-template/.claude/tools/session-reconcile),
the tool kind, [BUILDER.md §3](BUILDER.md)), built via `create-tool`, dogfooding the
Builder layer as `graph-health-scan` did. Its single job is to **keep concurrent
sessions consistent**, in two confined operations:

- **Compact `sessions.md`** (its own file, read-write). Keep the latest beat per
  session-id; drop sessions that posted `state: closing`; reap sessions whose
  `last_active` is older than a staleness window (the crashed / abruptly-closed tab).
  Atomic write (temp-then-rename) so an interrupted run never leaves a torn file.
- **Detect and report `core.md` staleness** (read-only over `core.md` + `log.md`). The
  deterministic proxy is the timestamp: `core.md`'s `updated` lagging the newest
  `log.md` entry. But a live session mid-integration appends to the log *before* the
  kernel flushes `core.md` (kernel §8/§10), so lag **with a live session is expected**,
  reported as `lag`, advisory, no gate. Lag with **no** live session is a possible lost
  write, reported as `stale`, with a non-zero exit so a caller can gate. Either way the
  tool only flags: *which* derivable anchor (§4) to correct, and the correction itself,
  are the kernel's on next load. The tool never writes `core.md`.

Discipline, mirroring `graph-health-scan`: **deterministic** given `(vault, now)`.
The current time is an explicit input because reaping is relative to it; in production
both triggers run against the wall clock, and `--now` is supplied only for reproducible
tests. **Local only, no network and no credentials.** And by **principle** it writes
only *operational coordination state*, never a knowledge or continuity tier: the kernel
owns every `canon/`/`core.md`/`log.md` write (§4), and the tool owns only the ephemeral
`sessions.md` presence note. Index/edge-map integrity is **not** its job; that is
`graph-health-scan`'s lane.

**Two triggers** (wired at instance time, §8):

- **`SessionEnd` hook:** on a clean tab close, the tool runs once: the session's
  `closing` beat is compacted away immediately, so the common case self-heals with
  **zero window**.
- **Periodic tick (~15'):** the backstop for the *unclean* case: a crashed, killed,
  or slept tab never runs its hook, so only an external sweep can reap its stale beat.

The interval stays loose precisely *because* the hook handles clean exits. Shrinking
it does **not** approach prevention: the tool is retrospective (it acts after writes
land), prevention is prospective (it acts at write time). They are different
mechanisms, not two ends of one dial. And a high-frequency sweep would begin racing
live writers (reading a half-written file), making it *less* safe, not more.

## 7. Developing the brain across tabs: the working discipline

The layer's second charter clause: how {{OWNER}} (with Claude) actually *operates and
evolves* the brain when several tabs are open. The principle is to make collisions
rare by **how you work**, not only by how the files are shaped:

- **One lane per tab.** Give each tab a distinct job: one integrating sources, one
  running research, one building an instrument. Lanes rarely touch the same page, so
  the *co-edited shared meaning* class (§3) seldom arises. Cross-lane coordination
  goes through the session note (§5), not through editing the same file at once.
- **Append-heavy.** Favour the append/new-file class for shared state; let the kernel
  serialise the in-place edits (`canon/` reconciliation, the edge-maps) within its own
  integration step.
- **Develop the engine section by section.** The engine is a git repo; brain
  development follows the project discipline: each section planned with `/plan`,
  pressure-tested before commit, one commit per section, linear history,
  committed only on {{OWNER}}'s explicit ask. Concurrent tabs build *different*
  sections or *different* instruments, never the same file.

This is the workflow half of "operated and evolved across concurrent tabs"; the
write-class protocol (§3 to §6) is the safety half. Together they let the brain be built
and run from many tabs without stepping on itself.

## 8. Security & the engine/instance boundary

- **The engine ships the template, not the runtime.** `sessions.md` ships as an empty,
  placeholdered template; live session beats are **instance runtime state**, created
  on the machine and **never committed**, like `log.md` and `core.md` content.
- **Triggers are instance wiring.** The `SessionEnd` hook and the ~15' cron live in the
  instance's `settings.json` / scheduler ([`scheduling.md`](vault-template/.claude/scheduling.md)),
  set when you instantiate your brain. Nothing runs on a backend in the engine; there is no
  live vault yet. Consistent with [RESEARCH-AGENTS §5](RESEARCH-AGENTS.md).
- **The tool is least-privilege.** No network, no credentials, deterministic, and
  confined to its own file. It cannot exfiltrate, reach the open world, or mutate the
  knowledge tiers.
- **Immutability holds.** `sessions.md` is append-only; compaction drops superseded
  beats but rewrites no provenance or log tier. The ledger is never edited.

## 9. Seams

- **→ Operations Kernel:** composes `update-memory` / `update-log` / `load` and adds
  no primitive; the `core.md`-from-log repair (§4) is the kernel's write, this layer
  only specifies and detects it.
- **↔ Research & Background Agents:** this layer is the **full protocol** that
  [§5](RESEARCH-AGENTS.md)'s safe-by-default posture deferred; background workers now
  coordinate through the session note and the reconciler.
- **↔ Persona / Presets:** concurrent tabs may each run a different preset over the
  one vault; the `active_preset` anchor is a derivable cache field (§4), so the
  question [PERSONA-PRESETS §9](PERSONA-PRESETS.md) handed to the concurrency layer
  (coordinating on `core.md` without colliding) is answered here.
- **↔ Self-Development:** `graph-health-scan` owns *graph/index* integrity; this
  layer's `session-reconcile` owns *session/cache* integrity. Distinct tools, distinct
  lanes, no overlap.
- **→ broad scope (deferred):** write-time leasing for true *prevention*, automated
  conflict detection, and merge arbitration of divergent `canon/` edits. The write-
  class taxonomy (§3) is the seam they slot into; none is built now.
- **Identity (cross-cutting):** coordination is mechanical; it never touches the
  dual-role identity or the one voice to {{OWNER}}.

> **Development complete.** The brain now runs across many concurrent CLI tabs over one
> shared vault without colliding: shared state is append-only and collision-safe by
> construction, `core.md` is a cache the kernel rebuilds from the immutable log, a
> lightweight session note keeps tabs aware of one another, and one deterministic
> reconciler reaps dead sessions and surfaces drift, on clean exit instantly and on a
> loose periodic backstop for crashes. It heals rather than locks; true prevention is
> the named broad-scope seam. Next on the roadmap is the **Interface** layer.
