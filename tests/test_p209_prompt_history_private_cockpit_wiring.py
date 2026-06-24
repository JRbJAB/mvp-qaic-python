from pathlib import Path

from mvp_qaic_py.p209_prompt_history_private_cockpit_wiring import (
    build_private_cockpit_prompt_history_sections,
    build_prompt_history_private_cockpit_panel,
)


def test_p209_builds_private_cockpit_panel(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text(
        "# Prompt GEM\nCopier le prompt\nSauver réponse GEM localement",
        encoding="utf-8",
    )

    payload = build_prompt_history_private_cockpit_panel(
        tmp_path,
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P209_PROMPT_HISTORY_PRIVATE_COCKPIT_PANEL_READY"
    assert payload["source_status"] == "OK_P208_PROMPT_HISTORY_UI_BINDING_READY"
    assert payload["panel"]["panel_id"] == "prompt_history_library"
    assert payload["panel"]["route_hint"] == "/prompt-history"
    assert payload["decision_header"]["library_entry_count"] == 1
    assert payload["decision_header"]["card_count"] == 1
    assert payload["cards"][0]["title"] == "session_prompt_gem"
    assert "Prompt History Library" in payload["markdown_preview"]
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p209_empty_library_returns_review_panel(tmp_path: Path) -> None:
    payload = build_prompt_history_private_cockpit_panel(
        tmp_path,
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P209_PROMPT_HISTORY_PRIVATE_COCKPIT_PANEL"
    assert payload["source_status"] == "REVIEW_P208_PROMPT_HISTORY_UI_BINDING_EMPTY_LIBRARY"
    assert payload["decision_header"]["library_entry_count"] == 0
    assert payload["decision_header"]["card_count"] == 0


def test_p209_sections_bundle_queries(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_private_cockpit_prompt_history_sections(
        tmp_path,
        queries=("", "gem", "absent"),
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P209_PROMPT_HISTORY_PRIVATE_COCKPIT_SECTIONS"
    assert payload["panel_count"] == 3
    assert payload["review_panel_count"] == 1
    assert payload["blocked_panel_count"] == 0
    assert payload["recommended_next"] == "P210_PROMPT_HISTORY_OPERATOR_WORKFLOW_FAST_FUSE"
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
