from pathlib import Path


BEGIN = "<!-- BEGIN_REFLEX_H8I_HARD_PROCESS_LOCK -->"
END = "<!-- END_REFLEX_H8I_HARD_PROCESS_LOCK -->"
AUTHORIZED_COMMAND = (
    "python -m reflex run --env dev --backend-host 0.0.0.0 "
    "--backend-port 8000 --frontend-port 3000"
)

VERSIONED_FINAL_DOCS = {
    Path("docs/FINAL/🛠️ MVP_QAIC_REFLEX_RUNTIME_PROCESS_LIVE_v0.2.7.md"): Path(
        "docs/FINAL/🛠️ MVP_QAIC_REFLEX_RUNTIME_PROCESS_LIVE_v0.2.8.md"
    ),
    Path("docs/FINAL/🧭 MVP_QAIC_INSTRUCTIONS_GOVERNANCE_FINAL_FUSED_v0.2.6.md"): Path(
        "docs/FINAL/🧭 MVP_QAIC_INSTRUCTIONS_GOVERNANCE_FINAL_FUSED_v0.2.7.md"
    ),
    Path("docs/FINAL/🚀 MVP_QAIC_NOTICE_RUNBOOK_FINAL_FUSED_v0.2.6.md"): Path(
        "docs/FINAL/🚀 MVP_QAIC_NOTICE_RUNBOOK_FINAL_FUSED_v0.2.7.md"
    ),
    Path("docs/FINAL/✅ REFERENCE_v0.2.6_FINAL_SEAL.md"): Path(
        "docs/FINAL/✅ REFERENCE_v0.2.7_FINAL_SEAL.md"
    ),
}

MANDATORY_DOCS = [
    *VERSIONED_FINAL_DOCS.values(),
    Path("docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md"),
]

REQUIRED_TOKENS = [
    "REFLEX H8I HARD PROCESS LOCK",
    "Reflex 0.9.6.post1",
    "jrb-reflex-pinned-hub:py312-node22-reflex096p1",
    "--frontend-host",
    "Forbidden flag because it is absent from the real help",
    AUTHORIZED_COMMAND,
    "127.0.0.1:3055:3000",
    "127.0.0.1:8055:8000",
    "REFLEX_CLI_HELP_CAPTURE_REQUIRED=True",
    "NO_FRONTEND_HOST_FLAG=True",
    "STOP_AND_AUDIT_READONLY",
    "NO_HELP = NO_RUNTIME",
    "HELP_FLAG_MISSING = COMMAND_FORBIDDEN",
    "TCP_ONLY = NOT_PREVIEW_READY",
    "HTTP_FAIL = STOP_AND_DIAG",
    "SOURCE_REPO_DIRTY_AFTER_RUNTIME = RUNTIME_INVALID",
    "PREVIEW_ONLY_AFTER_HTTP_PASS = TRUE",
]

GUARD_FILES = [
    Path("config/reflex_runtime_policy.json"),
    Path("tools/reflex_runtime_policy_guard.py"),
    Path("tools/reflex_readiness_policy_guard.py"),
    Path("tools/reflex_runner_hardening_policy_guard.py"),
    Path("tests/test_reflex_runtime_policy_r16f2h4.py"),
    Path("tests/test_reflex_readiness_policy_r16f2h6.py"),
    Path("tests/test_reflex_runner_hardening_policy_r16f2h7i.py"),
]

CURRENT_INDEX = Path("docs/FINAL/CURRENT_REFERENCE_INDEX.md")
CURRENT_MANIFEST = Path("docs/FINAL/REFERENCE_SOURCES_MANIFEST_v0.2.7.csv")


def _lock_block(text: str) -> str:
    assert text.count(BEGIN) == 1
    assert text.count(END) == 1
    start = text.index(BEGIN)
    end = text.index(END) + len(END)
    assert start < end
    return text[start:end]


def test_new_versioned_final_docs_exist_and_old_final_docs_remain_present():
    for old_path, new_path in VERSIONED_FINAL_DOCS.items():
        assert old_path.exists(), f"Old final doc must remain present: {old_path}"
        assert new_path.exists(), f"Missing new versioned final doc: {new_path}"


def test_h8i_contract_docs_contain_single_complete_lock_block():
    for path in MANDATORY_DOCS:
        assert path.exists(), f"Missing mandatory H8I contract doc: {path}"
        block = _lock_block(path.read_text(encoding="utf-8"))
        for token in REQUIRED_TOKENS:
            assert token in block, f"{path} missing required token: {token}"


def test_frontend_host_is_forbidden_and_not_in_authorized_command():
    assert "--frontend-host" not in AUTHORIZED_COMMAND
    for path in MANDATORY_DOCS:
        block = _lock_block(path.read_text(encoding="utf-8"))
        assert block.count(AUTHORIZED_COMMAND) == 1
        for line in block.splitlines():
            if "--frontend-host" in line:
                lowered = line.lower()
                assert any(
                    term in lowered
                    for term in ("forbidden", "absent", "never", "not appear")
                ), f"{path} has non-forbidden --frontend-host context: {line}"


def test_current_index_and_manifest_reference_new_versioned_docs():
    index_text = CURRENT_INDEX.read_text(encoding="utf-8")
    manifest_text = CURRENT_MANIFEST.read_text(encoding="utf-8")

    for new_path in VERSIONED_FINAL_DOCS.values():
        assert new_path.name in index_text

    assert "REFERENCE_SOURCES_MANIFEST_v0.2.7.csv" in index_text
    assert "MVP QAIC Instructions Governance Final Fused v0.2.7" in manifest_text
    assert "MVP QAIC Notice Runbook Final Fused v0.2.7" in manifest_text
    assert "REFERENCE_v0.2.7_FINAL_SEAL.md" in manifest_text


def test_prior_reflex_guard_files_still_exist():
    for path in GUARD_FILES:
        assert path.exists(), f"Missing required guard file/test: {path}"
