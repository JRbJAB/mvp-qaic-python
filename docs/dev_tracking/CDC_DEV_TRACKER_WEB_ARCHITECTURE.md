# CDC Dev Tracker â€” Web Architecture

Updated: 2026-06-29T12:43:47

## Routes

- /dev-tracking
- /cdc-dev-tracker
- /cdc-tracker

## Source data

- CDC delivery tracker source: V25_CDC_DELIVERY_TRACKER contract.
- Lifecycle state source: docs/dev_tracking/DEV_LIFECYCLE_TRACKER.json.
- Tool registry CDC source: data/tool_registry/* and docs/TOOL_REGISTRY_*.md.

## Visual oracle

Migration Tracker is the visual oracle.

CDC Dev Tracker preview must be visually coherent with Migration Tracker.

Required visual semantics:

- Migration-style cards and sections.
- Progress and percentage indicators.
- Blue/accent progress language.
- Status badges.
- Priority/readiness grouping.
- Operator-readable lifecycle state.
- No placeholder/stub language.

## Preview policy

**Visual tests are mandatory before Reflex deployment.**

A valid preview must either reuse the Migration Tracker components directly or prove parity with their visual structure.

Generic HTML preview is not accepted as release evidence.

## Runtime status

- Backend Reflex diagnostic: OK in R6Q.
- Frontend Reflex runtime: blocked by Bun install crash in .web.
- Public deployment: blocked until real browser/runtime visual smoke passes.
