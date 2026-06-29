---
name: agent-architecture-audit
description: Full-stack diagnostic for agent and LLM applications. Audits the 12-layer agent stack for wrapper regression, memory pollution, tool-discipline failures, hidden repair loops, and rendering corruption. Produces severity-ranked findings with code-first fixes. Use to review an agent/skill/command, an autonomous loop, or any LLM-powered feature before trusting it — including the brain's own instruments.
---

# agent-architecture-audit

A full-stack diagnostic for agent and LLM applications. It inspects the **12-layer
agent stack**, reports **severity-ranked findings**, and gives a **code-first fix**
for each — the concrete edit, not just advice. Its first duty in the brain is to
audit the brain's own instruments (RESEARCH-AGENTS.md), but it audits **any** agent
application, autonomous loop, or LLM feature {{OWNER}} is building.

## Input

A target to audit: an agent/skill/command file, a set of them, or a described
agent application. Read the target(s) fully before judging.

## The 12-layer stack (inspect each)

1. **Identity & role** — one clear, single job?
2. **Instruction/wrapper integrity** — has a wrapper/system layer drifted from its
   contract? (*wrapper regression*)
3. **Tool surface & discipline** — tools scoped, least-privilege, used as intended?
   (*tool-discipline failures*; e.g. `tools: ["*"]`)
4. **Input trust** — external/fetched input treated as **data, not instructions**?
   (prompt injection)
5. **Memory & state** — explicit, bounded, uncontaminated? (*memory pollution*;
   e.g. "keep everything in context")
6. **Control flow** — any unbounded/hidden retry or repair loop? (*hidden repair
   loops*; e.g. "retry until it works")
7. **Output contract** — output conforms to a declared schema/contract?
8. **Rendering/serialisation** — well-formed output? (*rendering corruption*;
   broken callouts, malformed frontmatter, raw/again-escaped markup, truncation)
9. **Handoff** — routes specialist work out rather than doing it inline?
10. **Safety/secrets** — secrets via `.env`; safe defaults; bounded runs?
11. **Provenance/audit** — state changes logged and traceable?
12. **Termination** — every path ends; no runaway?

## Method

1. **Read** the target(s) in full.
2. **Walk the 12 layers**; for each, decide pass / finding.
3. **Rank** findings Critical → High → Medium → Low. Critical = unsafe to run
   (injection-obedience, hardcoded secrets, blanket tools + canon overwrite). High
   = will misbehave (unbounded loops, memory pollution). Medium = correctness/clarity
   (rendering, multi-job, wrapper drift). Low = hygiene (missing logging).
4. **Fix-first** — give the concrete edit for each finding.
5. **State the clean layers explicitly** — "no findings at Critical/High" is part
   of the report; silence is not a pass.

## Acceptance (Test-Driven)

This skill must pass [`tests/audit-fixture.md`](../../tests/audit-fixture.md): run
on that deliberately broken agent, it must surface every must-catch finding at the
stated severity, each with a code-first fix. Refresh against the fixture if the
stack or conventions change.

## Output

A severity-ranked findings report. Each finding: **layer · what's wrong · code-first
fix**. End with the cleared layers and an overall verdict (safe to run / fix
Criticals first / etc.).
