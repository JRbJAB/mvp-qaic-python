# MVP UI — CDC + Dev Tracker Screen Migration Style R2D

## Status

`OK_MVP_QAIC_UI_CDC_DEV_TRACKER_SCREEN_MIGRATION_STYLE_R2D_READY_FOR_COMMIT`

## Purpose

Wire a runtime-free CDC + Dev Tracker screen model using the same layout contract as the existing Migration Tracker style.

## R2D fix

R2C imported a non-existing helper from R1G. R2D adapts `default_tracker_rows()` locally and converts tracker rows to dictionaries without modifying the R1G contract.

## UI contract

- Summary KPI bar
- Filter bar
- CDC tracker table
- Dev tracker table
- Detail panel
- Next actions panel

## Safety

- No runtime start
- No archive bundle
- No broker/order/sizing
- No Sheet/BQ write
- Uses QAIT handoff guard status: `FULLY_APPROVED_AND_GITIGNORE_RESOLVED`

## Next

`MVP_UI_ATTACH_CDC_DEV_TRACKER_TO_NAVIGATION_R3`
