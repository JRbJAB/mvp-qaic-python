# R16F2H6 - Reflex Readiness Anti-Loop Policy

Policy ID: R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY

This policy amends R16F2H4. It does not change the Reflex command or ports.

Locked command remains:
python -m reflex run --env dev --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000

Locked Docker preview mapping remains:
host 3055 -> container 3000
host 8055 -> container 8000

## Anti-loop rules

Future runners must not print identical LOG_TAIL blocks more than two times.
Future runners must stop waiting after max_wait_seconds=420.
Future runners must treat App Running / App running at / Backend running at as phase markers.
If compile is complete but HTTP is not ready, future runners must inspect internal ports 3000/8000, test host ports 3055/8055, write one diagnostic report, stop the container, and fail clearly.

## Required future runner lines

REFLEX_POLICY_GUARD_OK=True
REFLEX_READINESS_POLICY_GUARD_OK=True
MAX_IDENTICAL_LOG_TAIL_REPEATS=2
APP_RUNNING_MARKER_REQUIRED=True
INTERNAL_PORT_DIAGNOSTIC_REQUIRED=True
STOP_CONTAINER_ON_FAILURE=True
