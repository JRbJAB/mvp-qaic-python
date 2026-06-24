from pathlib import Path

from mvp_qaic_py.p214_response_draft_local_write_gate import (
    build_response_draft_local_write_gate,
    build_response_draft_local_write_gate_summary,
)


def test_p214_allows_safe_local_write_gate(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_response_draft_local_write_gate(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE_READY"
    assert payload["write_allowed"] is True
    assert payload["blocker_count"] == 0
    assert payload["output_inside_project"] is True
    assert payload["output_is_project_root"] is False
    assert payload["response_text_present"] is True
    assert payload["source_prompt_path"] == "01_OPERATOR_INPUTS/session_prompt_gem.md"
    assert payload["planned_files"]["json_filename"].endswith(".json")
    assert payload["planned_files"]["md_filename"].endswith(".md")
    assert payload["files_written"] is False
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p214_rejects_output_outside_project(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")
    outside = tmp_path.parent / "outside_p214_drafts"

    payload = build_response_draft_local_write_gate(
        tmp_path,
        outside,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE"
    assert payload["write_allowed"] is False
    assert "OUTPUT_DIR_OUTSIDE_PROJECT_ROOT" in payload["blockers"]
    assert payload["files_written"] is False


def test_p214_rejects_project_root_output(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")

    payload = build_response_draft_local_write_gate(
        tmp_path,
        tmp_path,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE"
    assert payload["write_allowed"] is False
    assert "OUTPUT_DIR_IS_PROJECT_ROOT" in payload["blockers"]


def test_p214_rejects_empty_response(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_response_draft_local_write_gate(
        tmp_path,
        output,
        gem_response_text=" ",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE"
    assert payload["write_allowed"] is False
    assert "EMPTY_GEM_RESPONSE_TEXT" in payload["blockers"]


def test_p214_rejects_missing_prompt(tmp_path: Path) -> None:
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_response_draft_local_write_gate(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE"
    assert payload["write_allowed"] is False
    assert "NO_PROMPT_CARD_SELECTED" in payload["blockers"]


def test_p214_summary_is_safe(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    gate = build_response_draft_local_write_gate(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )
    summary = build_response_draft_local_write_gate_summary(gate)

    assert summary["STATUS"] == "OK_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE_SUMMARY_READY"
    assert summary["write_allowed"] is True
    assert summary["files_written"] is False
    assert summary["review_only"] is True
    assert summary["auto_apply_gem_response"] is False
    assert summary["server_started"] is False
    assert summary["browser_started"] is False
    assert summary["broker"] is False
    assert summary["order"] is False
    assert summary["sizing"] is False
