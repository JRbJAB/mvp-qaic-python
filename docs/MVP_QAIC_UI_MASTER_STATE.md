# MVP QAIC UI Master State

## Current stable UI chain

- CURRENT_UI_HEAD_BEFORE_P219D1: `5b1e839`
- CURRENT_UI_SOURCE_OLD_MENU: `mvp_qaic_py/p173_nicegui_private_local_runner.py`
- CURRENT_DURABLE_ADMIN_PACKAGE: `mvp_qaic_py/private_admin_app/`
- CURRENT_DURABLE_ADMIN_SHELL: `mvp_qaic_py/private_admin_app/shell.py`
- CURRENT_DURABLE_NAVIGATION: `mvp_qaic_py/private_admin_app/navigation.py`

## Operating rule

Every UI modification must finish with:

1. targeted tests,
2. full pytest,
3. Ruff check,
4. Ruff format check,
5. commit/tag/push if green,
6. NiceGUI local server launch,
7. human visual check.

## Target architecture

```text
MVP_QAIC_PY
├─ private_admin_app/
│  ├─ navigation.py
│  ├─ shell.py
│  ├─ pages/
│  └─ components/
├─ p173_nicegui_private_local_runner.py
├─ p219b_core_admin_registry.py
├─ p219c_core_admin_shell_wiring.py
└─ docs/MVP_QAIC_UI_MASTER_STATE.md
```

## Private admin navigation

- Dashboard
- Base Python
- Google Sheets
- Prompt Cockpit
- Réponses GEM
- Documents
- Architecture
- Configuration
- Audit / Runs

## Safety locks

- HUMAN_REVIEW_ONLY
- NO_AUTO_APPLY
- NO_PROVIDER_CALL
- NO_GEM_CALL_FROM_ADMIN
- NO_BROKER
- NO_ORDER
- NO_SIZING
- PRIVATE_ADMIN_ONLY

## Next

`P219D2_INTEGRATE_REAL_P173_MENU_DETAILS_AND_PAGE_STUBS_VISUAL_GATE`
## P219D2 normal preview target

- CURRENT_NORMAL_PREVIEW_APP: `mvp_qaic_py/private_admin_app/app.py`
- CURRENT_VISUAL_URL: `http://127.0.0.1:8096`
- CURRENT_UI_MODE: `NORMAL_LEFT_MENU_PREVIEW`
- CURRENT_NEXT_BATCH: `P219D3_POLISH_REAL_PAGE_CONTENT_AND_LINKS_VISUAL_GATE`

P219D2 converts the durable shell into a normal NiceGUI preview with left drawer and route pages.
## P219D2-R4 runtime repair

- RUNTIME_ERROR_REPAIRED: `LeftDrawer nested inside Row`
- CURRENT_VISUAL_URL: `http://127.0.0.1:8097`
- CURRENT_UI_MODE: `NORMAL_LEFT_MENU_PREVIEW_TOPLEVEL_LAYOUT`
- CURRENT_NEXT_BATCH: `P219D3_POLISH_REAL_PAGE_CONTENT_AND_LINKS_VISUAL_GATE`

NiceGUI top-level layout rule: `ui.left_drawer()` and `ui.header()` must be direct page children, not nested inside `ui.row()` or `ui.column()`.
## P219E1-R3 P173 baseline frame anchorless polish

- BASELINE_FRAME: `mvp_qaic_py/p173_nicegui_private_local_runner.py`
- OFFICIAL_FINAL_UI: `False`
- PURPOSE: apply audit-driven UI suggestions on recovered baseline frame
- PREVIEW_COMMAND: `python -m mvp_qaic_py.p173_nicegui_private_local_runner --project-root . --host 127.0.0.1 --port 8088 --serve-private`
- NEXT: `P219E2_P173_APPLY_AUDIT_UI_CONTENT_FAST_FUSE`