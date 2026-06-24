from pathlib import Path
from typing import Any

from mvp_qaic_py.p219a_document_management_ui_foundation import (
    build_document_management_html,
    build_document_management_ui_payload,
    render_document_management_nicegui,
    scan_document_registry,
)


class FakeNiceGUI:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def html(self, content: str) -> None:
        self.calls.append(("html", content))

    def markdown(self, content: str) -> None:
        self.calls.append(("markdown", content))


def _seed_project(root: Path) -> None:
    (root / "01_OPERATOR_INPUTS").mkdir()
    (root / "01_OPERATOR_INPUTS" / "prompt_capture.md").write_text("# Prompt", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "architecture.md").write_text("# Architecture", encoding="utf-8")
    (root / "mvp_qaic_py").mkdir()
    (root / "mvp_qaic_py" / "nicegui_document_ui.py").write_text(
        "def view():\n    return {}\n", encoding="utf-8"
    )
    (root / "tests").mkdir()
    (root / "tests" / "test_document_ui.py").write_text(
        "def test_ok():\n    assert True\n", encoding="utf-8"
    )


def test_p219a_scans_document_registry(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    docs = scan_document_registry(tmp_path)

    assert len(docs) == 4
    assert {doc["group"] for doc in docs} >= {
        "operator_inputs",
        "docs",
        "python_ui_modules",
        "tests",
    }
    assert any(doc["is_ui_related"] for doc in docs)
    assert not any(doc["name"] == "desktop.ini" for doc in docs)


def test_p219a_builds_payload_with_svg_and_auto_update(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    payload = build_document_management_ui_payload(tmp_path, generated_at="2026-06-25T00:00:00Z")

    assert payload["STATUS"] == "OK_P219A_DOCUMENT_MANAGEMENT_UI_PAYLOAD_READY"
    assert payload["document_count"] == 4
    assert payload["group_count"] == 4
    assert payload["ui_related_count"] >= 1
    assert "<svg" in payload["svg_schema"]
    assert "MVP QAIC" in payload["svg_schema"]
    assert payload["html_strategy"]["primary"] == "ui.html"
    assert payload["html_strategy"]["auto_update"] == "rebuild payload by rescanning project roots"
    assert payload["server_started"] is False
    assert payload["browser_started"] is False


def test_p219a_payload_updates_when_file_added(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    first = build_document_management_ui_payload(tmp_path, generated_at="2026-06-25T00:00:00Z")
    (tmp_path / "docs" / "new_interface_note.md").write_text("# New", encoding="utf-8")
    second = build_document_management_ui_payload(tmp_path, generated_at="2026-06-25T00:01:00Z")

    assert second["document_count"] == first["document_count"] + 1
    assert any(doc["name"] == "new_interface_note.md" for doc in second["documents"])


def test_p219a_builds_html(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    payload = build_document_management_ui_payload(tmp_path, generated_at="2026-06-25T00:00:00Z")
    html = build_document_management_html(payload)

    assert "Gestion documentaire MVP QAIC" in html
    assert "prompt_capture.md" in html
    assert "architecture.md" in html
    assert "<svg" in html
    assert "<table>" in html


def test_p219a_renders_nicegui_html_markdown(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    payload = build_document_management_ui_payload(tmp_path, generated_at="2026-06-25T00:00:00Z")
    ui: Any = FakeNiceGUI()

    rendered = render_document_management_nicegui(ui, payload)

    assert rendered["STATUS"] == "OK_P219A_DOCUMENT_MANAGEMENT_NICEGUI_RENDERED"
    assert rendered["rendered_count"] == 2
    assert ui.calls[0][0] == "html"
    assert ui.calls[1][0] == "markdown"
    assert "Gestion documentaire MVP QAIC" in ui.calls[0][1]
    assert "Suivi interface MVP" in ui.calls[1][1]
    assert rendered["server_started"] is False
    assert rendered["browser_started"] is False
    assert rendered["gem_call_executed"] is False
    assert rendered["provider_call_executed"] is False
    assert rendered["broker"] is False
    assert rendered["order"] is False
    assert rendered["sizing"] is False
