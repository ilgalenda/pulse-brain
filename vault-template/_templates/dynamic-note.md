---
title:                          # REQUIRED — what this source is
description:                    # REQUIRED — one sentence on what it contains
domain:                         # gtm | ai-orchestration | product | people | operating | glossary
type: source
source_type:                    # url | file | page | feed | note
source:                         # provenance — the URL, file path, or origin
contributed_by:                 # which agent gathered it (author)
confidence:                     # high | medium | low — open-world reliability (dynamic-only)
tags: []
feeds: []                       # [[wiki pages]] this source was compiled into
related: []                     # [[wikilinks]] to related notes
id:                             # stable kebab-case slug
created:                        # YYYY-MM-DD
---

<!--
TEMPLATE — do not treat as a live note.
DYNAMIC = an AGENT-gathered source (raw input, kept for provenance — not the
answer surface; the wiki is). The kernel ingests it and compiles it INTO the
wiki (canon); `feeds` links the pages it informed. See OPERATIONS-KERNEL.md §2–3
for mechanics; CONTEXT-ENGINE.md (Dynamic) is the authority for the capture
contract, the `confidence` trust model, and the source lifecycle.
-->

## Summary
<!-- One short paragraph — what this source says, in brief. -->

## Extracted points
<!-- The key points the kernel pulled out and integrated into the wiki. -->

## Provenance
<!-- Where it came from, when, how retrieved — enough to re-find or cite it. -->
