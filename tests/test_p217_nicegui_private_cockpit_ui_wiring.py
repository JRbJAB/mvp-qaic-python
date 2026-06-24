from pathlib import Path
from typing import Any

from mvp_qaic_py.p217_nicegui_private_cockpit_ui_wiring import (
    build_nicegui_private_cockpit_view_model,
    render_nicegui_private_cockpit,
)


class FakeUI:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def label(self, text: str) -> None:
        self.calls.append(("label", text))

    def button(self, text: str) -> None:
        self.calls.append(("button", text))


def _seed_prompt(root: Path) -> None:
    inputs = root / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text("Prompt GEM", encoding="utf-8")


def test_p217_builds_nicegui_view_model(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_nicegui_private_cockpit_view_model(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
        execute_export=False,
    )

    assert payload["STATUS"] == "OK_P217_NICEGUI_PRIVATE_COCKPIT_VIEW_MODEL_READY"
    assert payload["bundle_status"] == "OK_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE_READY"
    assert payload["view_model"]["header"]["title"] == "MVP QAIC Private Prompt Cockpit"
    assert len(payload["view_model"]["tabs"]) == 4
    assert len(payload["view_model"]["cards"]) == 3
    assert payload["view_model"]["actions"][2]["id"] == "save_response_draft_local"
    assert payload["view_model"]["actions"][2]["enabled"] is True
    assert payload["view_model"]["safety"]["local_only"] is True
    assert payload["view_model"]["safety"]["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["provider_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p217_view_model_review_when_missing_prompt(tmp_path: Path) -> None:
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"

    payload = build_nicegui_private_cockpit_view_model(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P217_NICEGUI_PRIVATE_COCKPIT_VIEW_MODEL"
    assert "NO_PROMPT_CARD_SELECTED" in payload["blockers"]
    assert payload["view_model"]["actions"][2]["enabled"] is False


def test_p217_render_with_fake_ui_adapter(tmp_path: Path) -> None:
    _seed_prompt(tmp_path)
    output = tmp_path / "05_EXPORTS" / "P215_DRAFTS"
    payload = build_nicegui_private_cockpit_view_model(
        tmp_path,
        output,
        gem_response_text="Réponse GEM test",
        generated_at="2026-06-24T00:00:00Z",
    )

    fake_ui: Any = FakeUI()
    rendered = render_nicegui_private_cockpit(fake_ui, payload)

    assert rendered["STATUS"] == "OK_P217_NICEGUI_PRIVATE_COCKPIT_RENDERED_WITH_UI_ADAPTER"
    assert rendered["rendered_count"] > 8
    assert ("label", "MVP QAIC Private Prompt Cockpit") in fake_ui.calls
    assert ("button", "Sauver brouillon local") in fake_ui.calls
    assert rendered["server_started"] is False
    assert rendered["browser_started"] is False
    assert rendered["gem_call_executed"] is False
    assert rendered["provider_call_executed"] is False
    assert rendered["broker"] is False
    assert rendered["order"] is False
    assert rendered["sizing"] is False
