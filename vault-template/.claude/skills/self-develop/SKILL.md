---
name: self-develop
description: Run one self-development audit pass that measures the brain's own graph health and capability gaps, triages them, and drives the owning layer to fix each. Use for the meta-loop that grows the platform ("audit the brain", "where is the graph weak", "run a growth pass", "self-develop"). The canonical procedure /grow and growth-agent compose. Drives Builder/Research/Thinking; never performs their work itself.
---

# self-develop: the brain's growth meta-loop

The canonical procedure for **Self-Development & Growth**
([`SELF-DEVELOPMENT.md`](../../../../SELF-DEVELOPMENT.md), the authority, Brain-OS
layer 6). One bounded pass that audits the brain's **own** condition and drives the
layers that fix it. You are the **judgement that points the hands**: you decide
*what* is weak and *who* mends it; you never link-propose, resolve, gather, or build
yourself (SELF-DEVELOPMENT §2).

## When to use

A deliberate or scheduled audit of the **platform**, not the knowledge, and so
distinct from a Thinking sweep ([THINKING §4](../../../../THINKING.md), which keeps
health metrics out and assigns them here). Use it to find orphans, stale edges,
unresolved contradictions, confabulation surfaces, hub or duplicate defects,
ontology-promotion candidates, and recurring capability gaps, then route each.

## Procedure: audit, triage, route, record

Follow [SELF-DEVELOPMENT §3](../../../../SELF-DEVELOPMENT.md) exactly. The pass is
**bounded**: report the top findings and stop; do not try to heal the whole graph.

1. **Audit.** Run the mechanical signals via the
   [`graph-health-scan`](../../tools/graph-health-scan) tool (orphans, stale edges,
   exact-duplicate titles, and open `edge/contradicts` tags, all deterministic, so
   cite its output). Reason out the judgement signals (hub overload and weak
   connectivity; semantic duplicates come from the model and retrieval substrate's
   duplicate finder as threshold-gated **candidates** once it is calibrated, which
   happens when you instantiate your brain, so until then reason them out;
   unsourced-and-unmarked claims, taken from Thinking's grounding re-trace,
   [THINKING §6.2](../../../../THINKING.md)). Scan for the two **owned** growth signals
   ([§5](../../../../SELF-DEVELOPMENT.md)): ontology-promotion candidates Thinking has
   surfaced, and recurring capability gaps across sessions.

2. **Triage / prioritise.** Rank by **damage to the graph** (a duplicate node
   fractures more than one orphan) and **cheapness of fix**. Keep a bounded top set.

3. **Classify each finding** to the acceptance bar
   ([growth-proposal-contract.md](../../tests/growth-proposal-contract.md), Part A):
   name the **signal**, the **evidence**, the **owner**, and the **tier** (§6).

4. **Route: drive the owning hand** ([§4](../../../../SELF-DEVELOPMENT.md) routing
   table). You dispatch; you do not fix:
   - orphan / weak connectivity → a **Thinking link pass** (§3.2);
   - stale edge → **kernel edge-work** (re-point/prune in integration);
   - unresolved `contradicts` → a **Thinking resolution-proposal** (§3.3), then the
     `[!contradiction]` flag for {{OWNER}};
   - unsourced-and-unmarked → a **research prompt** onto the `edge/inference` queue
     ([`research`](../research/SKILL.md) / `research-agent`, the research loop);
   - hub overload → a **Canon split** candidate, surfaced for {{OWNER}};
   - duplicate node → a **Canon merge** candidate, surfaced for {{OWNER}}.

5. **For the two owned decisions, prepare a proposal to the gate** (§6, tier 3).
   Ontology promotion and architecture edits **mutate shared meaning**, so you
   **propose build-complete, never apply** (growth-proposal-contract Part B): draft
   the *exact* edit (the `NODE-GRAPH.md` edge-vocabulary row, or the precise layer-doc
   change), validate it against the existing vocabulary and surrounding docs, evidence
   the recurrence, and queue it as a **Pulse decision** via the existing two-part flag
   (page callout plus `core.md` "Needs review", kernel §10). The engine doc stays
   **unchanged** until {{OWNER}} ratifies. A **systemic capability gap** is driven to
   Builder via [`/build`](../../commands/build.md); Builder's lifecycle and gate own
   the build (tier 2, build-then-record); you decide *that* it should grow, not *how*.

6. **Record.** Stamp the pass (what it found, what it dispatched, what it queued)
   through the kernel's **`update-log`** ([OPERATIONS-KERNEL §6/§8/§12](../../../../OPERATIONS-KERNEL.md),
   the append-only audit tier), so the brain's self-growth has a permanent,
   reviewable trail. You **compose** the capability; an autonomous worker
   ([`growth-agent`](../../agents/growth-agent.md)) hands the record off for the
   kernel to write, never writing `log.md` or `core.md` itself.

## Non-negotiable discipline

- **Drive, do not perform.** Routing a fix to its owner is the job; doing the fix
  yourself collapses the layer (SELF-DEVELOPMENT §2). If you wrote the link, resolved
  the contradiction, or built the instrument, you broke the lane.
- **Never silently change shared meaning.** Ontology and architecture edits are
  ratify-gated (§6); propose, queue, log, but never apply unasked.
- **Bounded pass.** Top findings, then stop and report. No loop to heal everything.
- **Mechanical signals come from the tool**, not the eye; judgement signals are
  reasoned and named as such.
- **Compose, add nothing.** No new kernel primitive and no new flag: the existing
  contract and the existing flag carry it.

## Output

A short report: the signals found (mechanical, with the scan output; and judgement),
the triaged top set, where each was routed, any proposals queued for ratification
(named as Pulse decisions), and the `log.md` entry written.
