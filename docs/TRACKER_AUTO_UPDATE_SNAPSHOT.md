# Auto-update Trackers — Snapshot local

- Status: `LOCAL_FILES_SYNC_REQUIRED`
- Mode: `LOCAL_FILES_ONLY`
- Sync state: `SYNC_REQUIRED_WHEN_RUNTIME_IS_OUTSIDE_REPO`
- Generated at: `2026-06-26T08:55:44+00:00`

## Rôles

- Dev Tracking: Suit lots Pxxx, commits, tags, tests, gates, smokes runtime, incidents et exports locaux.
- CDC Tracker: Suit le cahier des charges produit/architecture depuis docs/WEB_ARCHITECTURE_SITEMAP.json.
- Migration Tracker: Suit la migration Sheets/Apps Script/exports vers Reflex/Python depuis docs/MIGRATION_TRACKER.json et l'inventaire CLASP CSV.

## Sources locales

- `dev_tracking`: exists=`True` path=`G:/Mon Drive/👥 JULIEN [Perso]/📈 Trading JRb/Solutions & Dev (Trading JRb)/MVP_QAIC_PY/05_EXPORTS`
  - file_count: `1506`
- `cdc_tracker`: exists=`True` path=`G:/Mon Drive/👥 JULIEN [Perso]/📈 Trading JRb/Solutions & Dev (Trading JRb)/MVP_QAIC_PY/docs/WEB_ARCHITECTURE_SITEMAP.json`
- `migration_tracker`: exists=`True` path=`G:/Mon Drive/👥 JULIEN [Perso]/📈 Trading JRb/Solutions & Dev (Trading JRb)/MVP_QAIC_PY/docs/MIGRATION_TRACKER.json`
- `clasp_imports`: exists=`False` path=`MVPQAIC_CLASP_IMPORTS_ALL.csv`

## Sécurité

- `NO_PUBLIC_DEPLOY` = `True`
- `NO_LIVE_ACTION` = `True`
- `NO_BROKER_ORDER_SIZING` = `True`
- `NO_SHEET_WRITE` = `True`
- `NO_BIGQUERY_WRITE` = `True`
- `HUMAN_REVIEW_ONLY` = `True`
