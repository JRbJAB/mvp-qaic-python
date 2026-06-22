# P108-R1 — Canonical Index Dedup Repair

## Status
CREATED_LOCAL_PENDING_GATE

## Repair
- Fix Windows case-insensitive duplicate detection for Index.html and index.html.
- Keep canonical Index.html read-only / no overwrite.
- Keep P108 as UI polish decision gate only.

## Safety
- NO_INDEX_HTML_EDIT
- NO_PUBLIC_DEPLOY
- NO_CLASP
- NO_APPS_SCRIPT_EXECUTION
- NO_SHEET_WRITE
- NO_BROKER_ORDER_SIZING

## Next
P109_CANONICAL_INDEX_READONLY_AUDIT_OR_UI_POLISH_PATCH_PLAN
