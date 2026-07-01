from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
POLICY_ID = "R16F2H7I_REFLEX_RUNNER_HARDENING_PROCESS_LOCK"
RULE_SUBSTRINGS = [
    "timeout dur sur chaque sous-commande native",
    "docker run sans image preflight",
    "docker run sans port preflight",
    "docker exec si container non running",
    "Copy-Item fichier par fichier",
    "ZIP sans self-check de structure",
    "rapport transitoire dans docs/",
    "commit/tag/push apres tests echoues",
    "runner pack sans self-test",
    "chemin payload ZIP avec emoji",
    "patch PowerShell inline long",
    "Codex requis apres deux echecs repetes sur le meme workstream",
]
PROCESS_RULES = {
    "no_commit_tag_push_after_failed_tests_required": "NO_COMMIT_TAG_PUSH_AFTER_FAILED_TESTS_REQUIRED=True",
    "runner_pack_self_test_required": "RUNNER_PACK_SELF_TEST_REQUIRED=True",
    "zip_payload_paths_emoji_free_required": "ZIP_PAYLOAD_PATHS_EMOJI_FREE_REQUIRED=True",
    "inline_long_powershell_patch_forbidden": "INLINE_LONG_POWERSHELL_PATCH_FORBIDDEN=True",
    "codex_required_after_two_repeated_workstream_failures": (
        "CODEX_REQUIRED_AFTER_TWO_REPEATED_WORKSTREAM_FAILURES=True"
    ),
}


def test_runner_hardening_policy_config_locked() -> None:
    data = json.loads((REPO / "config" / "reflex_runtime_policy.json").read_text(encoding="utf-8"))
    hardening = data["runner_hardening_policy"]
    rules = hardening["rules"]
    assert hardening["policy_id"] == POLICY_ID
    assert hardening["full_head_copy_method"] == "git_archive_head_tar_extract"
    assert rules["native_subcommand_timeout_required"] is True
    assert rules["docker_image_preflight_required"] is True
    assert rules["docker_port_preflight_required"] is True
    assert rules["docker_exec_running_container_required"] is True
    assert rules["full_head_copy_git_archive_required"] is True
    assert rules["zip_structure_self_check_required"] is True
    assert rules["transient_reports_forbidden_under_docs"] is True
    for rule in PROCESS_RULES:
        assert rules[rule] is True


def test_runner_hardening_guard_outputs_required_lines() -> None:
    proc = subprocess.run(
        [sys.executable, "tools/reflex_runner_hardening_policy_guard.py"],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=20,
        check=True,
    )
    out = proc.stdout
    assert "REFLEX_RUNNER_HARDENING_POLICY_GUARD_OK=True" in out
    assert "NATIVE_TIMEOUT_REQUIRED=True" in out
    assert "DOCKER_IMAGE_PREFLIGHT_REQUIRED=True" in out
    assert "DOCKER_PORT_PREFLIGHT_REQUIRED=True" in out
    assert "DOCKER_EXEC_RUNNING_REQUIRED=True" in out
    assert "FULL_HEAD_COPY_METHOD=git_archive_head_tar_extract" in out
    assert "ZIP_STRUCTURE_SELF_CHECK_REQUIRED=True" in out
    assert "TRANSIENT_REPORTS_FORBIDDEN_UNDER_DOCS=True" in out
    for guard_line in PROCESS_RULES.values():
        assert guard_line in out


def test_reference_and_live_docs_contain_all_operator_rules() -> None:
    docs = [
        REPO / "docs/RUNTIME/REFLEX_RUNNER_HARDENING_POLICY_R16F2H7I.md",
        REPO / "docs/FINAL/🧱 MVP_QAIC_RUNNER_HARDENING_PROCESS_LIVE_v0.2.8.md",
        REPO / "docs/FINAL/✅ REFERENCE_v0.2.6_FINAL_SEAL.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in docs)
    for snippet in RULE_SUBSTRINGS:
        assert snippet in text


def test_final_docs_have_fusion_marker() -> None:
    final_docs = [
        "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
        "docs/RUNTIME/REFLEX_TECH_PROCESS_LOCK_R16F2H6.md",
        "docs/FINAL/🛠️ MVP_QAIC_REFLEX_RUNTIME_PROCESS_LIVE_v0.2.7.md",
        "docs/FINAL/🧭 MVP_QAIC_INSTRUCTIONS_GOVERNANCE_FINAL_FUSED_v0.2.6.md",
        "docs/FINAL/🌐 MVP_QAIC_WEB_ARCHITECTURE_UI_PROCESS_FINAL_FUSED_v0.2.6.md",
        "docs/FINAL/🚀 MVP_QAIC_NOTICE_RUNBOOK_FINAL_FUSED_v0.2.6.md",
        "docs/FINAL/✅ REFERENCE_v0.2.6_FINAL_SEAL.md",
    ]
    for rel in final_docs:
        text = (REPO / rel).read_text(encoding="utf-8")
        assert "R16F2H7I_RUNNER_HARDENING_START" in text
        assert "R16F2H7I_RUNNER_HARDENING_END" in text
        assert POLICY_ID in text
