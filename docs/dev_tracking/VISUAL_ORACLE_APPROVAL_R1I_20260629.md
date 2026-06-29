# MVP QAIC R1I - Approved Tracker Visual Oracle

Status: APPROVED_TRACKER_VISUAL_ORACLE_LOCKED

Approved preview source:
$approved

Approved oracle file:
$oracleFile

Rules:
- This approved visual oracle is the single reference for CDC Tracker and Dev Tracker preview rendering.
- Generic runtime shims are not release evidence.
- HTTP 200 without browser-visible content is not enough.
- Reflex deployment remains blocked until browser/runtime visual proof matches this oracle.
- Any future tracker UI change must update this oracle or fail visual gate tests.

Required visual semantics:
- CDC Tracker and Dev Tracker must both be visible.
- Routes /dev-tracking, /cdc-dev-tracker and /cdc-tracker must be represented.
- Progress percentages and blue progress bars must be visible.
- Browser/runtime gate must remain explicit until real Reflex runtime proof exists.
