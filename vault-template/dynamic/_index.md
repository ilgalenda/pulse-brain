<!--
TEMPLATE: the dynamic (agents' sources) edge-map. The kernel maintains this;
every write updates it in the same step (see OPERATIONS-KERNEL.md §8). Consulted
by relevance, not always loaded. The `links` column carries each source note's
[[links]] to the wiki pages it feeds. One row per source note, grouped by domain.
Confidence (CONTEXT-ENGINE.md, Dynamic §2) is not a column. The columns stay
uniform across pillars; surface medium/low trust via a `confidence/medium` or
`confidence/low` tag in the `tags` column so it is consultable from the map
without opening the note. High confidence is the unmarked default.
The node/edge model the `links` column serialises is NODE-GRAPH.md.
-->

# Dynamic index (agent sources edge-map)

| title | description | path | domain | tags | links |
|-------|-------------|------|--------|------|-------|
