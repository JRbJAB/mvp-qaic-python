# P168F — Operator export capture instructions

## Goal

Prepare the five local CSV snapshots required before the local cache can be built.

Current preferred path: `LOCAL_EXPORT_IMPORT_FIRST`.

## Dropzone

`C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901\00_OPERATOR_EXPORTS\P168F_REQUIRED_SNAPSHOTS`

## Required exports

| Snapshot | Expected file | Operator action |
|---|---|---|
| CONFIG | `MVP_QAIC_CONFIG.csv` | Export the CONFIG tab/range as CSV and save it with this exact name. |
| PROMPT_SOURCE_REGISTRY | `MVP_QAIC_PROMPT_SOURCE_REGISTRY.csv` | Export the prompt/source registry tab or approved source table. |
| DECISION_JOURNAL | `MVP_QAIC_DECISION_JOURNAL.csv` | Export the decision journal tab/range as CSV. |
| PROMPT_REVIEW_WORKBENCH | `MVP_QAIC_PROMPT_REVIEW_WORKBENCH.csv` | Export the current prompt review/workbench table as CSV. |
| LEXIQUE_OR_COCKPIT_DATA | `MVP_QAIC_LEXIQUE_OR_COCKPIT_DATA.csv` | Export the approved lexique or current useful cockpit dataset. |

## Safety

- No Google Sheets write.
- No live Google API call from Python.
- No Apps Script execution.
- No CLASP push.
- No broker, order, or sizing.
- No runtime prompt modification.

## After placing files

Run the next cache validation/build step:

`P168G_LOCAL_CACHE_BUILD_FROM_OPERATOR_EXPORTS`
