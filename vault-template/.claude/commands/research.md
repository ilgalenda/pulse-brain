---
description: Run a research pass now — answer a question or confirm an open inference, filing a dynamic-note for the kernel to integrate.
argument-hint: [question or claim to research — omit to pull the next open inference]
---

Run one research pass.

- If `$ARGUMENTS` is given, research that question/claim.
- If `$ARGUMENTS` is empty, pull the **next open `[!inference]`** from the
  `edge/inference` queue and confirm it (the primary intake, RESEARCH-AGENTS.md §4).

Route to the **`research-agent`** (or the `research` skill directly for a quick
single pass). Do not implement the cycle here — the agent/skill owns it. For
several independent prompts, spawn `research-agent`s in parallel.

Report back: what was found, the confidence, the note(s) filed and what they fed;
if an inference was confirmed, name it and note the `log.md` stamp.
