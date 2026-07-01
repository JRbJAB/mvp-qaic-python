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
        "no_commit_tag_push_after_failed_tests_required": (
            rules.get("no_commit_tag_push_after_failed_tests_required") is True
        ),
        "runner_pack_self_test_required": rules.get("runner_pack_self_test_required") is True,
        "zip_payload_paths_emoji_free_required": rules.get("zip_payload_paths_emoji_free_required") is True,
        "inline_long_powershell_patch_forbidden": rules.get("inline_long_powershell_patch_forbidden") is True,
        "codex_required_after_two_repeated_workstream_failures": (
            rules.get("codex_required_after_two_repeated_workstream_failures") is True
        ),
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
    print(
        "NO_COMMIT_TAG_PUSH_AFTER_FAILED_TESTS_REQUIRED="
        f"{rules.get('no_commit_tag_push_after_failed_tests_required') is True}"
    )
    print(f"RUNNER_PACK_SELF_TEST_REQUIRED={rules.get('runner_pack_self_test_required') is True}")
    print(f"ZIP_PAYLOAD_PATHS_EMOJI_FREE_REQUIRED={rules.get('zip_payload_paths_emoji_free_required') is True}")
    print(f"INLINE_LONG_POWERSHELL_PATCH_FORBIDDEN={rules.get('inline_long_powershell_patch_forbidden') is True}")
    print(
        "CODEX_REQUIRED_AFTER_TWO_REPEATED_WORKSTREAM_FAILURES="
        f"{rules.get('codex_required_after_two_repeated_workstream_failures') is True}"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
