# P12G — Migration Decision Review Workbench

Status target: `OK_P_REFLEX_12G_MIGRATION_DECISION_REVIEW_WORKBENCH_COMMITTED_TAGGED`

## Purpose

Add a stable migration decision workflow without editing `migration_tracker.py` directly.

## Contract

- Decisions are written to `docs/MIGRATION_DECISION_OVERLAY.json`.
- `scripts/REFRESH_MIGRATION_OS.ps1` merges the overlay into `docs/MIGRATION_OS_LIVE_PAYLOAD.json`.
- `mvp_qaic_reflex_ui/migration_tracker.py` remains UI/render only.
- `scripts/ASSERT_NO_TRACKER_DIRECT_EDIT.ps1` remains the guard against direct tracker edits.
- `scripts/APPLY_MIGRATION_DECISION.ps1` applies one operator-reviewed decision and refreshes the live payload.
- `scripts/EXPORT_MIGRATION_DECISION_QUEUE.ps1` exports a decision queue to `docs/MIGRATION_DECISION_QUEUE.json`.

## Example

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\APPLY_MIGRATION_DECISION.ps1 `
  -RepoRoot $repo `
  -Source "Prompt Cockpit" `
  -DecisionStatus "MIGRATE_NOW" `
  -Target "PYTHON + REFLEX_UI" `
  -Note "operator reviewed"
```

## Safety

- No public deploy.
- No live action.
- No broker/order/sizing.
- No Sheet or BigQuery write.
- Human review only.
