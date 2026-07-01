from __future__ import annotations

import json
from pathlib import Path

POLICY_ID = "R16F2H7I_REFLEX_RUNNER_HARDENING_PROCESS_LOCK"


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    config_path = repo / "config" / "reflex_runtime_policy.json"
    data = json.loads(config_path.read_text(encoding="utf-8"))
    hardening = data.get("runner_hardening_policy", {})
    rules = hardening.get("rules", {})

    checks = {
        "policy_id": hardening.get("policy_id") == POLICY_ID,
        "native_subcommand_timeout_required": rules.get("native_subcommand_timeout_required") is True,
        "docker_image_preflight_required": rules.get("docker_image_preflight_required") is True,
        "docker_port_preflight_required": rules.get("docker_port_preflight_required") is True,
        "docker_exec_running_container_required": rules.get("docker_exec_running_container_required") is True,
        "full_head_copy_git_archive_required": rules.get("full_head_copy_git_archive_required") is True,
        "zip_structure_self_check_required": rules.get("zip_structure_self_check_required") is True,
        "transient_reports_forbidden_under_docs": rules.get("transient_reports_forbidden_under_docs") is True,
    }
    ok = all(checks.values())
    print(f"REFLEX_RUNNER_HARDENING_POLICY_GUARD_OK={ok}")
    print(f"RUNNER_HARDENING_POLICY_ID={hardening.get('policy_id', '')}")
    print(f"NATIVE_TIMEOUT_REQUIRED={rules.get('native_subcommand_timeout_required') is True}")
    print(f"DOCKER_IMAGE_PREFLIGHT_REQUIRED={rules.get('docker_image_preflight_required') is True}")
    print(f"DOCKER_PORT_PREFLIGHT_REQUIRED={rules.get('docker_port_preflight_required') is True}")
    print(f"DOCKER_EXEC_RUNNING_REQUIRED={rules.get('docker_exec_running_container_required') is True}")
    print(f"FULL_HEAD_COPY_METHOD={hardening.get('full_head_copy_method', '')}")
    print(f"ZIP_STRUCTURE_SELF_CHECK_REQUIRED={rules.get('zip_structure_self_check_required') is True}")
    print(f"TRANSIENT_REPORTS_FORBIDDEN_UNDER_DOCS={rules.get('transient_reports_forbidden_under_docs') is True}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
