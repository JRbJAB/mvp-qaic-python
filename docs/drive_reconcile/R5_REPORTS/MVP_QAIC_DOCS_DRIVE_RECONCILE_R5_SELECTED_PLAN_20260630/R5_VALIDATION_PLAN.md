# MVP QAIC Docs Drive Reconcile - R5 Selected Plan

## Verdict

R5 is a validation plan only. It does not apply any archive, copy, move, git add, commit, tag, or push.

The R4 digest showed a massive source tree. R5 narrows it to final documentation, governance, CDC, runbook, instructions, prompt, architecture, and R16E UI process material.

## Counts

| Metric | Count |
|---|---:|
| Source files from R1 | 8420 |
| Target docs files from R1 | 284 |
| Proposed actions from R1 | 8637 |
| R5 selected actions | 128 |
| R5 selected import candidates | 85 |
| R5 selected conflict reviews | 28 |
| R5 selected duplicate/archive reviews | 15 |
| R5 excluded/deferred actions | 8509 |
| R5 selected folders | 118 |

## Selected by action

- IMPORT_SOURCE_ONLY_CANDIDATE: 85
- REVIEW_SAME_NAME_DIFFERENT_HASH_OR_PATH: 28
- ARCHIVE_SOURCE_ALREADY_PRESENT_BY_HASH: 15

## Selected by bucket

- SELECT_01_DOCS_RUNBOOK_CANDIDATE: 30
- REVIEW_CONFLICT_SAME_NAME_DIFFERENT_HASH: 28
- ARCHIVE_SOURCE_DUPLICATE_EXACT_HASH_REVIEW: 15
- SELECT_01_DOCS_README_CANDIDATE: 12
- SELECT_01_DOCS_PROMPTS_CANDIDATE: 7
- SELECT_00_ADMIN_INSTRUCTIONS_METADATA: 5
- SELECT_01_DOCS_INSTRUCTIONS_CANDIDATE: 5
- SELECT_MISC_FINAL_DOCS_CANDIDATE: 4
- SELECT_01_DOCS_CDC_CANDIDATE: 4
- SELECT_01_DOCS_MANIFEST_CANDIDATE: 4
- REVIEW_DRIVE_SHORTCUT_EXPORT_REQUIRED: 3
- SELECT_01_DOCS_ARCHITECTURE_CANDIDATE: 3
- SELECT_FINAL_FUSED_CANDIDATE: 3
- SELECT_01_DOCS_PLANNING_CANDIDATE: 2
- SELECT_01_DOCS_NOTICE_UTILISATION_CANDIDATE: 1
- SELECT_01_DOCS_SYNTHESE_CANDIDATE: 1
- SELECT_01_DOCS_LEXIQUE_CANDIDATE: 1

## Selected by source top folder

- 01_DOCS: 120
- 00_ADMIN: 5
- 🧭 MVP_QAIC_FINAL_DOCS_FUSION_REFLEX_UI_PROCESS_R16E.md.gdoc: 1
- 04_APPSHEET: 1
- 🧭 R16E — FUSION MAJ Docs Finales CDC Archi Web Instructions: 1

## R5 scope retained

Included:

- Root R16E fusion document/process references.
- `01_DOCS/FINAL_FUSED`.
- `01_DOCS/FINAL_DRAFTS`.
- `01_DOCS/CDC`.
- `01_DOCS/RUNBOOK`.
- `01_DOCS/INSTRUCTIONS`.
- `01_DOCS/ARCHITECTURE`.
- `01_DOCS/PROMPTS`.
- `01_DOCS/PLANNING`, `INDEX`, `MANIFEST`, `README`, `NOTICE`, `SYNTHESE`, `LEXIQUE`.
- Limited admin instruction/final metadata from `00_ADMIN`.

Excluded/deferred:

- `03_EXPORTS`.
- `02_BUILD`.
- `03_DEV`.
- `03_APPS_SCRIPT`.
- `02_DELIVERABLES_ZIP`.
- `04_DELIVERABLES_ZIP`.
- `99_ARCHIVES`.
- massive `01_DOCS/VALIDATION` corpus.
- ZIPs, binaries, web build assets, Apps Script code, CSV bulk exports.
- Windows noise (`desktop.ini`, `.ini`).

## Important handling rules

1. Do not import `.gdoc` or `.gsheet` shortcuts as final content.
   - They require Drive export/fetch before R6.
   - The R16E Google Doc is especially important and should be exported as Markdown/text, not copied as a `.gdoc` pointer.

2. Do not overwrite conflicts.
   - The 28 selected conflict rows require manual comparison.
   - R6 should stage conflict files into `docs/FINAL/fusion_inbox_R6/conflicts_review/`, not overwrite existing `docs/FINAL`.

3. Do not archive source duplicates until validation.
   - The 15 selected duplicate/archive rows can be moved in Drive only after explicit validation.
   - Drive live moves must be separate from local repo docs commits.

4. R6 apply should be local repo only first.
   - Copy selected files into `docs/FINAL/fusion_inbox_R6/`.
   - Add report files into `docs/drive_reconcile/R5_REPORTS/`.
   - No direct replacement of final docs until visual/human review.

## Proposed R6 local apply

After validation, create a pack that:

- creates `docs/FINAL/fusion_inbox_R6/`;
- copies selected source-only files from local Drive mount to the fusion inbox;
- stores R5 CSV/MD reports under `docs/drive_reconcile/R5_REPORTS/`;
- skips `.gdoc`/`.gsheet` shortcuts unless an exported `.md` payload is supplied;
- stages only these paths;
- runs a docs hygiene test;
- commit/tag/push with a clear docs reconcile tag.

Suggested tag:

```text
mvp-qaic-docs-drive-reconcile-r6-selected-final-docs-20260630
```

## Proposed Drive live archive pass

Separate pass only after local R6 validation:

- create a Drive archive folder under `99_ARCHIVES` or a dedicated `R6_ARCHIVED_ALREADY_PRESENT_BY_HASH_YYYYMMDD`;
- move only exact duplicate source files listed in `R5_DUPLICATES_15_ARCHIVE_CANDIDATES.csv`;
- do not move conflicts or source-only docs.

## Files in this R5 pack

- `R5_SELECTED_ACTIONS_NEEDS_VALIDATION.csv`
- `R5_SELECTED_IMPORTS_TO_FUSION_INBOX_NEEDS_VALIDATION.csv`
- `R5_CONFLICTS_28_REVIEW_BEFORE_OVERWRITE.csv`
- `R5_DUPLICATES_15_ARCHIVE_CANDIDATES.csv`
- `R5_EXCLUDED_DEFERRED_MASS_IMPORT.csv`
- `R5_SELECTED_FOLDERS_NEEDS_VALIDATION.csv`
- `R5_SUMMARY.json`
- `R5_VALIDATION_PLAN.md`

## Operator validation needed

Validate one of:

```text
VALIDATE_R6_LOCAL_FUSION_INBOX_ONLY
VALIDATE_R6_LOCAL_FUSION_INBOX_PLUS_REPORTS
STOP_AND_REVIEW_CONFLICTS_FIRST
ADJUST_R5_SCOPE
```
