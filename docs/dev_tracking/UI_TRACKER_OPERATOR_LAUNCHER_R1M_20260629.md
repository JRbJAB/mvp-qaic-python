# UI Tracker Operator Launcher R1M - internal tool exposure

Status: `INTERNAL_TOOL_DEPLOYED`

R1M exposes the UI Common Tracker Kit as a standard internal repo tool, not only as docs/tests.

## Operator entrypoints

- Manifest module: `mvp_qaic_reflex_ui/common/tracker_ui_tool_manifest.py`
- Operator launcher CLI: `tools/ui_tracker_operator_launcher.py`
- Existing deploy gate CLI: `tools/ui_tracker_deploy_gate.py`
- Approved visual oracle: `docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html`

## Commands

```powershell
python tools/ui_tracker_operator_launcher.py --out C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY\ui_tracker_operator_launcher.json
python tools/ui_tracker_deploy_gate.py --out C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY\ui_tracker_deploy_gate.json
python -m http.server 3003 --directory docs/dev_tracking/visual_oracle
```

## Deployment rule

The UI Tracker Tool is deployed internally in the repository.
Public Reflex deployment remains blocked until a real Reflex browser runtime visually matches the R1I approved oracle.

```text
REFLEX_PUBLIC_DEPLOY_ALLOWED=False
REFLEX_PUBLIC_DEPLOY_STATUS=BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH
```
