# UI Tracker Tool Deployment â€” R1K

Status: internal tool deployment gate ready.

This document separates three layers that were previously mixed during runtime smoke work:

1. **UI Common Tracker Tool**: reusable renderer, render-type registry, visual contract, CLI/static preview support.
2. **Approved Visual Oracle**: `docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html`, locked by R1I.
3. **Reflex Public Deployment**: still blocked until a real Reflex browser runtime page visually matches the approved oracle.

## R1K decision

The UI Tracker Tool is considered deployed internally when:

- the approved oracle exists;
- required tokens are present: CDC Tracker, Dev Tracker, `/dev-tracking`, `/cdc-dev-tracker`, `/cdc-tracker`, percent/progress semantics;
- the blue/progress visual language is preserved;
- operator gates can produce a machine-readable deployment status.

## R1K non-goals

- No public Reflex deploy.
- No Bun loop.
- No browser claim without visual match.
- No generic shim accepted as release evidence.

## Operator command

```powershell
python tools/ui_tracker_deploy_gate.py --out C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY\ui_tracker_deploy_gate.json
```
