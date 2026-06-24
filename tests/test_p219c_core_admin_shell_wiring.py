from pathlib import Path
from typing import Any

from mvp_qaic_py.p219c_core_admin_shell_wiring import (
    TARGET_ADMIN_NAVIGATION,
    build_core_admin_shell_html,
    build_core_admin_shell_payload,
    build_shell_wiring_markdown,
    is_source_shell_candidate,
    render_core_admin_shell_nicegui,
    select_primary_nicegui_shell,
)


class FakeNiceGUI:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def html(self, content: str) -> None:
        self.calls.append(("html", content))

    def markdown(self, content: str) -> None:
        self.calls.append(("markdown", content))


def _seed_project(root: Path) -> None:
    package = root / "mvp_qaic_py"
    package.mkdir()
    (package / "p217_nicegui_private_cockpit_ui_wiring.py").write_text(
        "from nicegui import ui\n\n@ui.page('/')\ndef private_cockpit():\n    ui.left_drawer()\n    ui.tabs()\n    ui.html('cockpit')\n",
        encoding="utf-8",
    )
    export = root / "05_EXPORTS" / "P143B"
    export.mkdir(parents=True)
    (export / "P143B_NICEGUI_DATA_PREVIEW_APP.py").write_text(
        "from nicegui import ui\n\n@ui.page('/')\ndef exported_app():\n    ui.left_drawer()\n    ui.tabs()\n    ui.html('exported')\n",
        encoding="utf-8",
    )
    (root / "docs").mkdir()
    (root / "docs" / "architecture.md").write_text("# Architecture", encoding="utf-8")
    (root / "01_OPERATOR_INPUTS").mkdir()
    (root / "01_OPERATOR_INPUTS" / "prompt.md").write_text("# Prompt", encoding="utf-8")


def test_p219c_identifies_source_shell_candidates() -> None:
    assert is_source_shell_candidate(
        {
            "path": "mvp_qaic_py/p217_nicegui_private_cockpit_ui_wiring.py",
            "has_nicegui": True,
        }
    )
    assert not is_source_shell_candidate(
        {
            "path": "05_EXPORTS/P143B/P143B_NICEGUI_DATA_PREVIEW_APP.py",
            "has_nicegui": True,
        }
    )
    assert not is_source_shell_candidate(
        {
            "path": "tests/test_ui.py",
            "has_nicegui": True,
        }
    )


def test_p219c_selects_source_shell_over_export_shell() -> None:
    core = {
        "ui_candidates": [
            {
                "path": "05_EXPORTS/P143B/P143B_NICEGUI_DATA_PREVIEW_APP.py",
                "layer": "nicegui_private_cockpit",
                "score": 999,
                "has_nicegui": True,
                "has_menu_signal": True,
                "routes": ["/"],
            },
            {
                "path": "mvp_qaic_py/p217_nicegui_private_cockpit_ui_wiring.py",
                "layer": "private_cockpit_wiring",
                "score": 5,
                "has_nicegui": True,
                "has_menu_signal": True,
                "routes": ["/"],
            },
        ]
    }

    selection = select_primary_nicegui_shell(core)

    assert selection["STATUS"] == "OK_P219C_PRIMARY_SOURCE_NICEGUI_SHELL_SELECTED"
    assert selection["selected"]["path"].startswith("mvp_qaic_py/")
    assert selection["fallback_used"] is False
    assert selection["ignored_non_source_nicegui_count"] == 1


def test_p219c_builds_shell_payload_with_source_selection(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    payload = build_core_admin_shell_payload(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P219C_CORE_ADMIN_SHELL_PAYLOAD_READY"
    assert payload["navigation_count"] == len(TARGET_ADMIN_NAVIGATION)
    assert any(item["route"] == "/documents" for item in payload["navigation"])
    assert any(item["route"] == "/architecture" for item in payload["navigation"])
    assert (
        payload["primary_shell_selection"]["STATUS"]
        == "OK_P219C_PRIMARY_SOURCE_NICEGUI_SHELL_SELECTED"
    )
    assert payload["shell_strategy"]["mode"] == "SOURCE_SHELL_ADAPTER_FIRST_NO_DESTRUCTIVE_PATCH"
    assert payload["shell_strategy"]["selected_shell_path"].startswith("mvp_qaic_py/")
    assert payload["shell_strategy"]["selected_shell_is_source"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["provider_call_executed"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p219c_shell_html_contains_source_shell_and_navigation(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_core_admin_shell_payload(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )

    html = build_core_admin_shell_html(payload)

    assert "Noyau MVP QAIC" in html
    assert "Shell NiceGUI source sélectionné" in html
    assert "Is source: True" in html
    assert "/documents" in html
    assert "/architecture" in html
    assert "<table>" in html


def test_p219c_renders_nicegui_shell(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_core_admin_shell_payload(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )
    ui: Any = FakeNiceGUI()

    result = render_core_admin_shell_nicegui(ui, payload)

    assert result["STATUS"] == "OK_P219C_CORE_ADMIN_SHELL_NICEGUI_RENDERED"
    assert result["rendered_count"] == 2
    assert ui.calls[0][0] == "html"
    assert ui.calls[1][0] == "markdown"
    assert "Noyau MVP QAIC" in ui.calls[0][1]
    assert "Shell admin MVP QAIC" in ui.calls[1][1]
    assert "source" in ui.calls[1][1]
    assert result["server_started"] is False
    assert result["browser_started"] is False
    assert result["broker"] is False
    assert result["order"] is False
    assert result["sizing"] is False


def test_p219c_builds_shell_wiring_markdown(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_core_admin_shell_payload(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )

    markdown = build_shell_wiring_markdown(payload)

    assert "# P219C-R3" in markdown
    assert "/documents" in markdown
    assert "Selected shell is source: True" in markdown
    assert "P219D" in markdown
