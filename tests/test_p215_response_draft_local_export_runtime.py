from pathlib import Path

from mvp_qaic_py.p215_response_draft_local_export_runtime import (
    build_response_draft_local_export_summary,
    run_response_draft_local_export,
)


def _seed_prompt(root: Path) -> None:
    inputs = root / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")


def test_p215_plan_mode_does_not_write_files(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = run_response_draft_local_export(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_write=False,
    )

    assert payload["STATUS"] == "OK_P215_RESPONSE_DRAFT_LOCAL_EXPORT_PLAN_READY"
    assert payload["export_allowed"] is True
    assert payload["execute_write"] is False
    assert payload["files_written"] is False
    assert not output.exists()
    assert payload["json_path"].endswith(".json")
    assert payload["md_path"].endswith(".md")
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p215_execute_write_creates_json_and_md(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = run_response_draft_local_export(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_write=True,
    )

    assert payload["STATUS"] == "OK_P215_RESPONSE_DRAFT_LOCAL_EXPORT_RUNTIME_EXPORTED"
    assert payload["export_allowed"] is True
    assert payload["execute_write"] is True
    assert payload["files_written"] is True
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert Path(payload["json_path"]).parent == output
    assert Path(payload["md_path"]).parent == output


def test_p215_rejects_when_gate_rejects(tmp_path: Path) -> None:
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = run_response_draft_local_export(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_write=True,
    )

    assert payload["STATUS"] == "REVIEW_P215_RESPONSE_DRAFT_LOCAL_EXPORT_RUNTIME"
    assert payload["export_allowed"] is False
    assert payload["files_written"] is False
    assert "NO_PROMPT_CARD_SELECTED" in payload["blockers"]
    assert not output.exists()


def test_p215_rejects_output_outside_project(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    outside = tmp_path.parent / "outside_p215"

    payload = run_response_draft_local_export(
        tmp_path,
        outside,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_write=True,
    )

    assert payload["STATUS"] == "REVIEW_P215_RESPONSE_DRAFT_LOCAL_EXPORT_RUNTIME"
    assert payload["export_allowed"] is False
    assert "OUTPUT_DIR_OUTSIDE_PROJECT_ROOT" in payload["blockers"]


def test_p215_summary_is_safe(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = run_response_draft_local_export(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_write=False,
    )
    summary = build_response_draft_local_export_summary(payload)

    assert summary["STATUS"] == "OK_P215_RESPONSE_DRAFT_LOCAL_EXPORT_SUMMARY_READY"
    assert summary["export_allowed"] is True
    assert summary["execute_write"] is False
    assert summary["files_written"] is False
    assert summary["review_only"] is True
    assert summary["auto_apply_gem_response"] is False
    assert summary["server_started"] is False
    assert summary["browser_started"] is False
    assert summary["broker"] is False
    assert summary["order"] is False
    assert summary["sizing"] is False
