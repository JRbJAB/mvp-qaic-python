from pathlib import Path

from mvp_qaic_py.p216_private_cockpit_runtime_bundle import (
    build_private_cockpit_runtime_bundle,
    build_private_cockpit_runtime_summary,
)


def _seed_prompt(root: Path) -> None:
    inputs = root / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")


def test_p216_builds_ready_runtime_bundle_without_export_write(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_private_cockpit_runtime_bundle(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_export=False,
    )

    assert payload["STATUS"] == "OK_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE_READY"
    assert payload["component_statuses"]["prompt_history"].startswith("OK_")
    assert payload["component_statuses"]["response_draft_panel"].startswith("OK_")
    assert (
        payload["component_statuses"]["export_runtime"]
        == "OK_P215_RESPONSE_DRAFT_LOCAL_EXPORT_PLAN_READY"
    )
    assert payload["decision_header"]["export_allowed"] is True
    assert payload["decision_header"]["execute_export"] is False
    assert payload["decision_header"]["files_written"] is False
    assert not output.exists()
    assert payload["cockpit"]["runtime_mode"] == "LOCAL_PRIVATE_REVIEW_ONLY"
    assert "/prompt-history" in payload["cockpit"]["route_hints"]
    assert "/response-draft" in payload["cockpit"]["route_hints"]
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p216_can_execute_export_when_explicit(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_private_cockpit_runtime_bundle(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_export=True,
    )

    assert payload["STATUS"] == "OK_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE_READY"
    assert payload["decision_header"]["execute_export"] is True
    assert payload["decision_header"]["files_written"] is True
    assert Path(payload["export_runtime"]["json_path"]).exists()
    assert Path(payload["export_runtime"]["md_path"]).exists()


def test_p216_review_when_prompt_missing(tmp_path: Path) -> None:
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_private_cockpit_runtime_bundle(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_export=False,
    )

    assert payload["STATUS"] == "REVIEW_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE"
    assert "NO_PROMPT_CARD_SELECTED" in payload["blockers"]
    assert payload["decision_header"]["export_allowed"] is False
    assert payload["decision_header"]["files_written"] is False


def test_p216_review_when_response_empty(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_private_cockpit_runtime_bundle(
        tmp_path,
        output,
        gem_response_text=" ",
        generated_at="2026-06-24T00:00:00Z",
        execute_export=False,
    )

    assert payload["STATUS"] == "REVIEW_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE"
    assert "EMPTY_GEM_RESPONSE_TEXT" in payload["blockers"]
    assert payload["decision_header"]["export_allowed"] is False


def test_p216_summary_is_safe(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    bundle = build_private_cockpit_runtime_bundle(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_export=False,
    )
    summary = build_private_cockpit_runtime_summary(bundle)

    assert summary["STATUS"] == "OK_P216_PRIVATE_COCKPIT_RUNTIME_SUMMARY_READY"
    assert summary["bundle_status"] == "OK_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE_READY"
    assert summary["export_allowed"] is True
    assert summary["execute_export"] is False
    assert summary["files_written"] is False
    assert summary["review_only"] is True
    assert summary["server_started"] is False
    assert summary["browser_started"] is False
    assert summary["gem_call_executed"] is False
    assert summary["provider_call_executed"] is False
    assert summary["broker"] is False
    assert summary["order"] is False
    assert summary["sizing"] is False
