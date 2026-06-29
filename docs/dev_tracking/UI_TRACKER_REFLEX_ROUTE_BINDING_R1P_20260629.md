# R1P — UI Tracker Reflex Route Binding Gate

Status: `MVP_R1P_REFLEX_ROUTE_BINDING_READY`

## Scope

R1P binds the UI Common Tracker Kit to the approved internal route contract:

- `/dev-tracking`
- `/cdc-dev-tracker`
- `/cdc-tracker`

The route contract is tied to the approved visual oracle:

- `docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html`

## Deployment rule

Public Reflex deploy remains blocked until a real Reflex browser runtime surface matches the approved visual oracle.

```text
REFLEX_PUBLIC_DEPLOY_ALLOWED=False
REFLEX_PUBLIC_DEPLOY_STATUS=BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH
```

## Operator gate

```powershell
python tools/ui_tracker_route_binding_gate.py --out <report>\ui_tracker_route_binding_gate.json --repo <repo>
```

## Next

R1Q is the final deploy-readiness synthesis gate.
