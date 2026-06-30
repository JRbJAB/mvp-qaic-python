# R13B — Clean tracked desktop.ini noise

Status target: `OK_MVP_QAIC_R13B_CLEAN_R13_REPORT_DESKTOP_INI_NOISE_COMMITTED_TAGGED_PUSHED`

Scope:
- Remove only `docs/drive_reconcile/R13_REPORTS/desktop.ini` from git tracking.
- Preserve an evidence byte copy in this report folder before removal.
- No Drive write, no reset, no delete outside the targeted tracked Windows metadata file.
- No `git add .`.

Why:
R13 was functionally sealed, but it accidentally staged `docs/drive_reconcile/R13_REPORTS/desktop.ini` as Windows Explorer metadata noise. This R13B cleanup removes that tracked noise and keeps a trace.
