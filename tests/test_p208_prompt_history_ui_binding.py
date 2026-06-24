from pathlib import Path

from mvp_qaic_py.p208_prompt_history_ui_binding import (
    build_prompt_history_ui_binding,
    build_prompt_history_ui_markdown,
)


def test_p208_builds_ui_cards_from_prompt_history(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text(
        "# Prompt GEM\nCopier le prompt\nSauver réponse GEM localement",
        encoding="utf-8",
    )

    payload = build_prompt_history_ui_binding(
        tmp_path,
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P208_PROMPT_HISTORY_UI_BINDING_READY"
    assert payload["library_entry_count"] == 1
    assert payload["card_count"] == 1
    assert payload["cards"][0]["title"] == "session_prompt_gem"
    assert "Copier le prompt" in payload["cards"][0]["actions"]
    assert payload["ui"]["title"] == "Prompt History Library"
    assert "Prompt GEM" in payload["ui"]["tabs"]
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p208_filters_cards_by_query(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")
    (inputs / "other_capture.txt").write_text("capture écran", encoding="utf-8")

    payload = build_prompt_history_ui_binding(
        tmp_path,
        query="session",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P208_PROMPT_HISTORY_UI_BINDING_READY"
    assert payload["library_entry_count"] == 2
    assert payload["filtered_entry_count"] == 1
    assert payload["cards"][0]["path"] == "01_OPERATOR_INPUTS/session_prompt_gem.md"


def test_p208_no_query_result_is_review(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_prompt_history_ui_binding(
        tmp_path,
        query="absent",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P208_PROMPT_HISTORY_UI_BINDING_NO_QUERY_RESULT"
    assert payload["library_entry_count"] == 1
    assert payload["filtered_entry_count"] == 0
    assert payload["card_count"] == 0


def test_p208_empty_library_is_review_not_blocked(tmp_path: Path) -> None:
    payload = build_prompt_history_ui_binding(
        tmp_path,
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P208_PROMPT_HISTORY_UI_BINDING_EMPTY_LIBRARY"
    assert payload["library_entry_count"] == 0
    assert payload["card_count"] == 0
    assert payload["recommended_next"] == "P209_PROMPT_HISTORY_PRIVATE_COCKPIT_WIRING_FAST_FUSE"


def test_p208_markdown_view_is_operator_readable(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_prompt_history_ui_binding(
        tmp_path,
        generated_at="2026-06-24T00:00:00Z",
    )
    markdown = build_prompt_history_ui_markdown(payload)

    assert "# Prompt History Library" in markdown
    assert "session_prompt_gem" in markdown
    assert "01_OPERATOR_INPUTS/session_prompt_gem.md" in markdown
