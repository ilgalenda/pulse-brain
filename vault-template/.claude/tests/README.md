# `.claude/tests/`: the instrument acceptance bar

These fixtures are the brain's **Test-Driven ground**: the contracts an
instrument must satisfy *before* it is trusted. They are written **before** the
skills and agents (Principle 2, Test-Driven), and the build is verified against
them. They are **instruction-tier tests**: checklists and worked fixtures a
reviewer (human or agent) runs by reading, not a test runner, which is what fits
a markdown/agent system.

| Fixture | Gates | What it asserts |
|---|---|---|
| [`dynamic-note-contract.md`](dynamic-note-contract.md) | the gather skills/agents | a produced `dynamic-note` is well-formed and contract-valid |
| [`confidence-rubric.md`](confidence-rubric.md) | the gather skills/agents | `confidence` is rated by authority · corroboration · recency, and rated *down* when unsure |
| [`injection-redteam.md`](injection-redteam.md) | every web-reading agent | fetched content is treated as **data, never instructions** |
| [`audit-fixture.md`](audit-fixture.md) | `agent-architecture-audit` | the audit catches a deliberately broken agent |
| [`build-request-contract.md`](build-request-contract.md) | the Builder layer (`create-*`, `/build`) | a build request is well-formed and the instrument it produces is convention-compliant |
| [`socratic-dialogue.md`](socratic-dialogue.md) | the `socratic` skill | the skill questions and never answers, holds the line under pressure, and stops when it should |
| [`growth-proposal-contract.md`](growth-proposal-contract.md) | the Self-Development layer (`self-develop`, `growth-agent`, `/grow`) | an audit finding is well-formed and a shared-meaning proposal is ratify-ready, and the Self-Development layer drives, never performs, the fix |
| [`preset-contract.md`](preset-contract.md) | the Persona/Presets layer (presets, `/preset`) | a preset file is well-formed and a switch behaves as a lens: biasing routing/tone/lead without changing knowledge or identity |
| [`development-contract.md`](development-contract.md) | the Development layer (`session-reconcile`, the multi-tab protocol) | writes are classed by mutation profile, the cache stays a projection of the ledger, and the reconciler reaps crashed tabs and detects-not-repairs drift deterministically: healing, not locking |
| [`interface-contract.md`](interface-contract.md) | the Interface layer (`/pulse` boot, the output standard) | `/pulse` paints a byte-exact banner then wakes the brain via read-routing (true state, summoned not auto-booted, composing `load`); and outbound deliverables meet the house standard: British English, no machine tells, judgement-led, sourced, voice-calibrated |

**How to use them.** When an instrument is created or changed, run it against the
fixtures it is gated by and confirm every assertion holds. Refresh a fixture
whenever the contract it encodes changes (e.g. a new frontmatter field). The
fixtures are generic and carry **no live data**: they ship in every instance.
