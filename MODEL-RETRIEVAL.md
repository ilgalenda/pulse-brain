# Pulse_Brain — Model & Retrieval Substrate

Brain-OS **layer 10**: the **ML engine room** beneath the kernel — the *models the
brain runs on* and the *semantic retrieval* over the wiki. Everything above it (the
kernel, the Context Engine, the active layers) is **instruction**; this layer is the
one pure **code** tier ([BRAIN-OS instruction-vs-code map](BRAIN-OS.md)). It is where
the Builder layer deliberately deferred the heavy code substrate — embeddings, a vector
store, multi-model orchestration ([BUILDER §3](BUILDER.md)).

It introduces **no new kernel primitive**. It *realises* two hooks the kernel already
left open:

- **`model-route`** ([OPERATIONS-KERNEL §11/§12](OPERATIONS-KERNEL.md)) — the kernel is
  model-pluggable; a route or agent *may declare* its model, else the session model is
  used. This layer turns that declaration hook into a deterministic resolver and a
  documented tiering policy.
- **the semantic tie-breaker slot** ([OPERATIONS-KERNEL §7.5](OPERATIONS-KERNEL.md),
  [NODE-GRAPH §5](NODE-GRAPH.md)) — read-routing reserves "semantic similarity is added
  later by the Model & Retrieval Substrate." This layer fills it with embedding-based
  **re-ranking**, and adds the **semantic/vector edges** the Node-Graph seam
  ([NODE-GRAPH §4/§9](NODE-GRAPH.md)) names as S17's.

> The model is **rented**; the graph is **owned**. This layer makes the rented model
> pluggable and the owned graph searchable — without letting retrieval displace the
> compiled wiki. "Build Pulse as an ML" means an **LLM + RAG, multi-model** system whose
> compounding node-graph is the moat, not a bespoke trained model.

## 1. The defining boundary — re-rank, never retrieve-instead-of-compile

Pulse's defining idea is **compile, don't retrieve** ([OPERATIONS-KERNEL §5](OPERATIONS-KERNEL.md)):
the LLM maintains a living wiki; reading means reading the compiled synthesis, not
re-deriving it per query. S17 adds *retrieval machinery*, so the boundary must be
**enforced, not asserted**:

- **Re-ranking only.** Semantic similarity **re-orders the candidate set the bounded
  graph walk already surfaced** ([OPERATIONS-KERNEL §7.4 → §7.5](OPERATIONS-KERNEL.md)).
  It adds **no recall** — there is no parallel retrieval path that surfaces graph-distant
  pages the walk missed. A capped recall-expansion path was considered and **rejected**:
  it is a second answer surface that bypasses the graph, which §5 and "precision over
  recall" ([§9](OPERATIONS-KERNEL.md)) resist, and it routes around the moat
  ([NODE-GRAPH §1](NODE-GRAPH.md): a note is only as valuable as its edges).
- **A graph-distant similar is an edge-candidate, not a result.** When the substrate
  notices a page that is semantically near the task but not reachable by the walk, it
  emits a **Thinking edge-candidate** ([NODE-GRAPH §3.3](NODE-GRAPH.md) provisional →
  [§8](NODE-GRAPH.md) Thinking proposes the edge), never an injection into read-routing.
  The doctrine's fix for a relevant-but-distant page is **edge-work**, not a vector
  bypass.
- **The wiki stays the answer surface.** Embeddings index the **compiled wiki** (canon
  entity/topic/synthesis pages), not raw sources as a retrieval target. Source notes are
  **never** an answer surface ([OPERATIONS-KERNEL §2](OPERATIONS-KERNEL.md)); if they are
  embedded at all it is for integration-time de-duplication only (§3.5 below).
- **Similarity edges are candidates.** Embedding-derived edges are surfaced for the
  Thinking layer to propose and for {{OWNER}} to ratify ontology promotion
  ([NODE-GRAPH §3.3](NODE-GRAPH.md)) — **never auto-written** into canon.

## 2. Half A — model orchestration (multi-model)

### 2.1 The runtime truth that scopes it
Pulse runs **inside Claude Code**. The **main conversation loop's model cannot be
swapped mid-turn** — that is not a surface the runtime exposes. The only real model-swap
surfaces are a **subagent's `model:` frontmatter** and the **`model` parameter when an
orchestrating skill spawns a worker**, both at **whole-task (subagent) boundaries**. So
orchestration is not a runtime interceptor; it is *which model each instrument declares
and each spawn requests*.

### 2.2 The resolver — `model-route` made real
The `model-route` primitive is realised as a deterministic **tool**,
[`tools/resolve-model`](vault-template/.claude/tools/resolve-model):
`resolve(registry_file, role) → model`. It reads a **bindings file** and a role and
returns the model; it reads **no session state** (`core.md` is a lagging cache —
[OPERATIONS-KERNEL §10](OPERATIONS-KERNEL.md) — and reading it would break determinism,
exactly as `session-reconcile` takes `--now` rather than the wall clock). The caller —
the Builder, or a future orchestrator — passes the session model / active preset *in*.
It is a plain Builder `tool` (deterministic, no network, no credentials), not substrate.

**Consumer that exists today:** the Builder's `create-agent` lifecycle calls the
resolver when it stamps a new instrument's `model:` ([BUILDER §4](BUILDER.md), "enforce
conventions"). **Deferred consumer:** an orchestrating skill that spawns model-bound
workers — no such orchestrator ships yet, so it is built on real need via the Builder
([BUILDER](BUILDER.md)), not posited here.

### 2.3 The bindings — instance config, not engine content
The role→model bindings are **instance config**, like the watchlist
([RESEARCH-AGENTS §5](RESEARCH-AGENTS.md)) and presets
([PERSONA-PRESETS.md](PERSONA-PRESETS.md)): the engine ships a **generic, commented
template**; the populated bindings are stamped at instantiation (S19). The binding
*rule* — what `model:` a new instrument receives — lives in
[`instruments.md` §1](vault-template/.claude/instruments.md) (the Builder's existing
authority over instrument frontmatter), not in a parallel registry here.

### 2.4 The recommended tiering (the documented exemplar)
The engine ships this as **rationale**, generic and figure-free:

- **Main loop = Opus.** The loop owns integration, synthesis, partner judgement, and the
  canon/`log.md` writes — which are **kernel-owned and non-delegable** (workers gather
  and hand off; only the loop writes canon). That is the hardest, highest-stakes work and
  it *cannot* be escalated to a worker, so it runs on the strongest model. The loop's
  model is {{OWNER}}'s choice (`/model`); the template **documents** Opus as recommended,
  it does not force it (the resolver cannot set the main loop).
- **Worker tiers:** `reasoning` / `synthesis` / hostile-review / ontology-promotion →
  **strong (Opus)**; the default worker (routine research synthesis, dynamic-note
  drafting, audit sweeps, most monitor reasoning) → **balanced (Sonnet)**; `extraction` /
  dedup / format-checks / "is there new material?" monitor beats → **fast (Haiku)**.
- **Why not all-Opus or all-Sonnet:** all-Opus pays a large premium for mechanical work
  that gains nothing from it; Sonnet-on-the-loop permanently caps the core loop's
  judgement. Tiering is how the brain uses the rented model economically **without
  touching loop quality**.

### 2.5 Caching discipline (the cost lever that does not trade quality)
Prompt caching is **per-model** — switching models invalidates the cache. Two rules
follow:

- **Swap only at subagent boundaries.** A cheap worker runs in its own context, so it
  never invalidates the loop's cache. Fine-grained swapping would *cost* tokens, not save
  them.
- **Keep the always-loaded prefix stable and first.** `core.md`, the canon index, and
  pinned core pages are the cacheable prefix; cache-reads are a small fraction of input
  cost, so caching the prefix is the single largest steady-state saving — and it matters
  **more** as the prefix grows. The **minimum cacheable prefix differs by model**, so a
  cheaper worker can silently forfeit caching a prefix that cached on the loop — another
  reason to swap only at task boundaries.

The cost model is two levers: **cache the stable prefix** and **tier the workers**.
Together they reduce spend substantially against an all-strong-model, no-caching baseline
with loop quality unchanged. The engine documents the **levers and the reasoning** only —
never modelled figures or usage volumes, which are instance-specific.

### 2.6 What model orchestration is *not* (deferred, named)
- **Multi-provider chat plumbing** (calling non-Claude chat providers) stays deferred;
  the brain already runs on the session model, and S17 formalises *selection*, not new
  chat network calls. Exposing Pulse as an external MCP server is **S18**.
- **A self-tuning routing loop is not built.** Per-route cost/rework telemetry is **not
  capturable at the instruction tier** (no kernel `measure` primitive; tools are
  network/credential-forbidden; `log.md` records graph shape, not execution cost), and
  "model used / cost" is **not a node-graph property**, so it cannot be a
  [NODE-GRAPH §6](NODE-GRAPH.md) health signal. What is honest: the Self-Development
  layer's `growth-agent` may *qualitatively notice* a recurring routing miss in-session
  and **drive** an instance-config edit to the bindings (an instance-local change, not a
  shared-meaning one). Minting a real routing-signal *type* into the Node-Graph ontology
  is itself a tier-3 propose→ratify act ([SELF-DEVELOPMENT §6](SELF-DEVELOPMENT.md)) —
  named here as deferred scope, not built. No bespoke model-monitor agent (it would
  collide with `growth-agent`'s charter).

## 3. Half B — semantic retrieval (the substrate shell)

Built **lean and design-first**, the same discipline S16 used: the parts whose behaviour
is a function of the live content distribution defer to the live vault (S19), because
that distribution cannot enter the engine (the data boundary). What ships now is the
**deterministic shell**; what defers is calibration.

### 3.1 The embedding interface — provider-agnostic, local-first
A pluggable interface (the `embedding` role of `model-route`) with a **local default
adapter** and an **API adapter** (key via the credential map) as an opt-in upgrade.
Adapter swap preserves the interface. Honest framing: the local adapter is
**zero-API-config** (no key, content stays on-device — the tightest fit with the data
boundary), **not zero-install** — it needs a dependency install and a one-time model
pull (§3.6).

### 3.2 The vector store — an eventually-consistent derived cache
The store is a **derived cache of canon, never authoritative** — canon always wins. This
mirrors the kernel's `core.md`-cache / `log.md`-ledger model
([OPERATIONS-KERNEL §10](OPERATIONS-KERNEL.md)): a corrupted or stale store is always
**rebuildable from canon**. Embedding is **out-of-band** — it is *not* part of the
same-step integrity rule ([OPERATIONS-KERNEL §8](OPERATIONS-KERNEL.md)), because that
rule is synchronous and instruction-tier while embedding needs the substrate's
dependencies. Incremental **content-hash keying** avoids re-embedding unchanged pages.

**Staleness is a first-class read-time guard.** Canon pages are revised in place on
routine integration ([CONTEXT-ENGINE Canon §3/§6](CONTEXT-ENGINE.md)), so the store lags
canon between reindexes. A candidate whose **stored hash ≠ the page's current hash** is
treated as **stale — graph order wins** for that candidate, and the staleness is surfaced
*advisory* the way `session-reconcile` reports `core.md` lag (no gate, visible). A stale
vector never silently demotes a freshly-correct page.

### 3.3 Concurrency — a third integrity lane S15 does not cover
`session-reconcile` writes only `sessions.md`; the vector store is **new shared multi-tab
state** ([DEVELOPMENT §6](DEVELOPMENT.md) is explicit that index integrity is not its
job). The store is therefore written **single-writer-safe by construction**: per-page
**shards** keyed by page-id + content-hash (append / new-file — the collision-free write
class, [DEVELOPMENT §3](DEVELOPMENT.md)), and a **single atomic full-rebuild**
(temp-then-rename, the `write_atomic` precedent in `session-reconcile`) as the only writer
of any whole-store artifact. Two tabs reindexing at once cannot tear the store.

### 3.4 Re-ranking + the candidate-emission contract
Given the candidate set from the graph walk, the substrate returns a **re-ordering** by
similarity (subject to the staleness guard). It never adds candidates the walk did not
surface (§1). A graph-distant similar it happens to notice is emitted **separately** as a
Thinking edge-candidate, in the existing tag/`related` representation
([NODE-GRAPH §3.2/§3.3](NODE-GRAPH.md)) — never as a new edge type until promoted via
Self-Development.

### 3.5 The semantic-duplicate finder — candidates only, and the source-embedding fence
This pays off the forward-references in [`graph-health-scan`](vault-template/.claude/tools/graph-health-scan)
("semantic duplicates wait for S17") and [NODE-GRAPH §6](NODE-GRAPH.md) ("duplicate
**candidates**"). It finds near-duplicate pages the deterministic exact-title scan cannot,
and outputs **merge candidates** for {{OWNER}} / the Thinking layer — it **never
auto-merges** (the [SELF-DEVELOPMENT §6](SELF-DEVELOPMENT.md) autonomy gate). It is kept
**separate** from `graph-health-scan` so that tool stays deterministic and network-free;
vector-store health is its own lane.

**The source-embedding fence:** if source notes are embedded to detect near-duplicate
*incoming material* at integration time, those vectors are **fenced to the dedup path
only** and are explicitly **not** a read-routing or answer surface — otherwise the §1/§2
boundary re-enters through the dedup door.

### 3.6 Thresholds and the model pull — deferred and pinned
- **Thresholds are instance config (S19).** What cosine distance counts as *relevant* or
  *duplicate* can only be calibrated against real content; a cold-hardcoded cut is the
  silent-cap the loading rules warn against ([OPERATIONS-KERNEL §9](OPERATIONS-KERNEL.md)).
  The engine ships a **named, surfaced knob with a documented placeholder default**, and
  an explicit S19 calibration step gates "trust the output".
- **Supply chain (Security-First).** The local model is *fetched untrusted input*
  ([PRINCIPLES.md](PRINCIPLES.md) §3). The substrate **pins a model id and verifies a
  recorded checksum on pull, failing closed on mismatch**, from a named registry.

## 4. The substrate code category

Half A's resolver is a plain Builder `tool`. **Half B is not** — embedding needs network
(model pull or API) and optional credentials, which the `tool` kind forbids
([BUILDER §3](BUILDER.md): deterministic, no network, no credentials). So S17 introduces
the **substrate** code category: engine-internal foundational code beneath the kernel —
like the kernel runtime itself, **not** a Builder-built instrument. It lives in
`vault-template/.claude/substrate/`, is Python with its own `requirements.txt`, and may
use the network and (optionally) credentials via `.env`.

This required one **shared-meaning amendment** to
[`instruments.md` §1](vault-template/.claude/instruments.md), whose "nothing
instrument-shaped lives elsewhere" rule governs *instruments* (skill / agent / command /
tool). §1 now distinguishes **instruments** (Builder-built, registered) from **engine
substrate** (foundational code, not an instrument, not registry-listed). A thin
[`/reindex`](vault-template/.claude/commands/reindex.md) command *fronts* the substrate
and is registered as an instrument; the substrate code is not.

## 5. Security & the data boundary

- **Local default → no credentials, canon content never leaves the device.** The API
  adapter sends canon text to a third party — the same trust class as the brain's
  existing Claude calls, but a wider surface; it is a conscious opt-in, key strictly via
  `.env` ([the credential map](.claude/CLAUDE.md)), never hardcoded.
- **The substrate reads canon and writes only its own store.** Untrusted source text and
  the downloaded model are *data*, not instructions.
- **The engine ships no index, embeddings, or model.** Embeddings are *derived live
  content* — a lossy but real, possibly-invertible projection of canon — so a committed
  store would leak instance knowledge. The engine ships code, config/schema, contracts,
  and a synthetic fixture corpus only (`tests/fixtures/model-retrieval/`); the store
  itself is never shipped — it materialises at runtime under `.claude/substrate/store/`,
  and the store path, vector files, and the model cache are gitignored.

## 6. Built now vs deferred

- **Now (cold-testable, the deterministic shell):** the resolver tool + bindings template
  + Builder-stamp consumption; the embedding interface + local/API adapters (behind the
  interface, with a stub embedder for tests); the per-page-shard store + atomic rebuild +
  content-hash staleness guard; the re-rank-only candidate contract; the semantic-dup
  finder (candidates-only); the pinned-model + checksum; the `/reindex` command; the
  contract fixture + synthetic corpus.
- **Deferred to S19 (needs the live content distribution):** threshold calibration; real
  model selection + the model pull; ranking-quality and dedup-precision evaluation;
  **turning re-ranking on in read-routing**; the live index; populated instance bindings;
  live multi-provider chat routing if a need appears.
- **Deferred and named (not built):** any metered routing-telemetry signal and the
  self-tuning loop over it (needs a tier-3 Node-Graph ontology addition first). **S18:**
  MCP hosting.

## 7. Acceptance & seams

The acceptance bar is [`tests/model-retrieval-contract.md`](vault-template/.claude/tests/model-retrieval-contract.md),
which splits **deterministic** parts (resolver, hash-keying, staleness guard, atomic
write, candidate-emission shape — fixture-tested with a stubbed embedder) from the
**non-deterministic** embedder (property/tolerance-tested; no golden vectors). Consumers
and seams: the kernel ([§7.5](OPERATIONS-KERNEL.md) tie-break, [§11](OPERATIONS-KERNEL.md)
`model-route`), the Node-Graph ([§4/§5/§9](NODE-GRAPH.md) semantic/vector edges), the
Builder ([§4](BUILDER.md) resolver consumption), and Self-Development
([SELF-DEVELOPMENT §6](SELF-DEVELOPMENT.md) the autonomy gate over merge/edge candidates
and the deferred routing signal).
