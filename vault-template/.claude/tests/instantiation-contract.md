# Fixture: the instantiation-kit contract

The acceptance checklist the **instantiation kit** must pass before it is trusted (the kit
described in [`SETUP.md`](../../../SETUP.md), [`ARCHITECTURE.md` §1](../../../ARCHITECTURE.md)).
It has two halves. **Part A** covers the [`instantiate`](../tools/instantiate) tool's
deterministic guarantees; **Part B** covers the [`setup`](../skills/setup/SKILL.md) skill's
judgement responsibilities. The governing rule throughout: **the instance is created OUTSIDE
the engine and never committed to it**, and the **Model A topology** holds (the instance
preserves the engine's nesting so every instrument-to-authority-doc link resolves untouched).
This restates the authority as a *test*, not a new authority. If any item fails, the kit is
not correct.

## Part A: the `instantiate` tool

- [ ] **Model-A topology.** The instance is `<target>/` with the authority docs +
      `.gitignore` + `.env.example` + `.claude/CLAUDE.md` at the root, and the live vault at
      `<target>/vault/` (the stamped `vault-template/` contents). A sampled
      instrument-to-doc link (for example a skill's `../../../../OPERATIONS-KERNEL.md`)
      **resolves to a real file** in the instance, proving the nesting was preserved.
- [ ] **Operational stamping, docs left alone.** `{{OWNER}}`/`{{COMPANY}}` are stamped in
      the **operational surfaces only** (`vault/**` + the instance `.claude/CLAUDE.md`); the
      authority docs at the instance root are copied **UNSTAMPED** (a generic instruction:
      stamping would mangle the passages that document the placeholder convention). After a
      run, **no `{{OWNER}}`/`{{COMPANY}}` remains in the operational tree**; the tool
      **fails closed** (exit 2 + an `INSTANTIATION-FAILED` marker) if any survives.
- [ ] **Owner-defined domains.** Each pillar's domain subdirs match `--domains` exactly
      (with a `.gitkeep`); shipped example domains not chosen are removed; `entities` is
      added to `canon/` only and is never a chosen domain.
- [ ] **Seeded empty state.** `core.md` carries the chosen `active_preset` + `updated`;
      `index.md`'s `## Domains` is regenerated from `--domains`; `log.md` has the first
      "Brain instantiated" entry; `sessions.md` is empty; pillar `_index.md` tables are
      empty.
- [ ] **Excludes honoured.** `.git/`, `.obsidian/`, `substrate/store/`, `*.shard`/`*.vec`/
      model artefacts, `.env` (not `.env.example`), `__pycache__/` are **not** copied, so no
      stale runtime state or secret rides into the instance.
- [ ] **Instance `.gitignore` is instance-appropriate.** It is generated, NOT the engine's:
      it keeps `vault/` (the owner's brain, versionable privately) but excludes secrets +
      derived state (`.env`, `.obsidian/`, `**/substrate/store/`, `*.shard`, model cache).
- [ ] **Data-boundary guard (the load-bearing one).** A target **inside the engine** (the
      engine root, `vault-template`, or any subpath) gives **exit 2, nothing written**. A
      **non-empty** target gives exit 1 (re-instantiation is a deliberate delete-and-recreate,
      never a silent overwrite). A `--preset` naming a preset that doesn't exist gives exit 1
      **before any copy** (no half-built instance left behind). The engine is only ever READ.
- [ ] **Deterministic and least-privilege.** The same `(engine content, args, --now)` gives
      the same instance; `--now` makes seeded timestamps reproducible; `--dry-run` prints the
      plan and writes nothing; **no network, no credentials**. Exit 0 success, 1 recoverable
      refusal, 2 hard failure; errors go to stderr.

## Part B: the `setup` skill

- [ ] **Interviews, never assumes.** Collects owner/company, the owner's **own domains**
      (shipped six offered as editable examples), presets to keep/author, an optional
      writing sample, the embedding choice, and a target path outside the engine.
- [ ] **Authors presets before scaffolding.** Any preset the owner wants that isn't shipped
      is written from `_templates/preset.md` first, so the tool's `--preset` check passes.
- [ ] **Calls the tool, never reimplements it.** The deterministic copy/stamp/seed is the
      tool's; the skill passes the collected answers and reads the report; it does not
      proceed on a non-zero exit.
- [ ] **Owns the machine-specific wiring only.** The embedding adapter (local pull+pin / API
      key via `.env`), schedules + `SessionEnd` hook, watchlist, `.env` from `.env.example`,
      and model-bindings: the parts a tool may not do (network/credentials/cron).
- [ ] **Boundary discipline.** Never scaffolds into the engine; fills owner content (voice
      sample, `.env`, bindings) in the **instance**, not the engine; surfaces a **Pulse
      decision** recording what was instantiated.
- [ ] **Hands off.** Launch from the instance root, open `vault/` in Obsidian, `/pulse`,
      then `/reindex`; threshold calibration + turning re-ranking on once real content exists.

## Worked PASS example (a cold run)

> From the engine root, instantiate a stranger's brain into a temp dir with neutral domains:
>
> ```
> python3 vault-template/.claude/tools/instantiate \
>   --target /tmp/Pulse-test-Brain --owner "Test Owner" --company "TestCo" \
>   --domains work,people,reference --preset gtm-lead --now "2026-06-29 12:00"
> ```
>
> Result: exit 0, "instance created and verified clean". The instance has the authority docs
> at its root (unstamped, still `{{OWNER}}`), `.claude/CLAUDE.md` stamped to "Test Owner",
> and `vault/` with `canon/inbox/dynamic` each holding `work/people/reference` (+ `entities`
> under canon), example domains gone. `core.md` reads `active_preset: gtm-lead`; `index.md`'s
> Domains list is the three chosen; `log.md` has the instantiated entry. A grep of the
> operational tree for `{{OWNER}}`/`{{COMPANY}}` returns nothing; a skill's `../../../../`
> doc link resolves; the instance `.gitignore` does not ignore `vault/`.

*Why this is correct:* the structure is preserved (links resolve), only operational
surfaces are stamped (docs stay correct), domains are the owner's, and the instance sits
outside the engine. A clean, runnable brain with the data boundary intact.

## FAIL examples the kit must NOT produce

- **Scaffolding inside the engine.** Any write into the engine repo (its `vault-template/`
  or root); the tool must exit 2 and write nothing.
- **A surviving placeholder treated as success.** An operational file still containing
  `{{OWNER}}`/`{{COMPANY}}` after a run reported clean.
- **Stamping the authority docs.** Rewriting `{{OWNER}}` in ARCHITECTURE and the like, so the
  placeholder-convention passages read nonsensically ("… stands in for Ann …").
- **Broken instrument links.** A flattened instance where `../../../../X.md` overshoots
  the root and resolves to nothing.
- **The engine's `.gitignore` copied verbatim.** Ignoring the instance's own `vault/`
  (because the engine ignores `/vault/`), hiding the owner's brain from their own git.
- **A secret or stale store copied in.** An `.env`, a `*.shard`/`*.vec`, `substrate/store/`,
  or `.obsidian/` riding from the engine into the instance.
- **The tool reaching the network or a credential.** The deterministic scaffold must do
  neither; that is the `/setup` skill's wiring, never the tool's.
- **Hardcoded domains.** Scaffolding the shipped six regardless of `--domains`, or treating
  them as the only option (they are owner-defined examples).
- **Clobbering.** Overwriting a non-empty target instead of refusing (exit 1).
