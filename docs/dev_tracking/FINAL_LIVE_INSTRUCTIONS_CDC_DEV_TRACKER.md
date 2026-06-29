# Final Live Instructions â€” CDC Dev Tracker

Updated: 2026-06-29T12:43:47

## Scope

Applies to CDC Dev Tracker, Dev Tracking routes, Preview gates, and Reflex deployment readiness.

## Locked instructions

- Migration Tracker is the visual oracle.
- CDC Dev Tracker preview must be visually coherent with Migration Tracker.
- Visual tests are mandatory before Reflex deployment.
- Docs must be updated in the same commit as any CDC/dev tracker gate change.
- Lifecycle tracker status changes require matching evidence docs.
- No public deploy without browser/runtime visual evidence.
- No generic HTML preview may be used as release evidence.

## Current state

- Static CDC Dev Tracker layer: sealed.
- PRIVATE_RC static visual gate: sealed.
- Real Reflex browser preview: still required before deployment.
- Bun/frontend runtime issue: known blocker, not a CDC architecture blocker.
