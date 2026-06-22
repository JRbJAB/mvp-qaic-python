# P110A-R2 — Locator Exports BOM Repair

## Status
CREATED_LOCAL_PENDING_GATE

## Repair
- R1 script here-string corruption bypassed by full controlled source rewrite.
- Root JSON loading is UTF-8 BOM safe.
- Audit JSON, candidates CSV and review MD are regenerated.

## Safety
- NO_INDEX_HTML_EDIT
- NO_INDEX_HTML_GENERATION
- NO_PUBLIC_DEPLOY
- NO_CLASP
- NO_APPS_SCRIPT_EXECUTION
- NO_SHEET_WRITE
- NO_BROKER_ORDER_SIZING

## Next
P110B_HUMAN_CONFIRM_CANONICAL_INDEX_OR_PATCH_PLAN
