from pathlib import Path

from mvp_qaic_py.p212_prompt_history_response_draft_ui import (
    build_response_draft_ui_payload,
    build_response_draft_ui_summary,
)


def test_p212_builds_response_draft_ui_payload(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_ui_payload(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P212_PROMPT_HISTORY_RESPONSE_DRAFT_UI_READY"
    assert payload["source_status"] == "OK_P211_PROMPT_HISTORY_RESPONSE_DRAFT_READY"
    assert payload["ui"]["header"]["title"] == "GEM Response Draft"
    assert payload["ui"]["source_prompt_card"]["selection_status"] == "SELECTED"
    assert payload["ui"]["response_editor"]["text_present"] is True
    assert payload["ui"]["save_plan_card"]["mode"] == "LOCAL_OPERATOR_REVIEW_ONLY"
    assert payload["ui"]["save_plan_card"]["auto_apply_gem_response"] is False
    assert payload["markdown_preview"]
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p212_empty_response_is_review_and_save_disabled(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_ui_payload(
        tmp_path,
        gem_response_text="   ",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P212_PROMPT_HISTORY_RESPONSE_DRAFT_UI"
    assert "EMPTY_GEM_RESPONSE_TEXT" in payload["blockers"]
    save_action = [
        action
        for action in payload["ui"]["actions"]
        if action["action"] == "save_response_draft_local"
    ][0]
    assert save_action["enabled"] is False


def test_p212_missing_prompt_is_review(tmp_path: Path) -> None:
    payload = build_response_draft_ui_payload(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P212_PROMPT_HISTORY_RESPONSE_DRAFT_UI"
    assert payload["ui"]["source_prompt_card"]["selection_status"] == "MISSING"
    assert "NO_PROMPT_CARD_SELECTED" in payload["blockers"]


def test_p212_summary_reports_save_enabled(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_ui_payload(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )
    summary = build_response_draft_ui_summary(payload)

    assert summary["STATUS"] == "OK_P212_RESPONSE_DRAFT_UI_SUMMARY_READY"
    assert summary["source_selected"] is True
    assert summary["response_text_present"] is True
    assert summary["save_enabled"] is True
    assert summary["review_only"] is True
    assert summary["auto_apply_gem_response"] is False
    assert summary["server_started"] is False
    assert summary["browser_started"] is False
    assert summary["broker"] is False
    assert summary["order"] is False
    assert summary["sizing"] is False
