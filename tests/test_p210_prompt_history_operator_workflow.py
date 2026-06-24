from pathlib import Path

from mvp_qaic_py.p210_prompt_history_operator_workflow import (
    build_prompt_history_operator_action_menu,
    build_prompt_history_operator_workflow,
)


def test_p210_copy_prompt_workflow_selects_first_card(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text(
        "# Prompt GEM\nCopier le prompt\nSauver réponse GEM localement",
        encoding="utf-8",
    )

    payload = build_prompt_history_operator_workflow(
        tmp_path,
        action="copy_prompt",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P210_PROMPT_HISTORY_OPERATOR_WORKFLOW_READY"
    assert payload["blocker_count"] == 0
    assert payload["selected_card_found"] is True
    assert payload["workflow"]["action"] == "copy_prompt"
    assert payload["workflow"]["copy_payload"]["clipboard_access"] is False
    assert payload["workflow"]["copy_payload"]["copy_mode"] == "MANUAL_COPY_ONLY"
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p210_save_response_requires_text(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_prompt_history_operator_workflow(
        tmp_path,
        action="save_gem_response_local",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P210_PROMPT_HISTORY_OPERATOR_WORKFLOW"
    assert "EMPTY_GEM_RESPONSE_TEXT" in payload["blockers"]
    assert payload["workflow"]["save_response_payload"]["auto_apply_gem_response"] is False


def test_p210_save_response_with_text_is_ready(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_prompt_history_operator_workflow(
        tmp_path,
        action="save_gem_response_local",
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P210_PROMPT_HISTORY_OPERATOR_WORKFLOW_READY"
    assert payload["workflow"]["save_response_payload"]["gem_response_text_present"] is True
    assert (
        payload["workflow"]["save_response_payload"]["write_mode"] == "LOCAL_OPERATOR_REVIEW_ONLY"
    )


def test_p210_unsupported_action_is_review(tmp_path: Path) -> None:
    payload = build_prompt_history_operator_workflow(
        tmp_path,
        action="bad_action",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P210_PROMPT_HISTORY_OPERATOR_WORKFLOW"
    assert "UNSUPPORTED_ACTION:bad_action" in payload["blockers"]
    assert "NO_PROMPT_CARD_SELECTED" in payload["blockers"]


def test_p210_action_menu_is_safe() -> None:
    payload = build_prompt_history_operator_action_menu()

    assert payload["STATUS"] == "OK_P210_PROMPT_HISTORY_OPERATOR_ACTION_MENU_READY"
    assert len(payload["actions"]) == 3
    assert payload["clipboard_access"] is False
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False
