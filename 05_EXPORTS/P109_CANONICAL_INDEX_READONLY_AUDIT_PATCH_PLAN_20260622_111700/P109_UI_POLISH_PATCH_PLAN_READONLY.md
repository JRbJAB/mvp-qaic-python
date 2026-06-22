# P109 — Canonical Index Readonly Audit + UI Polish Patch Plan

## Decision status

`REVIEW_REQUIRED`

## Candidates

- `05_EXPORTS/P106_WEBAPP_STATIC_PREVIEW_DATA_EXPORT_20260622_103845/STATIC_PREVIEW/index.html` | role=`generated_export_not_canonical` | score=`0` | edit=`False`

## Requirements

- **P0 — confirm_canonical_index**: Human confirms which Index.html is the validated WebApp shell.
- **P0 — bind_json_data_packs**: Plan binding of webapp_pack/context_pack/prompt_payload/admin_status to the canonical UI.
- **P1 — portfolio_modes_visibility**: Show portfolio modes: none, pasted_text, structured, image_capture.
- **P1 — prompt_benchmark_visibility**: Show quality, public safety, completeness, usefulness, missing_data and blockers.
- **P1 — admin_monitor_separation**: Keep ADMIN_MONITOR.html internal and separate from public UI shell.
- **P0 — public_deploy_gate**: Public deployment stays blocked until explicit approval.

## Allowed next actions

- `HUMAN_CONFIRM_CANONICAL_INDEX`
- `PREPARE_UI_POLISH_PATCH_PLAN_ONLY`
- `PREPARE_DATA_BINDING_PATCH_AFTER_APPROVAL`

## Forbidden next actions

- `EDIT_INDEX_HTML_NOW`
- `OVERWRITE_INDEX_HTML`
- `GENERATE_PUBLIC_INDEX_HTML`
- `CLASP_PUSH`
- `APPS_SCRIPT_EXECUTION`
- `PUBLIC_DEPLOY_WITHOUT_APPROVAL`
- `BROKER_OR_TRADING_EXECUTION`

## Safety

- NO_INDEX_HTML_EDIT
- NO_INDEX_HTML_GENERATION
- NO_PUBLIC_DEPLOY
- NO_CLASP
- NO_APPS_SCRIPT_EXECUTION
- NO_SHEET_WRITE
- NO_BROKER_ORDER_SIZING
