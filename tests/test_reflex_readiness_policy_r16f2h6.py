from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "reflex_runtime_policy.json"


def _policy() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def test_readiness_policy_locked() -> None:
    readiness = _policy()["readiness"]
    assert readiness["policy_id"] == "R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY"
    assert readiness["max_wait_seconds"] >= 420
    assert readiness["max_identical_log_tail_repeats"] == 2


def test_readiness_policy_forbids_infinite_log_tail_loop() -> None:
    readiness = _policy()["readiness"]
    forbidden = set(readiness["forbidden_runner_behavior"])
    assert "unbounded_log_tail_loop" in forbidden
    assert "printing_identical_log_tail_more_than_two_times" in forbidden
    assert "dynamic_port_fallback" in forbidden


def test_readiness_policy_requires_port_diagnostics_and_stop_on_failure() -> None:
    readiness = _policy()["readiness"]
    diagnostics = set(readiness["if_compile_done_but_http_not_ready"])
    assert "inspect_internal_listening_ports_3000_8000" in diagnostics
    assert "test_host_http_3055_8055" in diagnostics
    assert "stop_container_on_failure" in diagnostics


def test_readiness_policy_guard_script() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "reflex_readiness_policy_guard.py")],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "REFLEX_READINESS_POLICY_GUARD_OK=True" in proc.stdout
