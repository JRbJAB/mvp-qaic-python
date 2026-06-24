# P174 NiceGUI Private Local Launch Operator Smoke

- STATUS: OK_P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE
- host: 127.0.0.1
- port: 8088
- route_count: 3
- route_success_count: 3
- smoke_ok: True
- server_started_by_smoke: True
- server_stopped_after_smoke: True
- blocker_count: 0

Safety:
- PUBLIC_SERVE=False
- GOOGLE_SHEETS_WRITE=False
- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False
- APPS_SCRIPT_EXECUTION=False
- CLASP_PUSH=False
- BROKER=False
- ORDER=False
- SIZING=False

Next:
- P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH
