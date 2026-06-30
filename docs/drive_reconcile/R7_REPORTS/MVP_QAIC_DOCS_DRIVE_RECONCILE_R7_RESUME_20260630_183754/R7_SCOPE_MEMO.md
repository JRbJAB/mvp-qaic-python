# MVP QAIC Docs Drive Reconcile - R7 Resume Commit UTF8

## Purpose

R7 resumes after R6 copied selected docs into the local fusion inbox and failed only during git add output decoding on Windows cp1252.

## Safety

- No Drive move.
- No source Drive write.
- No target overwrite.
- No git add dot.
- Targeted staging only.

## Residual files audit handling

Residual files were not ignored. They are kept out of the R6 apply and remain covered by R5/R6 reports:

- conflicts review stays separated from final docs overwrite;
- duplicate archive candidates stay separated from import;
- excluded mass import stays deferred;
- native Google Drive files stay deferred for export-aware handling.

## Numbered Drive folders handling

Numbered root folders such as 00_ADMIN, 01_DOCS, 02_BUILD, 03_EXPORTS, 03_DEV, 03_APPS_SCRIPT, 09_WEB_APP_IDE and 99_ARCHIVES were audited in R1/R4/R5.
R6 intentionally does not reorganize these folders. External rangement must be a separate R8 plan/apply pass after validation.

## Counts

- fusion_inbox_R6_file_count: 78
- r5_reports_file_count: 10
- r6_reports_file_count: 6
- imported_from_crypto_signal_os_file_count: 1
