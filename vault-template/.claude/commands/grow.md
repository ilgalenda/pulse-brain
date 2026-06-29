---
description: Run a self-development audit pass now, measuring the brain's own graph health and capability gaps, routing each weakness to the layer that fixes it, and reviewing any proposals queued for ratification.
argument-hint: [optional pillar or domain slice to scope the audit]
---

Run a **self-development audit pass** (the self-development capability; see
[`SELF-DEVELOPMENT.md`](../../../SELF-DEVELOPMENT.md)).

This is {{OWNER}}'s entry to the growth meta-loop. The *capability* belongs to the
Self-Development layer; this just invokes it (the same pass the scheduler runs
unattended, [`scheduling.md`](../scheduling.md)). It audits the **platform**, not the
knowledge, which makes it distinct from [`/sweep`](sweep.md), which reasons over content
([THINKING §4](../../../THINKING.md) keeps health metrics out and assigns them here).
Scope to `$ARGUMENTS` if given (a pillar or domain slice), otherwise audit the active
slice.

Run the [`self-develop`](../skills/self-develop/SKILL.md) skill. For an unattended
pass, spawn the [`growth-agent`](../agents/growth-agent.md). Per SELF-DEVELOPMENT §3,
the pass:
- runs [`graph-health-scan`](../tools/graph-health-scan) for the mechanical signals
  (orphans · stale edges · exact-duplicate titles · open `edge/contradicts` tags) and
  reasons out the judgement ones (hub overload · weak connectivity · semantic
  duplicates · unsourced-and-unmarked claims);
- triages to a **bounded** top set by graph damage and fix cost: it does not try to
  heal the whole graph;
- **routes** each finding to the owning layer (§4), whether Thinking, the kernel's
  edge-work, the `edge/inference` research queue, or a Canon split/merge candidate, and
  **drives** it; it never performs the fix itself;
- for the two owned decisions (ontology promotion · systemic capability gap), prepares
  a **build-complete** proposal and queues it as a **Pulse decision** for {{OWNER}}'s
  ratification (§6, tier 3); it **never** edits the ontology or a layer doc unasked;
- records the pass through the kernel's `update-log`.

Report back: the signals found (with the scan output), the triaged top set, where each
was routed and at which tier, and any proposals queued for ratification.
