# Fixture — the `dynamic-note` contract

The acceptance checklist a gather instrument's output must pass. It encodes the
capture contract (CONTEXT-ENGINE Dynamic §1) and the frontmatter contract
(TAXONOMY) — restated here as a *test*, not a new authority. If a produced note
fails any item, the instrument is not yet correct.

## Frontmatter — every field present and valid

- [ ] `title` — present, one line, names what the source *is*.
- [ ] `description` — present, one sentence on what it contains.
- [ ] `domain` — one of `gtm | ai-orchestration | product | people | operating | glossary`.
- [ ] `type: source` — literal.
- [ ] `source_type` — one of `url | file | page | feed | note`.
- [ ] `source` — the provenance handle (URL, path, or origin); enough to re-find.
- [ ] `contributed_by` — the **agent** that gathered it (author), not {{OWNER}}.
- [ ] `confidence` — one of `high | medium | low` (see [`confidence-rubric.md`](confidence-rubric.md)).
- [ ] `tags` — list (may be empty).
- [ ] `feeds` — list; empty until integrated, then the `[[wiki pages]]` it informed.
- [ ] `related` — list (may be empty).
- [ ] `id` — stable kebab-case slug.
- [ ] `created` — `YYYY-MM-DD`.

## Body — the three required sections

- [ ] `## Summary` — one paragraph: what the source says.
- [ ] `## Extracted points` — the specific, integrable claims (the payload). A
      source that yields **no** extractable point is not worth capturing — reject it.
- [ ] `## Provenance` — where it came from, when, how retrieved; enough to re-find or cite.

## Discipline checks

- [ ] **Atomic** — one source, one note. A find spanning two distinct subjects is two notes.
- [ ] **Not the answer surface** — the note is raw provenance; the *wiki* is the answer. It does not pretend to be canon.
- [ ] **Immutable** — the note is newly created, not an in-place edit of an existing one. (Refresh/supersede is a *new* note; see Dynamic §3.)
- [ ] **Supersession is represented correctly** — when a new note replaces a stale one, the link is recorded per [NODE-GRAPH §3.2](../../../NODE-GRAPH.md): a `related` link to the replacement + a one-line body note, surfaced as an `edge/supersedes` tag. **No dedicated `supersedes` frontmatter field** — S9 deliberately gives it no new schema field. The superseded note is kept for provenance, not deleted.
- [ ] **Deduped** — a search for the same `source` found no existing note; if one existed, the instrument refreshed/superseded rather than duplicated.
- [ ] **No live secrets** — no credentials or tokens embedded; auth (if any) referenced via `.env`.

## Worked PASS example (shape only — illustrative, not live data)

```
---
title: Example vendor timing-product brief
description: A vendor page describing a timing product's stated accuracy claims.
domain: product
type: source
source_type: url
source: https://example.com/vendor/timing-brief
contributed_by: research-agent
confidence: medium
tags: [timing, competitor]
feeds: []
related: []
id: example-vendor-timing-brief
created: 2026-01-01
---

## Summary
A vendor brief stating accuracy figures for a timing product, with no
independent corroboration on the page.

## Extracted points
- The vendor claims sub-microsecond accuracy under stated conditions.
- The claim is the vendor's own; no third-party measurement is cited.

## Provenance
Retrieved from the vendor's public product page on 2026-01-01; URL above.
```

*Why `confidence: medium`:* single-source, vendor-authored (interested party),
no corroboration — rated down per the rubric.

## FAIL examples the instrument must NOT produce

- Missing `## Extracted points`, or points so vague nothing is integrable.
- `confidence` absent, or free-text ("fairly sure") instead of `high|medium|low`.
- `contributed_by: {{OWNER}}` on a dynamic note (that is an **inbox** note).
- Two unrelated subjects in one note (not atomic).
- Body that asserts the claim as established fact rather than *reported*.
