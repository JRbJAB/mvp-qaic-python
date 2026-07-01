# REFLEX Windows Runtime Audit - MVP QAIC

## Decision
Use a simple foreground local starter in `scripts/START_REFLEX_LOCAL_SAFE.ps1`.

## Why
- Reflex `run` is a development server command with hot reload.
- Windows local ports 3000/8000 must be checked before launch.
- The server should stay visible in one PowerShell window so crashes are visible.
- The runtime must run from LocalAppData, not from Google Drive, to reduce path/sync issues.

## Commands

Start:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\START_REFLEX_LOCAL_SAFE.ps1
```

Status:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\STATUS_REFLEX_LOCAL_SAFE.ps1
```

Stop:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\STOP_REFLEX_LOCAL_SAFE.ps1
```

## Safety
NO_PUBLIC_DEPLOY=true
NO_LIVE_ACTION=true
NO_BROKER_ORDER_SIZING=true
NO_SHEET_WRITE=true
NO_BIGQUERY_WRITE=true
HUMAN_REVIEW_ONLY=true

## Notes
The start script sets REFLEX_DIR under LocalAppData and keeps Reflex in the foreground with logs under LocalAppData/MVP_QAIC_REFLEX_LOGS.
