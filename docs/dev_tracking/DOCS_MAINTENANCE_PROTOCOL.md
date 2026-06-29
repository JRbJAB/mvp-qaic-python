# Documentation Maintenance Protocol

Locked: 2026-06-29T12:43:47

## Non-negotiable process

Every future feature, UI, tracker, preview, or deployment-related change must update the relevant docs in the same commit.

The operator must not need to remind the project to update documentation.

## Required doc updates per change

- Architecture doc when routes, pages, data contracts, or visual behavior change.
- Gate/instructions doc when deployment, runtime, or preview rules change.
- Evidence doc when a phase is marked DONE.
- Lifecycle tracker JSON when phase state changes.
- Cleanup agenda when stale docs or placeholders are discovered.

## Hard rules

- Do not mark DONE if docs are queued but not updated.
- Do not mark preview-ready without visual evidence.
- Do not mark deploy-ready without runtime/browser proof.
- Do not create generic previews when a visual oracle exists.
- Do not write project source outside the active repo.
- Runtime reports belong under C:\JRb_TRADING_OS\_RUN_REPORTS\....
