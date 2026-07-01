from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "docs" / "FINAL"
MEMO = FINAL / "R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md"
REQUIRED_TOKENS = [
    "REFLEX_RUNTIME_STATUS=PAUSED",
    "REFLEX_RUNTIME_RUNNER_CHAIN=STOPPED",
    "H9H_H9I_H9K_CHAIN=CLOSED_FAILED_NO_COMMIT_ROLLBACK_DONE",
    "STOP_DEV_PREVIEW_RETRY_AFTER_HTTP_BODY_ZERO=True",
    "STOP_CODEX_RUNTIME_RUNNER_GENERATION_UNTIL_RUNNER_AUDITED=True",
    "NO_MICRO_FIX_LOOP=True",
    "ONE_BATCH_ONE_DECISION=True",
    "NO_DOCKER_RM_ON_FAILURE=True",
    "PS51_RUNNER_REVIEW_REQUIRED_BEFORE_EXECUTION=True",
    "NO_COMMIT_BEFORE_HTTP_PREVIEW_OK=True",
    "FALLBACK_STATIC_WYSIWYG_ALLOWED=True",
    "REFLEX_ALLOWED_NEXT_ONLY_AFTER_HUMAN_RUNNER_REVIEW=True",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _one_by_suffix(suffix: str) -> Path:
    hits = [p for p in FINAL.glob(f"*{suffix}") if "99_SUPERSEDED" not in str(p)]
    assert hits, suffix
    return hits[0]


def test_r21b_memo_exists_and_contains_policy_tokens() -> None:
    text = _read(MEMO)
    for token in REQUIRED_TOKENS:
        assert token in text


def test_r21b_final_docs_reference_memo_and_policy_marker() -> None:
    targets = [
        FINAL / "CURRENT_REFERENCE_INDEX.md",
        _one_by_suffix("REFERENCE_v0.2.7_FINAL_SEAL.md"),
        _one_by_suffix("MVP_QAIC_INSTRUCTIONS_GOVERNANCE_FINAL_FUSED_v0.2.7.md"),
        _one_by_suffix("MVP_QAIC_NOTICE_RUNBOOK_FINAL_FUSED_v0.2.7.md"),
        _one_by_suffix("MVP_QAIC_REFLEX_RUNTIME_PROCESS_LIVE_v0.2.8.md"),
    ]
    for path in targets:
        text = _read(path)
        assert "R21B_REFLEX_RUNTIME_CLOSURE" in text
        assert "REFLEX_RUNTIME_STATUS=PAUSED" in text
        assert "R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md" in text


def test_r21b_manifest_references_memo() -> None:
    manifest = _read(FINAL / "REFERENCE_SOURCES_MANIFEST_v0.2.7.csv")
    assert "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md" in manifest
