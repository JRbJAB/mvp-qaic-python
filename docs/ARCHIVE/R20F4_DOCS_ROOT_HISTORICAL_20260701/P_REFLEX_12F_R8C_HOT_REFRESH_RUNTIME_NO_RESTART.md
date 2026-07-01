# P_REFLEX_12F_R8C - Hot refresh runtime without server restart

Adds a refresh command that regenerates the global migration matrix and syncs the updated docs into the active LocalAppData Reflex runtime.

Policy:

- No public deploy.
- No live action.
- No broker/order/sizing.
- No Sheets write.
- No BigQuery write.
- No drive scan.
- No server start.
- No mandatory server restart.

Command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_P_REFLEX_12F_REFRESH_GLOBAL_MIGRATION_MATRIX.ps1 -RepoRoot "<repo>"
```

Expected operator flow after the server is already running:

1. Run the refresh command.
2. Wait for `RUNTIME_SYNC_OK=True` and `HOT_RELOAD_TOUCH_OK=...`.
3. Refresh Mission Control in the browser with Ctrl+F5.

The command updates the runtime copies of `docs/MIGRATION_GLOBAL_MATRIX*` and touches the runtime Mission Control Python file to trigger Reflex hot reload. `/migration/global` remains a detail route; Mission Control remains the operator entry point.
