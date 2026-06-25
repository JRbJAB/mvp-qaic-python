from pathlib import Path
from typing import Any

from mvp_qaic_py.private_admin_app.navigation import (
    get_admin_navigation,
    get_navigation_groups,
    get_route_index,
)
from mvp_qaic_py.private_admin_app.shell import (
    build_architecture_blueprint_svg,
    build_private_admin_shell_html,
    build_private_admin_shell_payload,
    inspect_p173_old_menu,
    render_private_admin_shell_nicegui,
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
    (package / "p173_nicegui_private_local_runner.py").write_text(
        "from nicegui import ui\n\n"
        "@ui.page('/')\n"
        "def index():\n"
        "    with ui.left_drawer():\n"
        "        ui.link('Base Python', '/base-python')\n"
        "        ui.link('Google Sheets', '/google-sheets')\n"
        "        ui.link('GitHub', '/github')\n"
        "    ui.tabs()\n",
        encoding="utf-8",
    )
    (package / "p217_nicegui_private_cockpit_ui_wiring.py").write_text(
        "from nicegui import ui\n\n@ui.page('/')\ndef cockpit():\n    ui.left_drawer()\n",
        encoding="utf-8",
    )
    (root / "docs").mkdir()
    (root / "docs" / "architecture.md").write_text("# Architecture", encoding="utf-8")
    (root / "01_OPERATOR_INPUTS").mkdir()
    (root / "01_OPERATOR_INPUTS" / "prompt.md").write_text("# Prompt", encoding="utf-8")


def test_p219d1_navigation_contains_required_old_menu_entries() -> None:
    nav = get_admin_navigation()
    labels = {item["label"] for item in nav}
    routes = get_route_index()

    assert "Base Python" in labels
    assert "Google Sheets" in labels
    assert "Prompt Cockpit" in labels
    assert "Documents" in labels
    assert "Architecture" in labels
    assert "/base-python" in routes
    assert "/google-sheets" in routes


def test_p219d1_navigation_groups_are_stable() -> None:
    groups = get_navigation_groups()

    assert "foundation" in groups
    assert "workflow" in groups
    assert "knowledge" in groups
    assert "governance" in groups


def test_p219d1_inspects_p173_old_menu_source(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    evidence = inspect_p173_old_menu(tmp_path)

    assert evidence["STATUS"] == "OK_P173_OLD_MENU_SOURCE_CONFIRMED"
    assert evidence["exists"] is True
    assert evidence["has_left_drawer"] is True
    assert evidence["has_base_python"] is True
    assert evidence["has_sheets"] is True
    assert evidence["menu_evidence_score"] >= 3


def test_p219d1_builds_private_admin_shell_payload(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    payload = build_private_admin_shell_payload(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P219D1_PRIVATE_ADMIN_SHELL_PAYLOAD_READY"
    assert payload["old_menu_source"]["path"] == "mvp_qaic_py/p173_nicegui_private_local_runner.py"
    assert payload["navigation_count"] >= 9
    assert payload["safety_flags"]["HUMAN_REVIEW_ONLY"] is True
    assert payload["safety_flags"]["NO_BROKER"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["provider_call_executed"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p219d1_html_and_svg_include_old_menu_and_architecture(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_private_admin_shell_payload(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )

    html = build_private_admin_shell_html(payload)
    svg = build_architecture_blueprint_svg()

    assert "MVP QAIC — Private Admin Shell" in html
    assert "Base Python" in html
    assert "Google Sheets" in html
    assert "Source historique P173" in html
    assert "<svg" in svg
    assert "P173 Old Menu" in svg
    assert "Core Registries" in svg


def test_p219d1_renders_private_admin_shell_nicegui(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_private_admin_shell_payload(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )
    ui: Any = FakeNiceGUI()

    result = render_private_admin_shell_nicegui(ui, payload)

    assert result["STATUS"] == "OK_P219D1_PRIVATE_ADMIN_SHELL_NICEGUI_RENDERED"
    assert result["rendered_count"] == 3
    assert ui.calls[0][0] == "html"
    assert ui.calls[1][0] == "html"
    assert ui.calls[2][0] == "markdown"
    assert "Private Admin App" in ui.calls[0][1]
    assert "Private Admin Shell" in ui.calls[1][1]
    assert "Private Admin Shell" in ui.calls[2][1]
    assert result["server_started"] is False
    assert result["browser_started"] is False
    assert result["broker"] is False
    assert result["order"] is False
    assert result["sizing"] is False
