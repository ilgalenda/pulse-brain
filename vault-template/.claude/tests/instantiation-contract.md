# Fixture: the instantiation-kit contract

The acceptance checklist the **instantiation kit** must pass before it is trusted (the kit
described in [`SETUP.md`](../../../SETUP.md), [`ARCHITECTURE.md` §1](../../../ARCHITECTURE.md)).
It has two halves. **Part A** covers the [`instantiate`](../tools/instantiate) tool's
deterministic guarantees; **Part B** covers the [`setup`](../skills/setup/SKILL.md) skill's
judgement responsibilities. The governing rule throughout: **the instance is created OUTSIDE
the engine and never committed to it**, and the **flat-instance topology** holds (the
instance root is both the directory Claude Code launches from and the Obsidian vault, so the
director and the commands load together and the knowledge sits where the working directory
expects it). This restates the authority as a *test*, not a new authority. If any item fails,
the kit is not correct.

## Part A: the `instantiate` tool

- [ ] **Flat topology.** The instance is `<target>/` with `README` + `LICENSE` +
      `.env.example` + a generated `.gitignore` at the root; the authority docs in
      `<target>/docs/`; the dual-role director and the whole operating layer in
      `<target>/.claude/` (`CLAUDE.md`, `commands/`, `skills/`, `agents/`, `tools/`,
      `substrate/`, `tests/`, …); and the live knowledge (`canon/inbox/dynamic/memory/
      presets/_templates` + `index.md`/`log.md`) at the root. Launching from `<target>`
      resolves the commands (root `.claude/commands/`) and the director (root
      `.claude/CLAUDE.md`).
- [ ] **Authority-doc links repointed.** Because the engine nests its instruments one level
      deeper (`vault-template/.claude/`) than the instance's root `.claude/`, every
      authority-doc link inside an instrument **and the director** is rewritten to
      `<correct-depth>/docs/NAME.md` for that file's location. A sampled link (a command's
      `../../docs/OPERATIONS-KERNEL.md`, a skill's `../../../docs/THINKING.md`, the director's
      `../docs/PRINCIPLES.md`) **resolves to a real file**. Knowledge links, cross-instrument
      links, and bare prose mentions are **untouched**.
- [ ] **Operational stamping, docs left alone.** `{{OWNER}}`/`{{COMPANY}}` are stamped in the
      **operational surfaces only** (`.claude/**` + the knowledge folders + `README`); the
      authority docs in `docs/` are copied **UNSTAMPED** (a generic instruction: stamping
      would mangle the passages that document the placeholder convention). After a run, **no
      `{{OWNER}}`/`{{COMPANY}}` remains in the operational tree**; the tool **fails closed**
      (exit 2 + an `INSTANTIATION-FAILED` marker) if any survives.
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
      it keeps the knowledge folders (the owner's brain, versionable privately) but excludes
      secrets + derived state (`.env`, `.obsidian/`, `**/substrate/store/`, `*.shard`,
      `*.tmp`, model cache).
- [ ] **Data-boundary guard (the load-bearing one).** A target that is **inside**, **equal
      to**, or an **ancestor of** the engine (the engine root, `vault-template`, any subpath,
      or a parent directory) gives **exit 2, nothing written** — case-insensitively, so the
      guard holds on the macOS default filesystem. A **non-empty** target gives exit 1
      (re-instantiation is a deliberate delete-and-recreate, never a silent overwrite). A
      `--preset` naming a preset that doesn't exist, or an empty `--owner`/`--company`, gives
      exit 1 **before any copy** (no half-built instance left behind). The engine is only ever
      READ.
- [ ] **Fails closed on a malformed engine.** A missing required template (`ARCHITECTURE.md`,
      `.claude/CLAUDE.md`, `vault-template/{memory/core.md,index.md,log.md}`) gives exit 2
      **before any copy**, never a crash mid-run that strands a stamped-but-unseeded partial
      instance.
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
- [ ] **Hands off.** Launch from the instance root, open that same folder in Obsidian,
      `/pulse`, then `/reindex`; threshold calibration + turning re-ranking on once real
      content exists.

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
> in `docs/` (unstamped, still `{{OWNER}}`), `.claude/CLAUDE.md` stamped to "Test Owner" with
> its doc links repointed to `../docs/…`, the operating layer in `.claude/`, and
> `canon/inbox/dynamic` at the root each holding `work/people/reference` (+ `entities` under
> canon), example domains gone. `core.md` reads `active_preset: gtm-lead`; `index.md`'s
> Domains list is the three chosen; `log.md` has the instantiated entry. A grep of the
> operational tree for `{{OWNER}}`/`{{COMPANY}}` returns nothing; a command's `../../docs/`
> doc link resolves; the instance `.gitignore` does not ignore the knowledge folders.

*Why this is correct:* the links resolve (repointed to `docs/`), only operational surfaces
are stamped (docs stay correct), domains are the owner's, the instance launches from its own
root, and it sits outside the engine. A clean, runnable brain with the data boundary intact.

## FAIL examples the kit must NOT produce

- **Scaffolding inside the engine.** Any write into the engine repo (its `vault-template/`
  or root), or a target equal to / an ancestor of the engine; the tool must exit 2 and write
  nothing.
- **A surviving placeholder treated as success.** An operational file still containing
  `{{OWNER}}`/`{{COMPANY}}` after a run reported clean.
- **Stamping the authority docs.** Rewriting `{{OWNER}}` in ARCHITECTURE and the like, so the
  placeholder-convention passages read nonsensically ("… stands in for Ann …").
- **A doc link that resolves to nothing.** An instrument or the director whose authority-doc
  link was not repointed to the instance's `docs/` at the right depth (overshooting the root,
  or still pointing at a now-nonexistent root `.md`).
- **The engine's `.gitignore` copied verbatim.** Ignoring the instance's own knowledge
  folders, hiding the owner's brain from their own git.
- **A secret or stale store copied in.** An `.env`, a `*.shard`/`*.vec`, `substrate/store/`,
  or `.obsidian/` riding from the engine into the instance.
- **The tool reaching the network or a credential.** The deterministic scaffold must do
  neither; that is the `/setup` skill's wiring, never the tool's.
- **Hardcoded domains.** Scaffolding the shipped six regardless of `--domains`, or treating
  them as the only option (they are owner-defined examples).
- **Clobbering.** Overwriting a non-empty target instead of refusing (exit 1).
