# MVP QAIC R17B — Drive Root Taxonomy Readout

Mode: read-only summary of R17 reports. No Drive write. No delete. No reset. No git add dot.

- Source R17 report dir: `docs\drive_reconcile\R17_REPORTS\R17_DRIVE_ROOT_TAXONOMY_AUDIT_20260630_235017`
- Inventory rows: `13`
- Plan rows: `13`
- Classification column: `classification`
- Item column: `name`
- Verdict: `R18_APPLY_NOT_AUTOMATIC_REQUIRES_HUMAN_VALIDATION`

## Counts

| Classification | Count | Items |
|---|---:|---|
| KEEP_ROOT_ACTIVE | 11 | 00_ADMIN / 01_DOCS / 02_SHEETS / 03_APPS_SCRIPT / 04_APPSHEET / 05_LOOKER / 06_STITCH / 07_ANTIGRAVITY / 08_QAIC_BRIDGE / 09_WEB_APP_IDE / 99_ARCHIVES |
| MOVE_TO_99_ARCHIVES_CANDIDATE | 1 | desktop.ini |
| MOVE_TO_DOMAIN_FOLDER_CANDIDATE | 0 |  |
| HOLD_REVIEW | 1 | source |

## Decision

R18 apply must not be automatic. Human validation is required before any Drive move.

## Action List

- `KEEP_ROOT_ACTIVE` — 00_ADMIN
- `KEEP_ROOT_ACTIVE` — 01_DOCS
- `KEEP_ROOT_ACTIVE` — 02_SHEETS
- `KEEP_ROOT_ACTIVE` — 03_APPS_SCRIPT
- `KEEP_ROOT_ACTIVE` — 04_APPSHEET
- `KEEP_ROOT_ACTIVE` — 05_LOOKER
- `KEEP_ROOT_ACTIVE` — 06_STITCH
- `KEEP_ROOT_ACTIVE` — 07_ANTIGRAVITY
- `KEEP_ROOT_ACTIVE` — 08_QAIC_BRIDGE
- `KEEP_ROOT_ACTIVE` — 09_WEB_APP_IDE
- `KEEP_ROOT_ACTIVE` — 99_ARCHIVES
- `HOLD_REVIEW` — source
- `MOVE_TO_99_ARCHIVES_CANDIDATE` — desktop.ini

