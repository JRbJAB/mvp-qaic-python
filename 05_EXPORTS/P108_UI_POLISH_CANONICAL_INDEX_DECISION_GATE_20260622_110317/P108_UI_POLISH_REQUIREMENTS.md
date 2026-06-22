# MVP QAIC — P108 UI Polish Decision Gate

## Decision status

`REVIEW_REQUIRED`

## Canonical UI policy

- File: `Index.html`
- Policy: `DO_NOT_OVERWRITE_FROM_PYTHON`
- Python role: `generate_data_contracts_context_packs_and_admin_monitor_only`

## Canonical index candidates

- `REVIEW_REQUIRED`: no local candidate found in bounded scan.

## UI polish requirements

- **P0 — ui_shell_preserve_canonical_index**: Preserve validated WebApp Index.html. Python must not overwrite it.
- **P0 — bind_data_packs**: Bind generated webapp_pack, context_pack, prompt_payload, benchmark and admin status to the existing UI shell.
- **P1 — portfolio_input_modes_visible**: Expose portfolio modes: none, pasted_text, structured, image_capture.
- **P1 — benchmark_cards_visible**: Expose quality, public safety, data completeness and public usefulness scores.
- **P1 — missing_data_and_blockers_visible**: Expose missing_data and blockers clearly before any human review output.
- **P1 — admin_monitor_internal_only**: Keep ADMIN_MONITOR.html as internal local admin/suivi, not public UI shell.
- **P0 — public_deploy_explicit_gate**: Public deploy remains blocked until explicit human approval.

## Allowed next actions

- `HUMAN_REVIEW_CANONICAL_INDEX`
- `PREPARE_UI_POLISH_PATCH_PLAN_ONLY`
- `BIND_JSON_DATA_PACKS_TO_CANONICAL_UI_AFTER_APPROVAL`

## Forbidden next actions

- `OVERWRITE_INDEX_HTML`
- `GENERATE_NEW_PUBLIC_INDEX_HTML`
- `CLASP_PUSH`
- `APPS_SCRIPT_EXECUTION`
- `PUBLIC_DEPLOY_WITHOUT_APPROVAL`
- `BROKER_OR_TRADING_EXECUTION`

## Safety

- NO_INDEX_HTML_EDIT
- NO_REVOLUTX_REAL_ACCESS
- NO_BROKER
- NO_ORDER
- NO_AUTO_SIZING
- NO_SHEET_WRITE
- NO_APPS_SCRIPT_EXECUTION
- NO_CLASP
- NO_PUBLIC_DEPLOY
