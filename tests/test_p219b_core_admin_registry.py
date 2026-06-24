from pathlib import Path
from typing import Any

from mvp_qaic_py.p219b_core_admin_registry import (
    build_core_admin_audit_markdown,
    build_core_admin_html,
    build_core_admin_registry,
    render_core_admin_nicegui,
    scan_ui_foundation,
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
        "from nicegui import ui\n\n@ui.page('/')\ndef cockpit():\n    ui.left_drawer()\n    ui.tabs()\n",
        encoding="utf-8",
    )
    (package / "p219a_document_management_ui_foundation.py").write_text(
        "def build_document_management_ui_payload(*args, **kwargs):\n    return {}\n",
        encoding="utf-8",
    )
    (root / "docs").mkdir()
    (root / "docs" / "architecture.md").write_text("# Architecture", encoding="utf-8")
    (root / "01_OPERATOR_INPUTS").mkdir()
    (root / "01_OPERATOR_INPUTS" / "prompt.md").write_text("# Prompt", encoding="utf-8")


def test_p219b_scans_existing_ui_foundation(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    candidates = scan_ui_foundation(tmp_path)

    assert candidates
    assert any(item["has_nicegui"] for item in candidates)
    assert any(item["has_menu_signal"] for item in candidates)
    assert any(item["layer"] == "private_cockpit_wiring" for item in candidates)


def test_p219b_source_first_scan_reaches_mvp_source_before_exports(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    export_root = tmp_path / "05_EXPORTS" / "many"
    export_root.mkdir(parents=True)
    for i in range(30):
        (export_root / f"export_{i}.py").write_text(
            "from nicegui import ui\n\n@ui.page('/')\ndef index():\n    ui.html('export')\n",
            encoding="utf-8",
        )

    candidates = scan_ui_foundation(tmp_path, max_files=5)

    assert any(
        item["path"] == "mvp_qaic_py/p217_nicegui_private_cockpit_ui_wiring.py"
        for item in candidates
    )


def test_p219b_builds_core_admin_registry(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    payload = build_core_admin_registry(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P219B_CORE_ADMIN_REGISTRY_READY"
    assert payload["ui_candidate_count"] >= 2
    assert payload["nicegui_candidate_count"] >= 1
    assert payload["target_routes"][0]["route"] == "/"
    assert any(route["route"] == "/documents" for route in payload["target_routes"])
    assert payload["safety_registry"]["HUMAN_REVIEW_ONLY"] is True
    assert payload["safety_registry"]["NO_BROKER"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["provider_call_executed"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p219b_core_admin_html_contains_target_routes(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_core_admin_registry(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )

    html = build_core_admin_html(payload)

    assert "Noyau d'administration MVP QAIC" in html
    assert "/documents" in html
    assert "/architecture" in html
    assert "Safety registry" in html
    assert "<table>" in html


def test_p219b_renders_core_admin_nicegui(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_core_admin_registry(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )
    ui: Any = FakeNiceGUI()

    result = render_core_admin_nicegui(ui, payload)

    assert result["STATUS"] == "OK_P219B_CORE_ADMIN_NICEGUI_RENDERED"
    assert result["rendered_count"] == 2
    assert ui.calls[0][0] == "html"
    assert ui.calls[1][0] == "markdown"
    assert "Noyau d'administration" in ui.calls[0][1]
    assert "Noyau d'administration" in ui.calls[1][1]
    assert result["server_started"] is False
    assert result["browser_started"] is False
    assert result["broker"] is False
    assert result["order"] is False
    assert result["sizing"] is False


def test_p219b_builds_audit_markdown(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_core_admin_registry(
        tmp_path,
        generated_at="2026-06-25T00:00:00Z",
    )

    markdown = build_core_admin_audit_markdown(payload)

    assert "# P219B/P219C-R3" in markdown
    assert "NiceGUI Private Admin Cockpit" in markdown
    assert "Safety registry" in markdown
    assert "P219D" in markdown
