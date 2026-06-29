# Reflex Preview Gate â€” Mandatory Instructions

Locked: 2026-06-29T12:43:47

## Non-negotiable rule

**Visual tests are mandatory before Reflex deployment.**

No Reflex deployment is allowed unless all preview gates below are passed and evidenced.

## Required gate sequence

1. Static import and route contract gate.
2. Static visual/render gate.
3. CDC Dev Tracker preview aligned with Migration Tracker visual oracle.
4. Local browser/runtime visual smoke gate.
5. Operator review with visible evidence.
6. Deployment approval only after visual evidence is stored.

## Blockers

- Generic HTML preview is blocked.
- Fake screenshots are blocked.
- Route 200 alone is blocked.
- Import-only proof is blocked.
- Backend-only proof is blocked.
- Frontend/Bun unresolved state blocks public deployment.

## Required evidence before deploy

- Preview artifact path.
- Screenshot or operator visible validation.
- Test command output.
- Git commit and tag containing the gate docs/tests.
- Explicit statement that the preview follows Migration Tracker visual semantics.
