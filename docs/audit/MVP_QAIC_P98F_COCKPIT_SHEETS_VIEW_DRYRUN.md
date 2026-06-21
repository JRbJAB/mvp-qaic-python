# MVP QAIC - P98F Cockpit Sheets View Dryrun

Status: `OK_P98F_COCKPIT_SHEETS_VIEW_DRYRUN_READY`

Scope:
- plan how the P98E-R1 local cockpit UI export would map to a Google Sheets cockpit view
- target view name: `QAIC_RUNTIME_COCKPIT_VIEW`
- dry-run only: no Sheet creation, no cell update, no live write
- no Decision Journal write in P98F
- no Apps Script execution
- no CLASP push
- no broker/order/sizing

Planned cockpit rows:
- 17 cockpit cards from P98D/P98E-R1
- journal workflow cards
- benchmark / quality cards
- lexique / methods / signals / risk cards
- portfolio / Revolut read-only cards

Next:
- `P98G_CREATE_OR_UPDATE_COCKPIT_SHEET_AFTER_EXPLICIT_GO_OR_P99_MVP_FREEZE`
