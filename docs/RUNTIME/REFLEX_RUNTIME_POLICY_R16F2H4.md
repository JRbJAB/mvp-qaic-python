# R16F2H4 - Reflex Runtime Policy Lock

Policy ID: R16F2H4_REFLEX_RUNTIME_POLICY_LOCK

## Locked decision

Authorized MVP QAIC Reflex UI preview:

python -m reflex run --env dev --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000

Docker preview mapping:
host 3055 -> container 3000
host 8055 -> container 8000

Docker reference mapping:
host 3035 -> container 3000
host 8035 -> container 8000

## Forbidden for primary UI preview

Forbidden: --env prod, --single-port, reflex export as primary preview, minimal allowlist runtime copy, silent dynamic port fallback, patching the real repo before preview, commit/tag/push before DOM + PNG + human validation, NiceGUI, .web source patch.

## Required gate

Every future Reflex runner must execute:
python tools\reflex_runtime_policy_guard.py --repo C:\JRb_TRADING_OS\MVP_QAIC_PY

and display:
REFLEX_POLICY_GUARD_OK=True
POLICY_ID=R16F2H4_REFLEX_RUNTIME_POLICY_LOCK
REFLEX_POLICY_GUARD_REQUIRED=True

## Official Reflex docs binding

The assistant must check official Reflex CLI/config docs before proposing any new Reflex command or config change.

Locked preview strategy:
Docker pinned + full tracked HEAD copy outside repo + Reflex dev mode + container frontend/backend 3000/8000 + host preview ports 3055/8055 + no real repo patch before visual validation.
<!-- BEGIN_REFLEX_H8I_HARD_PROCESS_LOCK -->
## REFLEX H8I HARD PROCESS LOCK

- Pinned image: `jrb-reflex-pinned-hub:py312-node22-reflex096p1`.
- Pinned Reflex version: `Reflex 0.9.6.post1`.
- Never propose, modify, or launch Reflex commands from memory.
- The real `python -m reflex run --help` output from the pinned image is the only source of truth for CLI flags.
- Authorized command shape: `python -m reflex run --env dev --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000`.
- Forbidden flag because it is absent from the real help: `--frontend-host`.
- `--frontend-host` is forbidden and must never appear in an allowed command.
- Required local preview port mappings: `127.0.0.1:3055:3000` and `127.0.0.1:8055:8000`.
- Runtime remains forbidden unless explicitly approved by operator.
- Manual preview URL only after HTTP smoke pass: `http://127.0.0.1:3055/`.
- TCP-only port checks are not success.
- Use temporary runtime copy outside source repo: `C:\JRb_TRADING_OS\_RUNTIME_TMP\`.
- Store evidence under: `C:\JRb_TRADING_OS\_RUN_REPORTS\`.
- No browser open, no public deploy, no provider call, no broker/order/sizing, no Sheet/BQ write, no Apps Script execution, no clasp push.
- After any Reflex failure: stop runtime, capture logs, capture docker inspect, capture command used, capture Reflex version, capture Reflex run help, capture repo status, and do not relaunch.

Required guard constants:

```text
REFLEX_CLI_HELP_CAPTURE_REQUIRED=True
NO_FRONTEND_HOST_FLAG=True
STOP_AND_AUDIT_READONLY
NO_HELP = NO_RUNTIME
HELP_FLAG_MISSING = COMMAND_FORBIDDEN
TCP_ONLY = NOT_PREVIEW_READY
HTTP_FAIL = STOP_AND_DIAG
SOURCE_REPO_DIRTY_AFTER_RUNTIME = RUNTIME_INVALID
PREVIEW_ONLY_AFTER_HTTP_PASS = TRUE
```
<!-- END_REFLEX_H8I_HARD_PROCESS_LOCK -->
