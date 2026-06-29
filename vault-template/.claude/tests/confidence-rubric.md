# Fixture — the `confidence` rubric

Worked examples that pin down how a gather agent assigns `confidence`
(CONTEXT-ENGINE Dynamic §2). The rule: rate from **authority** (is the origin
reputable/primary?), **corroboration** (do independent sources agree?), and
**recency** (is it current for a claim that changes over time?) — and when unsure,
**rate down** (precision over optimism). These cases are the acceptance bar: an
agent that rates them differently is mis-calibrated.

## The rule in one line

`high` = authoritative/primary **and** (corroborated **or** self-evidently
factual) **and** current. `low` = weak on authority, uncorroborated, or stale.
`medium` = everything in between. **When torn between two grades, choose the lower.**

## Cases (source → expected rating → why)

| # | Source (illustrative, not live) | Expected | Why |
|---|---|---|---|
| 1 | A standards body's own published specification, current version | **high** | Primary, authoritative, current. |
| 2 | Two independent reputable outlets reporting the same figure | **high** | Corroborated across independent authorities. |
| 3 | A single vendor's marketing page making a self-interested claim | **medium** | Authored by an interested party, single-source, uncorroborated. |
| 4 | A dated blog post stating a figure that changes year to year | **low** | Stale for a time-sensitive claim, regardless of original authority. |
| 5 | An anonymous forum comment with no sourcing | **low** | No authority, no corroboration. |
| 6 | A reputable outlet, but the specific claim is unverifiable and uncorroborated | **medium** | Authority present, corroboration absent → rate down from high. |
| 7 | A primary regulatory filing, current, but dense/ambiguous on the exact point | **medium** | Primary & current, but the *specific* claim is not clearly supported → down. |
| 8 | Agent is genuinely unsure between medium and high | **medium** | Tie breaks **down**. |

## Downstream behaviour these ratings must trigger (Dynamic §2)

- **high** → integrate normally.
- **medium / low** → integrate as *reported, not established* (attributed in-line);
  must be **corroborated** before it hardens into a canon assertion.
- A **medium/low** source **never silently overwrites** an established canon claim
  — a conflict routes to the Canon §4 flag protocol.
- Confidence **travels with the claim** into canon until corroboration lifts it.

## Anti-patterns the agent must avoid

- Rating `high` because the source is *interesting* or *recent* alone (recency ≠ authority).
- Rating up to avoid the extra corroboration step (optimism over precision).
- Putting the trust judgement in prose instead of the structured field.
