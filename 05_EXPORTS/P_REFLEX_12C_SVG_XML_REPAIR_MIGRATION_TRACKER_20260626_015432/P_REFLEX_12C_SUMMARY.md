# P_REFLEX_12C — SVG XML Repair + Mission Migration Tracker

Status: `OK_P_REFLEX_12C_SVG_XML_REPAIR_MIGRATION_TRACKER`

Fix:

- escaped invalid SVG ampersands
- added XML parse guard for SVG files
- browser rendering error should be removed

Added:

- Mission Control migration tracker
- compact table for Sheets / Apps Script / functions / features
- docs/MIGRATION_TRACKER.json
- docs/MIGRATION_TRACKER.md

Clarification:

- Dev Tracking = development batches, commits, tags, tests, runtime gates.
- CDC Tracker = product requirements, pages, cockpits, % completion.
- Migration Tracker = legacy Sheets / Apps Script / features to migrate into Reflex/Python.

Safety:

- server started by batch: `false`
- public deploy: `false`
- broker/order/sizing: `false`
- Sheet write: `false`
- BigQuery write: `false`

Next:

`P_REFLEX_12D_RUNTIME_VISUAL_SMOKE_AFTER_SVG_REPAIR`
