from pathlib import Path

from mvp_qaic_py.private_admin_app.app import (
    register_private_admin_pages,
    render_private_admin_normal_preview,
)
from mvp_qaic_py.private_admin_app.navigation import get_admin_navigation
from mvp_qaic_py.private_admin_app.shell import build_route_page_payload


class FakeContext:
    def __enter__(self) -> "FakeContext":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def classes(self, value: str) -> "FakeContext":
        return self

    def props(self, value: str) -> "FakeContext":
        return self


class FakeUI:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []
        self.registered_routes: list[str] = []

    def query(self, value: str) -> FakeContext:
        self.calls.append(("query", value))
        return FakeContext()

    def add_head_html(self, value: str) -> None:
        self.calls.append(("head", value))

    def column(self) -> FakeContext:
        self.calls.append(("column", "column"))
        return FakeContext()

    def left_drawer(self, value: bool = True) -> FakeContext:
        self.calls.append(("left_drawer", str(value)))
        return FakeContext()

    def header(self) -> FakeContext:
        self.calls.append(("header", "header"))
        return FakeContext()

    def label(self, value: str) -> FakeContext:
        self.calls.append(("label", value))
        return FakeContext()

    def link(self, label: str, target: str) -> FakeContext:
        self.calls.append(("link", f"{label}|{target}"))
        return FakeContext()

    def separator(self) -> FakeContext:
        self.calls.append(("separator", "separator"))
        return FakeContext()

    def space(self) -> None:
        self.calls.append(("space", "space"))

    def html(self, value: str) -> None:
        self.calls.append(("html", value))

    def page(self, route: str):
        def decorator(func):
            self.registered_routes.append(route)
            return func

        return decorator


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


def test_p219d2_builds_route_payload_for_base_python(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    payload = build_route_page_payload(tmp_path, active_route="/base-python")

    assert payload["STATUS"] == "OK_P219D2_ROUTE_PAGE_PAYLOAD_READY"
    assert payload["title"] == "Base Python"
    assert payload["active_route"] == "/base-python"
    assert payload["provider_call_executed"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p219d2_registers_all_navigation_routes() -> None:
    ui = FakeUI()

    register_private_admin_pages(ui, ".")

    expected = {item["route"] for item in get_admin_navigation()}
    assert set(ui.registered_routes) == expected


def test_p219d2_renders_normal_preview_with_top_level_left_menu(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    ui = FakeUI()

    result = render_private_admin_normal_preview(ui, tmp_path, active_route="/google-sheets")

    assert result["STATUS"] == "OK_P219D2_PRIVATE_ADMIN_NORMAL_PREVIEW_RENDERED"
    assert result["navigation_count"] >= 9
    assert result["left_drawer_top_level"] is True
    assert result["header_top_level"] is True
    assert ("left_drawer", "True") in ui.calls
    assert ("header", "header") in ui.calls
    assert any(call[0] == "link" and "Base Python" in call[1] for call in ui.calls)
    assert any(call[0] == "link" and "Google Sheets" in call[1] for call in ui.calls)
    assert any(call[0] == "html" and "Menu latéral officiel" in call[1] for call in ui.calls)
    assert result["server_started"] is False
    assert result["browser_started"] is False
    assert result["broker"] is False
    assert result["order"] is False
    assert result["sizing"] is False
