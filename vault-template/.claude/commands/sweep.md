---
description: Run a Thinking sweep now — reason across a slice of the graph to generate synthesis, propose links, and work open inferences.
argument-hint: [optional domain or topic to focus the sweep]
---

Run a **Thinking sweep** (the S10 capability — see [`THINKING.md`](../../../THINKING.md) §4).

This command is S11's concrete entry for running Thinking unattended; the
*capability* belongs to the Thinking layer, this just invokes it. Scope to
`$ARGUMENTS` if given, otherwise sweep the active domain.

Per THINKING §4/§6.2, the sweep:
- reasons over **knowledge** (what connects/conflicts/emerges) — **not**
  graph-health metrics (those are S13);
- runs the **grounding re-trace** — surfaces any canon claim that is unsourced and
  unmarked (the missed-inference backstop);
- proposes synthesis and links, written freely; significant proposals surface via
  the existing flag (page callout + `core.md` "Needs review");
- respects the **core.md cap** — overflow rolls into a single line pointing at
  `log.md`.

Report back: synthesis/links proposed, inferences worked, and anything flagged for
review.
