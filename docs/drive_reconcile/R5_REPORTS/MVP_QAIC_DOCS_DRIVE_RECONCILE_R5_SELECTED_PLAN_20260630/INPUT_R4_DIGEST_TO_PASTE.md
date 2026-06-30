# MVP QAIC Docs Drive Reconcile - R4 Digest

## Run

- R1_OUT_ROOT: `C:\Users\Julie\Downloads\MVP_QAIC_DOCS_DRIVE_RECONCILE_AUDIT_R1_PS51_FIX_20260630_174335`
- R4_OUT_ROOT: `C:\Users\Julie\Downloads\MVP_QAIC_DOCS_DRIVE_RECONCILE_R4_DIGEST_PY_SAFE_20260630_180906`
- MODE: READ_ONLY_DIGEST
- NO_WRITE_SOURCE: TRUE
- NO_WRITE_TARGET_DOCS: TRUE
- NO_GIT_ACTION: TRUE

## Inventory counts

- SOURCE_FILE_COUNT: 8420
- TARGET_DOCS_FILE_COUNT: 284
- SOURCE_ENUM_ERROR_COUNT: 0
- TARGET_ENUM_ERROR_COUNT: 0
- PROPOSED_ACTION_COUNT: 8637
- PROPOSED_FOLDER_COUNT: 1405

## Proposed actions by action label

- IMPORT_SOURCE_ONLY_CANDIDATE: 7204
- IGNORE_WINDOWS_NOISE: 1133
- TARGET_ONLY_KEEP_NO_SOURCE_MATCH: 217
- REVIEW_SAME_NAME_DIFFERENT_HASH_OR_PATH: 56
- ARCHIVE_SOURCE_ALREADY_PRESENT_BY_HASH: 27

## Source top folders

- 03_EXPORTS: 4278
- 02_BUILD: 1976
- 01_DOCS: 1477
- 03_DEV: 181
- 03_APPS_SCRIPT: 140
- 99_ARCHIVES: 93
- 02_SHEETS: 47
- 00_ADMIN: 34
- 02_DELIVERABLES_ZIP: 31
- 06_STITCH: 25
- source: 25
- 07_ANTIGRAVITY: 21
- 04_APPSHEET: 20
- 08_QAIC_BRIDGE: 19
- 09_WEB_APP_IDE: 9
- 04_DELIVERABLES_ZIP: 7
- P27A2A_UX_LOCK_CONTRACT_20260618: 7
- P44_FIELD_EMOJI_METRIC_DERIVATION_20260618_231547: 7
- 05_LOOKER: 5
- 🧭 R16E — FUSION MAJ Docs Finales CDC Archi Web Instructions: 2
- 🛠️ MVP QAIC — Crypto Signal OS — DEV.gsheet: 1
- MVPQAIC_CLASP_GIT_EXPORT_ALLINONE_0.1.7_REAUTH_PULL_VALIDATE_BACKUP.ps1: 1
- MVP_QAIC_P27D11A_CONTENT_ENRICHMENT_REVIEW_PACK_20260618_160310.zip: 1
- MVP_QAIC_P27D11B_CONTENT_WORKBENCH_LOCAL_ONLY_20260618_161255.zip: 1
- MVP_QAIC_P27D11C_FIRST_10_TERMS_DRAFT_20260618_162307.zip: 1
- MVP_QAIC_P27D11D_HUMAN_REVIEW_FIRST_10_20260618_163009.zip: 1
- MVP_QAIC_P27D11E_REVISED_FIRST_10_DRAFTS_20260618_164534.zip: 1
- MVP_QAIC_DEV_MEMO_COMPACT_20260618_165146.gdoc: 1
- MVP_QAIC_P27D11F_TO_P27D14_MAXI_20260618_165756.zip: 1
- MVP_QAIC_P28_MAXI_CONTENT_EXTENSION_20260618_170936.zip: 1

## Target docs top folders

- dev_tracking: 34
- FINAL: 34
- ARCHIVE: 33
- mvp_ui: 32
- audit: 29
- brand_assets: 29
- qaic_public_contracts: 15
- INDEX: 12
- ARCHIVE_MANIFESTS: 7
- UX: 6
- FINAL_DRAFTS: 4
- GOVERNANCE: 4
- desktop.ini: 1
- MIGRATION_DECISION_OVERLAY.json: 1
- MIGRATION_DECISION_OVERLAY.zip: 1
- MIGRATION_DECISION_QUEUE.json: 1
- MIGRATION_GLOBAL_MATRIX.csv: 1
- MIGRATION_GLOBAL_MATRIX.json: 1
- MIGRATION_GLOBAL_MATRIX.md: 1
- MIGRATION_GLOBAL_MATRIX_SUMMARY.json: 1
- MIGRATION_OS_LIVE_PAYLOAD.json: 1
- MIGRATION_OS_REFRESH_SIGNAL.txt: 1
- MIGRATION_STATUS_LEGEND.json: 1
- MIGRATION_TRACKER.json: 1
- MIGRATION_TRACKER.md: 1
- MVPQAIC_CLASP_IMPORTS_ALL.csv: 1
- MVPQAIC_CLASP_IMPORTS_ALL_HEADERS.csv: 1
- MVP_QAIC_BRAND_ASSETS_INSTRUCTIONS.md: 1
- MVP_QAIC_P173_BASELINE_FRAME.md: 1
- MVP_QAIC_UI_MASTER_STATE.md: 1

## Source file extensions

- .csv: 3210
- .md: 2089
- .ini: 1134
- .json: 763
- .zip: 318
- .js: 295
- .png: 141
- .svg: 133
- .html: 81
- .diff: 72
- .txt: 65
- .gs: 30
- [no_ext]: 28
- .css: 26
- .ps1: 17
- .gdoc: 13
- .gsheet: 1
- .py: 1
- .pdf: 1
- .xlsx: 1
- .bak: 1

## Target docs file extensions

- .md: 148
- .ini: 44
- .json: 38
- .csv: 28
- .png: 14
- .zip: 4
- .svg: 3
- .html: 2
- .txt: 1
- .ico: 1
- .css: 1

## Immediate interpretation

- Do not apply archive/fusion yet.
- Use this digest plus review_sample_actions_first_80.csv to validate the R5 apply scope.
- Recommended R5 should be selective: docs/final docs first, then archive duplicate ZIP/build/export folders separately.
- Keep Drive live moves separate from local repo docs commits.

## Files copied into this digest folder

- AUDIT_REPORT_MVP_QAIC_DOCS_DRIVE_RECONCILE_R1_PS51_FIX.md
- proposed_actions_NEEDS_VALIDATION.csv
- proposed_docs_folders_NEEDS_VALIDATION.csv
- review_sample_actions_first_80.csv
- review_sample_folders_first_80.csv
- RUN_STATUS.json
- source_drive_inventory.csv
- source_inventory_errors.csv
- target_docs_inventory.csv
- target_inventory_errors.csv
