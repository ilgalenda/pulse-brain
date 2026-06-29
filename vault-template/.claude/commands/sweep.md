---
description: Run a Thinking sweep now, reasoning across a slice of the graph to generate synthesis, propose links, and work open inferences.
argument-hint: [optional domain or topic to focus the sweep]
---

Run a **Thinking sweep** (the reasoning capability; see [`THINKING.md`](../../../THINKING.md) §4).

This command is the concrete entry for running Thinking unattended. The
*capability* belongs to the Thinking layer, and this just invokes it. Scope to
`$ARGUMENTS` if given, otherwise sweep the active domain.

Per THINKING §4/§6.2, the sweep:
- reasons over **knowledge** (what connects, conflicts, or emerges), not
  graph-health metrics (those belong to the self-development layer);
- runs the **grounding re-trace**, which surfaces any canon claim that is unsourced and
  unmarked (the missed-inference backstop);
- proposes synthesis and links, written freely; significant proposals surface via
  the existing flag (page callout plus a `core.md` "Needs review" entry);
- respects the **core.md cap**: overflow rolls into a single line pointing at
  `log.md`.

Report back: synthesis and links proposed, inferences worked, and anything flagged for
review.
