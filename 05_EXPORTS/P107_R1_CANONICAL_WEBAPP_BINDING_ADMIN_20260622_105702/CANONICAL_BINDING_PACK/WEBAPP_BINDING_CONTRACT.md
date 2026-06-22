# MVP QAIC — Canonical WebApp Binding Contract

## Status

`CANONICAL_BINDING_READY`

## Canonical UI

- Canonical file: `Index.html`
- Policy: `DO_NOT_OVERWRITE_FROM_PYTHON`
- Python role: `generate_data_contracts_context_packs_and_admin_monitor_only`
- Human review before UI change: `True`

## Allowed generated files

- `data/webapp_pack.json`
- `data/context_pack.json`
- `data/prompt_payload.json`
- `data/binding_contract.json`
- `data/admin_status.json`
- `WEBAPP_BINDING_CONTRACT.md`
- `admin/ADMIN_MONITOR.html`
- `admin/README_ADMIN_MONITOR.md`

## Forbidden generated files

- `index.html`
- `Index.html`
- `MVPQAIC_Index.html`
- `Code.gs`
- `appsscript.json`

## Safety

- NO_REVOLUTX_REAL_ACCESS
- NO_BROKER
- NO_ORDER
- NO_CANCEL
- NO_REPLACE_ORDER
- NO_AUTO_SIZING
- NO_SECRET_LOG
- NO_SHEET_WRITE
- NO_APPS_SCRIPT_EXECUTION
- NO_CLASP
- NO_PUBLIC_DEPLOY

## Next

`P108_UI_POLISH_USING_CANONICAL_INDEX_OR_PUBLIC_DEPLOY_DECISION_GATE`
