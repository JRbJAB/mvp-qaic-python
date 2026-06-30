# MVP QAIC Docs Drive Reconcile - R8 Numerated Folders External Rangement Plan

## Mode

- READ ONLY: TRUE
- NO_WRITE_SOURCE_DRIVE: TRUE
- NO_WRITE_TARGET_DOCS: TRUE
- NO_DRIVE_MOVE: TRUE
- NO_GIT_ACTION: TRUE
- APPLY_REQUIRES_EXPLICIT_VALIDATION: TRUE

## Scope decision

R6/R7/R7B closed the local docs final fusion inbox and reports. R8 is only the external rangement plan for numbered root folders.

## Root folder summary

| Root | Files | Bucket | Status | Next |
|---|---:|---|---|---|
| `00_ADMIN` | 34 | `ADMIN_GOVERNANCE_EXTERNAL_REVIEW` | `PARTIAL_DOCS_SELECTED_R6_REMAINING_EXTERNAL_ADMIN_REVIEW` | Review admin docs against fusion_inbox_R6, then archive stale admin packs outside docs/FINAL. |
| `01_DOCS` | 1464 | `CANONICAL_DOCS_REVIEW_QUEUE` | `CANONICAL_DOCS_SOURCE_PARTIAL_R6_R7B_DONE` | Do not bulk move. Continue final-docs fusion review from R6/R7B reports. |
| `02_BUILD` | 1866 | `EXTERNAL_ARCHIVE_BUILD_OUTPUTS` | `MASS_BUILD_OUTPUTS_EXTERNAL_ARCHIVE_CANDIDATE` | Archive as build artifacts; never import bulk into repo docs. |
| `02_DELIVERABLES_ZIP` | 27 | `EXTERNAL_ARCHIVE_DELIVERABLE_ZIPS` | `DELIVERABLE_ZIPS_EXTERNAL_ARCHIVE_CANDIDATE` | Archive ZIP deliverables by date/prefix outside docs final. |
| `02_SHEETS` | 47 | `EXTERNAL_REFERENCE_SHEETS` | `SHEETS_REFERENCES_KEEP_EXTERNAL` | Keep as data/sheet references; import only explicit docs/manifests later. |
| `03_APPS_SCRIPT` | 140 | `EXTERNAL_CODE_APPS_SCRIPT` | `APPS_SCRIPT_SOURCE_MIRROR_EXTERNAL_CODE_SCOPE` | Do not mix with docs final. Treat in separate code/mirror audit if needed. |
| `03_DEV` | 181 | `EXTERNAL_ARCHIVE_DEV_RUNS` | `DEV_RUN_OUTPUTS_EXTERNAL_REVIEW` | Archive/dev-run index separately after extracting any remaining handoff memos. |
| `03_EXPORTS` | 4278 | `EXTERNAL_ARCHIVE_EXPORTS` | `MASS_EXPORTS_EXTERNAL_ARCHIVE_CANDIDATE` | Archive CSV/export mass separately. No bulk import into docs. |
| `04_APPSHEET` | 20 | `EXTERNAL_APPSHEET_REVIEW` | `APPSHEET_SCOPE_PARTIAL_DOC_IMPORTED_R6` | R6 imported one AppsSheet runbook. Keep remaining AppsSheet material external pending review. |
| `04_DELIVERABLES_ZIP` | 7 | `EXTERNAL_ARCHIVE_DELIVERABLE_ZIPS` | `DELIVERABLE_ZIPS_EXTERNAL_ARCHIVE_CANDIDATE` | Archive ZIP deliverables by date/prefix outside docs final. |
| `05_LOOKER` | 5 | `EXTERNAL_LOOKER_REFERENCE` | `LOOKER_SCOPE_EXTERNAL_REFERENCE` | Keep external; import only approved docs later. |
| `06_STITCH` | 25 | `EXTERNAL_STITCH_REFERENCE` | `STITCH_SCOPE_EXTERNAL_REFERENCE` | Keep external; import only approved docs later. |
| `07_ANTIGRAVITY` | 21 | `EXTERNAL_ANTIGRAVITY_REFERENCE` | `ANTIGRAVITY_SCOPE_EXTERNAL_REFERENCE` | Keep external; R6 already selected prompt-related docs where applicable. |
| `08_QAIC_BRIDGE` | 19 | `EXTERNAL_QAIC_BRIDGE_REFERENCE` | `QAIC_BRIDGE_EXTERNAL_REFERENCE` | Keep external until QAIC bridge docs/code audit. |
| `09_WEB_APP_IDE` | 9 | `EXTERNAL_WEB_APP_IDE_REVIEW` | `WEB_APP_IDE_EXTERNAL_REVIEW` | Review for UI process docs only; no bulk import. |
| `99_ARCHIVES` | 93 | `EXTERNAL_ARCHIVES_KEEP` | `PREEXISTING_ARCHIVES_KEEP_EXTERNAL` | Keep as archives. Do not import old archives into repo docs. |
| `P27A2A_UX_LOCK_CONTRACT_20260618` | 7 | `UNCLASSIFIED` | `UNCLASSIFIED` | Manual review required. |
| `P44_FIELD_EMOJI_METRIC_DERIVATION_20260618_231547` | 7 | `UNCLASSIFIED` | `UNCLASSIFIED` | Manual review required. |
| `P46A_APPS_SCRIPT_GLOBAL_AUDIT_READONLY_20260619_083322` | 1 | `UNCLASSIFIED` | `UNCLASSIFIED` | Manual review required. |
| `P46B_LEXIQUE_CORE_TARGETED_AUDIT_READONLY_20260619_084756` | 1 | `UNCLASSIFIED` | `UNCLASSIFIED` | Manual review required. |
| `source` | 25 | `EXTERNAL_SOURCE_REFERENCE` | `SOURCE_FOLDER_EXTERNAL_REFERENCE` | Keep external unless a specific source doc is selected. |
| `🧭 R16E — FUSION MAJ Docs Finales CDC Archi Web Instructions` | 2 | `UNCLASSIFIED` | `UNCLASSIFIED` | Manual review required. |

## Outputs

- `R8_ROOT_FOLDER_SUMMARY.csv`
- `R8_EXTERNAL_RANGEMENT_PLAN_NEEDS_VALIDATION.csv`
- `R8_SAMPLE_FILES_BY_ROOT_FIRST_40.csv`
- `R8_STATUS.json`
- `R8_ERRORS.csv`

## Recommended next

Validate only the external rangement plan, then run an R9 apply that creates/moves under an external archive/review tree. Do not mix R9 with docs/FINAL fusion commits.
