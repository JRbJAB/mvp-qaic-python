from pathlib import Path

from mvp_qaic_py.p213_response_draft_private_cockpit_wiring import (
    build_response_draft_private_cockpit_panel,
    build_response_draft_private_cockpit_sections,
)


def test_p213_builds_private_cockpit_panel(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_private_cockpit_panel(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_PANEL_READY"
    assert payload["source_status"] == "OK_P212_PROMPT_HISTORY_RESPONSE_DRAFT_UI_READY"
    assert payload["panel"]["panel_id"] == "response_draft_review"
    assert payload["panel"]["route_hint"] == "/response-draft"
    assert payload["decision_header"]["source_selected"] is True
    assert payload["decision_header"]["response_text_present"] is True
    assert payload["decision_header"]["save_enabled"] is True
    assert payload["source_prompt_card"]["selection_status"] == "SELECTED"
    assert payload["save_plan_card"]["auto_apply_gem_response"] is False
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p213_empty_response_returns_review_panel(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_private_cockpit_panel(
        tmp_path,
        gem_response_text=" ",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_PANEL"
    assert "EMPTY_GEM_RESPONSE_TEXT" in payload["blockers"]
    assert payload["decision_header"]["save_enabled"] is False


def test_p213_missing_prompt_returns_review_panel(tmp_path: Path) -> None:
    payload = build_response_draft_private_cockpit_panel(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_PANEL"
    assert "NO_PROMPT_CARD_SELECTED" in payload["blockers"]
    assert payload["source_prompt_card"]["selection_status"] == "MISSING"


def test_p213_sections_bundle_three_queries(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_private_cockpit_sections(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_SECTIONS_READY"
    assert payload["panel_count"] == 3
    assert payload["review_panel_count"] == 0
    assert payload["blocked_panel_count"] == 0
    assert payload["recommended_next"] == "P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE_FAST_FUSE"
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False
