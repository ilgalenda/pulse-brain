---
description: Run a monitoring beat now. Check the watchlist for new material and file dynamic-notes for what's changed.
---

Run one monitoring beat over the instance watchlist.

Route to the **`monitor-agent`** (or the `monitor` skill directly). Do not
implement the beat here; the agent or skill owns it. With an empty watchlist this is
correctly a no-op.

Report back: sources checked, what was new, what was filed or fed, or "no changes".
