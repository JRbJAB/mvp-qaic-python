from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "docs" / "FINAL"
MARKER = "R21F_DRIVE_FIRST_REFERENCE_LOCK"
MEMO = FINAL / "R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md"

REQUIRED_KEYS = [
    "DRIVE_LIVE_ACCESS=True",
    "DRIVE_SOURCE_OF_TRUTH_REQUIRED=True",
    "READ_CURRENT_REFERENCE_INDEX_BEFORE_PROJECT_BATCH=True",
    "READ_FINAL_DOCS_BEFORE_PROJECT_BATCH=True",
    "READ_CDC_TOOL_REGISTRY_UI_TRACKER_REFERENCES_BEFORE_PATCH=True",
    "NO_MEMORY_ONLY=True",
    "NO_APPROXIMATION=True",
    "NO_BATCH_WITHOUT_REFERENTIAL_AUDIT=True",
]


def _one_by_suffix(suffix: str) -> Path:
    matches = list(FINAL.glob(f"*{suffix}"))
    assert len(matches) == 1, (suffix, matches)
    return matches[0]


def test_r21f_memo_exists_and_contains_lock() -> None:
    assert MEMO.exists()
    text = MEMO.read_text(encoding="utf-8")
    for key in REQUIRED_KEYS:
        assert key in text


def test_r21f_lock_in_current_index_and_core_final_docs() -> None:
    docs = [
        FINAL / "CURRENT_REFERENCE_INDEX.md",
        _one_by_suffix("REFERENCE_v0.2.7_FINAL_SEAL.md"),
        _one_by_suffix("MVP_QAIC_INSTRUCTIONS_GOVERNANCE_FINAL_FUSED_v0.2.7.md"),
        _one_by_suffix("MVP_QAIC_NOTICE_RUNBOOK_FINAL_FUSED_v0.2.7.md"),
        _one_by_suffix("MVP_QAIC_REFLEX_RUNTIME_PROCESS_LIVE_v0.2.8.md"),
        _one_by_suffix("MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md"),
        _one_by_suffix("MVP_QAIC_WEB_ARCHITECTURE_UI_PROCESS_FINAL_FUSED_v0.2.6.md"),
        _one_by_suffix("MVP_QAIC_PROMPT_GEM_WORKFLOW_FINAL_FUSED_v0.2.6.md"),
        _one_by_suffix("MVP_QAIC_LEXIQUE_REFERENCE_FINAL_FUSED_v0.2.6.md"),
    ]
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        assert MARKER in text, doc
        assert "READ_CDC_TOOL_REGISTRY_UI_TRACKER_REFERENCES_BEFORE_PATCH=True" in text, doc


def test_r21f_manifest_references_memo() -> None:
    manifest = FINAL / "REFERENCE_SOURCES_MANIFEST_v0.2.7.csv"
    text = manifest.read_text(encoding="utf-8")
    assert "R21F_DRIVE_FIRST_REFERENCE_LOCK" in text
    assert "R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md" in text
