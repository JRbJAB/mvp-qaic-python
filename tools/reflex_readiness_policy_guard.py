from __future__ import annotations

import json
from pathlib import Path

POLICY_PATH = Path(__file__).resolve().parents[1] / "config" / "reflex_runtime_policy.json"


def main() -> int:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    readiness = policy.get("readiness", {})
    errors: list[str] = []
    if policy.get("policy_id") != "R16F2H4_REFLEX_RUNTIME_POLICY_LOCK":
        errors.append("POLICY_ID_MISMATCH")
    if readiness.get("policy_id") != "R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY":
        errors.append("READINESS_POLICY_ID_MISSING")
    if readiness.get("max_wait_seconds", 0) < 420:
        errors.append("MAX_WAIT_SECONDS_TOO_LOW")
    if readiness.get("max_identical_log_tail_repeats") != 2:
        errors.append("MAX_IDENTICAL_LOG_TAIL_REPEATS_NOT_LOCKED_TO_2")
    forbidden = set(readiness.get("forbidden_runner_behavior", []))
    for item in ["unbounded_log_tail_loop", "printing_identical_log_tail_more_than_two_times", "dynamic_port_fallback"]:
        if item not in forbidden:
            errors.append(f"FORBIDDEN_BEHAVIOR_MISSING:{item}")
    markers = set(readiness.get("required_log_markers", []))
    for item in ["App Running", "App running at:", "Backend running at:"]:
        if item not in markers:
            errors.append(f"REQUIRED_MARKER_MISSING:{item}")
    diagnostics = set(readiness.get("if_compile_done_but_http_not_ready", []))
    for item in ["inspect_internal_listening_ports_3000_8000", "test_host_http_3055_8055", "stop_container_on_failure"]:
        if item not in diagnostics:
            errors.append(f"DIAGNOSTIC_MISSING:{item}")
    if errors:
        print("REFLEX_READINESS_POLICY_GUARD_OK=False")
        for err in errors:
            print(f"ERROR={err}")
        return 1
    print("REFLEX_READINESS_POLICY_GUARD_OK=True")
    print("READINESS_POLICY_ID=R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY")
    print("MAX_WAIT_SECONDS=420")
    print("MAX_IDENTICAL_LOG_TAIL_REPEATS=2")
    print("APP_RUNNING_MARKER_REQUIRED=True")
    print("INTERNAL_PORT_DIAGNOSTIC_REQUIRED=True")
    print("STOP_CONTAINER_ON_FAILURE=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
