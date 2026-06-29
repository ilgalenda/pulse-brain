<!--
TEMPLATE — the canon (wiki) edge-map. The kernel maintains this table; every
write updates it in the same step (see OPERATIONS-KERNEL.md §8). It is the
always-read map of the wiki. The `links` column carries each page's outbound
[[wikilinks]]/related so the graph can be traversed from here without opening files.
One row per wiki page, grouped by domain. The editorial standard for the pages this
maps — kinds, atomicity, lifecycle — is CONTEXT-ENGINE.md (Canon); the node/edge
model the `links` column serialises is NODE-GRAPH.md.
-->

# Canon index (wiki edge-map)

| title | description | path | domain | tags | links |
|-------|-------------|------|--------|------|-------|
