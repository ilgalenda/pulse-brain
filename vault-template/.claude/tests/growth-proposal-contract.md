# Fixture: the growth-proposal contract

The acceptance checklist the **Self-Development layer**
([`SELF-DEVELOPMENT.md`](../../../SELF-DEVELOPMENT.md)) must pass on every audit
pass. It has two halves. An **audit finding** must be well-formed before it is acted on,
and a **growth proposal** (raised when the finding touches shared meaning) must be
ratify-ready before it reaches {{OWNER}}. This restates the meta-loop
(SELF-DEVELOPMENT §3), the routing table (§4), and the three-tier autonomy gate (§6)
as a *test*, not a new authority. If any item fails, the audit is not yet correct.

## Part A: a well-formed audit finding

Before the Self-Development layer acts on a finding, it answers:

- [ ] **The signal**: which [NODE-GRAPH §6](../../../NODE-GRAPH.md) health signal or
      owned growth signal (§5) this is, named exactly (orphan · weak connectivity ·
      stale edge · unresolved `contradicts` · unsourced-and-unmarked · hub overload ·
      duplicate node · ontology-promotion candidate · systemic capability gap).
- [ ] **The evidence**: what surfaced it, either a `graph-health-scan` line (for a
      mechanical signal) or the reasoning (for a judgement signal). A mechanical
      signal cites the tool; the LLM does not re-decide it by eye.
- [ ] **The owner**: the layer that owns the fix (§4 routing table). The Self-Development
      layer dispatches there; it does **not** name itself as the fixer for a routed signal.
- [ ] **The tier**: which autonomy tier this falls in (§6), whether *free* (route to a
      flag-don't-gate lane), *build-then-record* (drive Builder), or *ratify*
      (mutates shared meaning).
- [ ] **Triaged, not exhaustive**: the finding earned a place in a **bounded** top
      set ranked by graph damage and fix cost; the pass did not dump every signal.

A finding missing the signal, the owner, or the tier is **not actionable**: the
Self-Development layer does not act on an unclassified finding.

## Part B: a ratify-ready growth proposal (tier 3 only)

When the finding mutates shared meaning, whether an **ontology promotion** or an
**architecture edit** (§5/§6), the proposal {{OWNER}} sees satisfies:

- [ ] **Build-complete**: the *exact* edit is drafted (the precise `NODE-GRAPH.md`
      edge-vocabulary row, or the precise layer-doc change), not a vague "we should
      add an edge type". Ratification is a one-glance yes/no, not work for {{OWNER}}.
- [ ] **Validated against the frame**: the draft was checked against the existing
      edge vocabulary and the surrounding docs, so it does not duplicate a named edge,
      contradict another layer, or break a seam.
- [ ] **Evidenced as recurring**: for an ontology promotion, the provisional to
      recurring history is shown ([NODE-GRAPH §3.3](../../../NODE-GRAPH.md)), so the
      relation appears across several nodes, not once.
- [ ] **Surfaced as a Pulse decision**: queued via the **existing** two-part flag
      (page callout plus `core.md` "Needs review", kernel §10), not a new queue, and
      recorded in [`log.md`](../../../OPERATIONS-KERNEL.md).
- [ ] **Not applied**: the engine doc is **unchanged** until {{OWNER}} ratifies. The
      brain proposes; it never silently rewrites its own ontology or architecture.

## Worked PASS example (an audit pass leading to a routed fix and a ratified proposal)

> **Finding 1 (free tier).** Signal: *orphan*. `graph-health-scan` reports
> `canon/some-page.md` with empty `links` and absent from every other row's `links`.
> Owner: Thinking link-proposal ([§3.2](../../../THINKING.md)). Tier: free, because the link
> pass flag-don't-gates. **Action:** the Self-Development layer drives a Thinking link pass over the orphan;
> logs the dispatch. Done, with no ratification needed.
>
> **Finding 2 (ratify tier).** Signal: *ontology-promotion candidate*. Thinking has
> surfaced a `depends-on` relation expressed in prose across five pages. Tier:
> ratify (it mutates the edge vocabulary). **Proposal:** the exact new row for
> `NODE-GRAPH.md §3.2` is drafted, checked against the seeded edges (no collision),
> the five occurrences are cited, and it is queued as a Pulse decision in
> `core.md` plus `log.md`. `NODE-GRAPH.md` is **not edited**. {{OWNER}} ratifies, *then*
> the row lands.

*Why two tiers in one pass:* the orphan fix is additive and reversible, so it just
runs; promoting an edge type changes the frame every layer reads, so it waits for a
human in the transition.

## FAIL examples the audit must NOT produce

- **The Self-Development layer performing the fix**: writing the missing link, resolving the contradiction,
  filing the research note, or building the instrument *itself* instead of driving the
  owning layer (§2: it points the hands, it is not the hands).
- **A silent shared-meaning change**: editing `NODE-GRAPH.md`'s edge vocabulary or a
  layer doc without ratification (§6 tier 3 collapsed into build-then-record).
- **A vague proposal**: "we should add an edge type" with no drafted edit, forcing
  {{OWNER}} to do the work ratification was meant to make cheap.
- **An unbounded pass**: dumping every signal in the graph instead of a triaged top
  set, or looping to heal the whole graph in one run.
- **A mechanical signal re-decided by eye**: claiming an orphan, stale-edge, or duplicate
  finding without the `graph-health-scan` line behind it.
- **Health metrics in the content sweep**: computing graph health inside a Thinking
  sweep ([THINKING §4](../../../THINKING.md) keeps them out; they belong here).
