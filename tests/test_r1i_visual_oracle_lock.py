from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs" / "dev_tracking" / "visual_oracle" / "APPROVED_TRACKER_PREVIEW.html"
DOC = ROOT / "docs" / "dev_tracking" / "VISUAL_ORACLE_APPROVAL_R1I_20260629.md"


def test_approved_visual_oracle_exists_and_has_tracker_semantics() -> None:
    assert ORACLE.exists(), "Approved visual oracle must exist"
    html = ORACLE.read_text(encoding="utf-8")
    required = [
        "CDC Tracker",
        "Dev Tracker",
        "/dev-tracking",
        "/cdc-dev-tracker",
        "/cdc-tracker",
        "%",
    ]
    for token in required:
        assert token in html
    assert any(
        token in html for token in ("#2563eb", "#1d4ed8", "#3b82f6", "blue", "progress", "accent")
    )


def test_approved_visual_oracle_is_not_runtime_shim_placeholder() -> None:
    html = ORACLE.read_text(encoding="utf-8")
    forbidden = [
        "rendu visible local npm",
        "MVP QAIC Runtime Preview",
        "Runtime Preview",
    ]
    for token in forbidden:
        assert token not in html


def test_r1i_visual_oracle_approval_doc_locks_deploy_gate() -> None:
    assert DOC.exists(), "R1I visual oracle approval doc must exist"
    text = DOC.read_text(encoding="utf-8")
    assert "APPROVED_TRACKER_VISUAL_ORACLE_LOCKED" in text
    assert "Reflex deployment remains blocked" in text
    assert "browser/runtime visual proof" in text
