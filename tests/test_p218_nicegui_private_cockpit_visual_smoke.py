from pathlib import Path

from mvp_qaic_py.p218_nicegui_private_cockpit_visual_smoke import (
    build_private_cockpit_static_html,
    build_private_cockpit_visual_smoke_payload,
    write_private_cockpit_visual_smoke_files,
)


def _seed_prompt(root: Path) -> None:
    inputs = root / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")


def test_p218_builds_visual_smoke_payload(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P218_VISUAL_SMOKE"

    payload = build_private_cockpit_visual_smoke_payload(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P218_NICEGUI_PRIVATE_COCKPIT_VISUAL_SMOKE_READY"
    assert payload["source_status"] == "OK_P217_NICEGUI_PRIVATE_COCKPIT_VIEW_MODEL_READY"
    assert "MVP QAIC Private Prompt Cockpit" in payload["html_preview"]
    assert "Sauver brouillon local" in payload["html_preview"]
    assert payload["html_preview_bytes"] > 1000
    assert len(payload["observation_checklist"]) == 6
    assert payload["observation_required"] is True
    assert payload["operator_decision_values"] == ["OK", "UX_POLISH", "BLOCKER"]
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p218_review_when_prompt_missing(tmp_path: Path) -> None:
    output = tmp_path / "05_EXPORTS" / "P218_VISUAL_SMOKE"

    payload = build_private_cockpit_visual_smoke_payload(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P218_NICEGUI_PRIVATE_COCKPIT_VISUAL_SMOKE"
    assert "NO_PROMPT_CARD_SELECTED" in payload["blockers"]
    assert "Sauver brouillon local" in payload["html_preview"]


def test_p218_static_html_escapes_user_content(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P218_VISUAL_SMOKE"
    payload = build_private_cockpit_visual_smoke_payload(
        tmp_path,
        output,
        gem_response_text="<script>alert(1)</script>",
        generated_at="2026-06-24T00:00:00Z",
    )

    html = build_private_cockpit_static_html(payload["view_model_payload"])

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_p218_write_visual_smoke_files_is_explicit(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P218_VISUAL_SMOKE"
    payload = build_private_cockpit_visual_smoke_payload(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    result = write_private_cockpit_visual_smoke_files(payload, output)

    assert result["files_written"] is True
    assert Path(result["html_path"]).exists()
    assert Path(result["json_path"]).exists()
    assert Path(result["html_path"]).parent == output
    assert Path(result["json_path"]).parent == output
    assert "MVP QAIC Private Prompt Cockpit" in Path(result["html_path"]).read_text(
        encoding="utf-8"
    )
