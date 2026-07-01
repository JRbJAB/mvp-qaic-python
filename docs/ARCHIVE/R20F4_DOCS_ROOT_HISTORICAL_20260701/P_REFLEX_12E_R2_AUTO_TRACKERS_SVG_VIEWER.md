
# P_REFLEX_12E-R2 — Auto Trackers + SVG Viewer + Repo Locator Hard Fix

## Objectif

Batch maxi fast & fuse pour reprendre après les échecs P12D/P12E sans dépendance au lecteur `Q:`.

## Ce que le batch ajoute

- `mvp_qaic_reflex_ui/tracker_auto_update.py`
- `mvp_qaic_reflex_ui/svg_schema_viewer.py`
- `mvp_qaic_reflex_ui/mission_control_auto_update_panel.py`
- `mvp_qaic_reflex_ui/auto_update_trackers_page.py`
- route Reflex best-effort `/architecture-web/schema`
- route Reflex best-effort `/trackers/auto-update`
- snapshot local `docs/TRACKER_AUTO_UPDATE_SNAPSHOT.json/.md`
- script runtime permanent `scripts/RUN_P_REFLEX_12E_R2_PERMANENT_LOCAL_SERVER_WITH_SYNC.ps1`
- tests ciblés P12E-R2

## Garde-fous

- `NO_PUBLIC_DEPLOY=true`
- `NO_LIVE_ACTION=true`
- `NO_BROKER_ORDER_SIZING=true`
- `NO_SHEET_WRITE=true`
- `NO_BIGQUERY_WRITE=true`
- `HUMAN_REVIEW_ONLY=true`
- `NO_SERVER_START_BY_BATCH=true`

## Point dur corrigé

Le locator ne teste `Q:\MVP_QAIC_PY` que si `Test-Path Q:\` est vrai. Le fallback durable `G:\...\MVP_QAIC_PY` est ensuite utilisé.

## Serveur permanent

Le batch ne démarre pas le serveur. Après validation du batch, lancer manuellement :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_P_REFLEX_12E_R2_PERMANENT_LOCAL_SERVER_WITH_SYNC.ps1
```

Ce script synchronise vers :

`C:\Users\Julie\AppData\Local\MVP_QAIC_REFLEX_RUNTIME\P_REFLEX_06C_20260625_200632`

puis garde un watcher de sync actif.
