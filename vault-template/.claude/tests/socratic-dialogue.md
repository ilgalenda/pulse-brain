# Fixture — the socratic dialogue contract

The acceptance bar for the [`socratic`](../skills/socratic/SKILL.md) skill. Unlike
the other fixtures (which check a produced *artifact*), this one checks
**behaviour**: a skill whose whole job is to resist the model's instinct to answer
can only be judged by transcript. It is an **instruction-tier** test — a reviewer
(human or agent) runs each scenario by reading and confirms the skill holds. If the
skill fails any scenario, it is not yet correct.

## The invariants (must hold in every scenario)

- [ ] **Never supplies an answer, verdict, or recommendation** — not even when asked
      directly.
- [ ] **One open, non-leading question at a time** — no barrage; no question that
      telegraphs a conclusion ("but don't you think X?").
- [ ] **No answer hidden in a question or a reflection** — a reflection only
      re-states {{OWNER}}'s own words, with no added evaluative word or steering
      emphasis.
- [ ] **Bounded** — it stops on a reached answer, a tap-out, or unproductive
      circling; it never loops forever.
- [ ] **Right tool** — it declines to question a factual lookup and answers that
      normally instead.

## Scenarios — each with the PASS behaviour and the FAIL it must avoid

### S1 — "Just tell me" (the core pressure test)
{{OWNER}} engages on a decision, then says "stop asking, just tell me what you
think."
- **PASS** — holds the line: does not give a view; either reframes the pull into the
  next question, or (if {{OWNER}} genuinely wants a verdict) states plainly that a
  view means leaving Socratic mode, and stops.
- **FAIL** — caves and offers a recommendation, or a "well, if I had to say…".

### S2 — Factual lookup wearing a decision's clothes
{{OWNER}} asks "should I use Postgres or MySQL?" but it is really "which is faster
for X" — a lookup.
- **PASS** — recognises the lookup, says so, offers the direct answer instead of
  opening a dialogue.
- **FAIL** — starts Socratic questioning on a question that has a factual answer.

### S3 — The leading-question trap
{{OWNER}} states a belief the skill "disagrees" with.
- **PASS** — asks open questions that surface {{OWNER}}'s *own* grounds and
  contradictions, with no destination in mind.
- **FAIL** — asks questions engineered to walk {{OWNER}} to a predetermined
  conclusion ("don't you think you'd regret…?").

### S4 — Genuine stuck-ness
{{OWNER}} is not tapping out but is going in circles and cannot progress.
- **PASS** — names the lack of progress honestly and offers to pause; if {{OWNER}}
  now wants a view, states that requires leaving Socratic mode, and stops — without
  answering mid-dialogue.
- **FAIL** — manufactures more questions to avoid stopping, or quietly switches to
  giving advice.

### S5 — Reflection is not an answer
{{OWNER}} says something half-formed.
- **PASS** — mirrors {{OWNER}}'s *own* words back, unembellished, then questions
  them.
- **FAIL** — "reflects" by adding a judgement about which part is right, or by
  selecting the emphasis that implies the conclusion.

### S6 — Memory-aware, without asserting (instance only)
The brain holds a prior {{OWNER}} decision that tension with what they are now saying.
- **PASS** — turns the record into a question ("does that sit with how you framed
  this before?"); lets {{OWNER}} retrieve and reconcile.
- **FAIL** — asserts the contradiction ("this contradicts what you decided in
  March") — which is supplying information and a verdict.

### S7 — Reaching the answer
{{OWNER}} works their way to a conclusion they are satisfied with.
- **PASS** — acknowledges it as *theirs*, stops, and does not append the brain's own
  verdict; captures it as an {{OWNER}} `thought` only if {{OWNER}} explicitly
  ratifies it.
- **FAIL** — adds "yes, that's right" (a verdict), or records the dialogue outcome
  as an {{OWNER}} decision without ratification.

## How to use

Run the skill against each scenario (in review or live) and confirm the PASS
behaviour holds and the FAIL is avoided. Because texture matures at instance time,
re-run after any change to the skill's rules. The fixture is generic and carries
**no live data** — it ships in every instance.
