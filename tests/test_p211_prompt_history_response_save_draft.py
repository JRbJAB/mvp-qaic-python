from pathlib import Path

from mvp_qaic_py.p211_prompt_history_response_save_draft import (
    build_response_draft_markdown,
    build_response_draft_payload,
    safe_draft_slug,
    write_response_draft_files,
)


def test_p211_builds_response_draft_payload(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_payload(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P211_PROMPT_HISTORY_RESPONSE_DRAFT_READY"
    assert payload["blocker_count"] == 0
    assert payload["source_prompt_path"] == "01_OPERATOR_INPUTS/session_prompt_gem.md"
    assert payload["response_text_present"] is True
    assert payload["write_plan"]["mode"] == "LOCAL_OPERATOR_REVIEW_ONLY"
    assert payload["write_plan"]["auto_apply_gem_response"] is False
    assert payload["write_plan"]["requires_human_review"] is True
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p211_empty_response_is_review(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_payload(
        tmp_path,
        gem_response_text="   ",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P211_PROMPT_HISTORY_RESPONSE_DRAFT"
    assert "EMPTY_GEM_RESPONSE_TEXT" in payload["blockers"]
    assert payload["response_text_present"] is False


def test_p211_markdown_is_review_only(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_payload(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )
    markdown = build_response_draft_markdown(payload)

    assert "GEM Response Draft" in markdown
    assert "LOCAL_OPERATOR_REVIEW_ONLY" in markdown
    assert "Auto-apply GEM response: `false`" in markdown


def test_p211_write_response_draft_files_is_explicit(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_payload(
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    output = tmp_path / "drafts"
    result = write_response_draft_files(payload, output)

    assert result["files_written"] is True
    assert Path(result["json_path"]).exists()
    assert Path(result["md_path"]).exists()
    assert Path(result["json_path"]).parent == output
    assert Path(result["md_path"]).parent == output


def test_p211_safe_draft_slug() -> None:
    assert safe_draft_slug(" Prompt / GEM : test ") == "Prompt_GEM_test"
    assert safe_draft_slug("///") == "gem_response_draft"
