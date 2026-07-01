# REFLEX CLI CONTRACT H8I

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
