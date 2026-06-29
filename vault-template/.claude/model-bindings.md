# Model bindings — role → model (INSTANCE CONFIG)

The brain's **model-routing policy**: which model each *role* runs on. The deterministic
[`resolve-model`](tools/resolve-model) tool reads this file; the Builder consults it when
it stamps a new instrument's `model:` ([`instruments.md` §1](instruments.md),
[BUILDER.md §4](../../BUILDER.md)). It realises the kernel's `model-route` hook
([OPERATIONS-KERNEL.md §11](../../OPERATIONS-KERNEL.md)); the authority is
[MODEL-RETRIEVAL.md §2](../../MODEL-RETRIEVAL.md).

> **This is INSTANCE config — the engine ships it commented/placeholdered, never
> populated.** Concrete model ids are filled at instantiation (S19), like the watchlist
> and presets. A role with no binding falls back to the **session model** (the kernel
> rule: absent a declaration, the session model is used). The main conversation loop's
> model is {{OWNER}}'s choice (`/model`) — this file cannot set it; it routes *workers*.

## How to populate (at S19)

Uncomment a line and set a concrete model id. Format: `- <role>: <model-id>` (one role
per line). The main loop is documented, not bound (the resolver routes workers, not the
loop).

## Recommended tiering (the documented exemplar — see MODEL-RETRIEVAL.md §2.4)

The rationale, not a binding: the model is rented, so tier it by the work, never trading
loop quality for cost.

- **Main loop → strongest model (recommended: Opus).** Owns integration, synthesis,
  partner judgement, and the canon/log writes — kernel-owned, non-delegable, highest
  stakes. Set via `/model`; not bound here.
- **Worker roles → tier by the task:**

```
# --- worker bindings (uncomment + set concrete model ids at S19) ---

# reasoning:   <strong-model>     # complex multi-source synthesis, hard analysis
# synthesis:   <strong-model>     # canon synthesis-page reasoning handed back to integrate
# review:      <strong-model>     # adversarial hostile-review — send the strongest model to attack
# promotion:   <strong-model>     # ontology-promotion reasoning (candidates only)

# research:    <balanced-model>   # routine research-cycle synthesis (default worker)
# monitor:     <balanced-model>   # most monitoring-beat reasoning
# draft:       <balanced-model>   # dynamic-note / deliverable drafting

# extraction:  <fast-model>       # pull structured fields from a fetched source
# dedup:       <fast-model>       # mechanical format / duplicate checks
# triage:      <fast-model>       # "is there new material?" monitor beats

# embedding:   <embedding-model>  # the Half-B semantic substrate (MODEL-RETRIEVAL.md §3)
```

Roles are open: add a row when a real instrument needs one. Keep names the role's one job
(`extraction`, not `helper`). A role absent here resolves to the session model, so the
brain always runs — populating this file *tunes* routing, it is never a prerequisite.
