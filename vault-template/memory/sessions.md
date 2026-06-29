<!--
TEMPLATE: the session-presence note. APPEND-ONLY, collision-safe across concurrent
tabs (DEVELOPMENT.md §5). Each open CLI tab APPENDS a beat: when it starts, and
whenever it writes (its heartbeat). A beat is never edited in place; the current view
is produced by `session-reconcile`, which compacts this file, keeping the latest
beat per session, dropping cleanly-closed tabs, and reaping stale (crashed) ones.

Live beats are INSTANCE RUNTIME STATE, created on the machine and never committed.

Beat format (append one per heartbeat):

## <session-id>, <YYYY-MM-DD HH:MM>
- scope: the domain / pillar / page this tab is working (e.g. canon/entities, or a slice)
- state: active | closing
- last_active: <YYYY-MM-DD HH:MM>

A tab appends `state: closing` as its final beat on a clean exit, so the reconciler
drops it immediately. A crashed tab leaves no closing beat; the reconciler reaps it
once its last_active passes the staleness window.
-->

# Session presence
