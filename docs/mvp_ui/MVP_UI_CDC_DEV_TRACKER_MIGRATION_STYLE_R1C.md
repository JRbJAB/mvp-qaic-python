# MVP UI CDC + Dev Tracker - Migration Tracker Style R1C

## Purpose

Create the MVP UI source contract for a CDC Tracker and a Dev Tracker using the
same layout shape as the existing Migration Tracker.

## Priority

The operator priority is CDC + Dev Tracker UI, not the portfolio packet flow.
The portfolio packet work is deferred until this screen contract is in place.

## UI contract

```text
UI_STYLE_SOURCE=MIGRATION_TRACKER
SAME_COLUMNS=True
SUMMARY_KPI_BAR=True
FILTER_BAR=True
TRACKER_TABLE=True
DETAIL_PANEL=True
NEXT_ACTIONS_PANEL=True
OPERATOR_REVIEW_REQUIRED=True
```

## Safety

```text
NO_RUNTIME=True
NO_ARCHIVE=True
NO_BROKER_ORDER=True
NO_SIZING=True
NO_SHEET_WRITE=True
NO_BQ_WRITE=True
LOCAL_ONLY=True
```

## Source of truth

The MVP UI must consume the sealed QAIT handoff files and must not recreate a
parallel contract.
