---
description: Enter Socratic mode — the brain questions you toward your own answer and never supplies one. For thinking a decision or belief through, not factual lookup.
argument-hint: [the decision, belief, or question you want to be questioned on]
---

Enter **Socratic mode** for `$ARGUMENTS`.

Route to the [`socratic`](../skills/socratic/SKILL.md) skill and run it — do not
implement the method here.

- If `$ARGUMENTS` names a topic, open on it: get {{OWNER}} to state the claim, then
  question.
- If `$ARGUMENTS` is empty, ask {{OWNER}} what they want to be questioned on.

Hold the skill's hard rules: **never** supply an answer, verdict, or recommendation
(no escape hatch — for a view, {{OWNER}} leaves Socratic mode for challenge-&-advise,
Thinking §3.5); one open, non-leading question at a time; stop the moment {{OWNER}}
reaches their own answer or asks to stop. If `$ARGUMENTS` is really a factual lookup,
say so and offer the direct answer instead.
