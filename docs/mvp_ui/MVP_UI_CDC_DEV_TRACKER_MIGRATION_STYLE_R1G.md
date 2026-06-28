# MVP UI CDC + Dev Tracker Migration Style R1G

## Status

R1G reapplies the CDC + Dev Tracker contract with the same UI shape as the Migration Tracker.

## Scope

- CDC tracker view model
- Dev tracker view model
- Migration Tracker style contract
- Summary KPI bar contract
- Filter bar contract
- Table columns contract
- Detail panel contract
- Next actions panel contract

## Safety

```text
NO_RUNTIME=True
NO_ARCHIVE=True
NO_BROKER_ORDER=True
NO_SIZING=True
NO_SHEET_WRITE=True
NO_BQ_WRITE=True
TARGETED_COMMIT_ONLY=True
```

## UI contract

```text
UI_STYLE_SOURCE=MIGRATION_TRACKER
SAME_COLUMNS=True
SUMMARY_KPI_BAR=True
FILTER_BAR=True
TRACKER_TABLE=True
DETAIL_PANEL=True
NEXT_ACTIONS_PANEL=True
```

## Next

```text
MVP_UI_WIRE_CDC_DEV_TRACKER_SCREEN_MIGRATION_STYLE_R2
```
