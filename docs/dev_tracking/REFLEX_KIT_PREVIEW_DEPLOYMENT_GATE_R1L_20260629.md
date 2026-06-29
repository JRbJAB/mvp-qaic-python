# Reflex Kit Preview Deployment Gate â€” R1L

Status: Reflex public deployment is blocked until real browser runtime visual match.

R1J proved the approved static preview locally. R1K deploys the internal UI Tracker Tool gate. R1L defines the public deployment rule.

## Public Reflex deploy rule

`REFLEX_PUBLIC_DEPLOY_ALLOWED=False` until all of the following are true in the same run report:

- real Reflex browser runtime starts without Bun crash;
- `/dev-tracking`, `/cdc-dev-tracker`, and `/cdc-tracker` are reachable;
- the rendered browser page matches `APPROVED_TRACKER_PREVIEW.html` by required tokens and visual semantics;
- screenshot or browser evidence is captured;
- tests and Ruff pass after the runtime proof.

## Current status

`REFLEX_PUBLIC_DEPLOY_STATUS=BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH`.

This is intentional: the UI Tracker Tool can be deployed internally, while public Reflex deployment remains gated.
