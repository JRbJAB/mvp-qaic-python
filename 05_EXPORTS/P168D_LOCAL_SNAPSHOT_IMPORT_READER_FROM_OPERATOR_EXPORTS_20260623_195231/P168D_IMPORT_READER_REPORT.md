# P168D — Local snapshot import reader from operator exports

## Decision

Use local operator exports first. The Python reader validates files, counts rows/columns, computes checksums, and prepares a local import queue. It does not write Google Sheets and does not call Google APIs.

## Source

- P168C export: `C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901\05_EXPORTS\P168C_SHEETS_READONLY_EXPORT_IMPORT_OR_API_BINDING_20260623_194731`
- P168C preferred path now: `LOCAL_EXPORT_IMPORT_FIRST`
- Operator export directory: `C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901\01_INPUTS\P168D_OPERATOR_SHEETS_EXPORTS`
- Required manifest rows: `5`
- Ready import rows: `0`
- Blocker count: `0`

## Safety

- Google Sheets write: `False`
- Live Google API call from Python: `False`
- Apps Script execution: `False`
- CLASP push: `False`
- Broker/order/sizing: `False`

## Validation preview

| tab_name | local_file | file_exists | reader_status | import_ready | issue_code |
| --- | --- | --- | --- | --- | --- |
| CONFIG | MVP_QAIC_DEV__CONFIG__A1_D200.csv | False | WAITING_FOR_OPERATOR_EXPORT | NO | MISSING_LOCAL_FILE |
| LEXIQUE_CRYPTO_APPROVED | MVP_QAIC_DEV__LEXIQUE_CRYPTO_APPROVED__A1_Z5000.csv | False | WAITING_FOR_OPERATOR_EXPORT | NO | MISSING_LOCAL_FILE |
| PROMPT_IMPROVEMENT_QUEUE | MVP_QAIC_DEV__PROMPT_IMPROVEMENT_QUEUE__A1_Z5000.csv | False | WAITING_FOR_OPERATOR_EXPORT | NO | MISSING_LOCAL_FILE |
| DECISION_JOURNAL | MVP_QAIC_DEV__DECISION_JOURNAL__A1_Z5000.csv | False | WAITING_FOR_OPERATOR_EXPORT | NO | MISSING_LOCAL_FILE |
| GPT_QUALITY_DASHBOARD | MVP_QAIC_DEV__GPT_QUALITY_DASHBOARD__A1_Z2000.csv | False | WAITING_FOR_OPERATOR_EXPORT | NO | MISSING_LOCAL_FILE |
