from __future__ import annotations

import json

from mvp_qaic_py.release.local_mvp_seal import (
    build_local_mvp_seal,
    export_local_mvp_seal,
    render_local_mvp_seal_markdown,
)


def test_p89_local_mvp_sealed() -> None:
    seal = build_local_mvp_seal()
    assert seal["status"] == "OK_P89_LOCAL_MVP_SEALED"
    assert seal["release_status"] == "OK_P87_OPERATOR_RELEASE_PACK_READY"
    assert seal["sheets_dryrun_status"] == "OK_P88_SHEETS_READONLY_CONNECTOR_DRYRUN_READY"
    assert seal["write_route_count"] == 0
    assert seal["sealed_step_count"] >= 7


def test_p89_safety_flags() -> None:
    seal = build_local_mvp_seal()
    assert seal["sheet_write"] is False
    assert seal["apps_script_execution"] is False
    assert seal["clasp_push"] is False
    assert seal["broker_execution"] is False
    assert seal["order_execution"] is False
    assert seal["auto_sizing_execution"] is False
    assert seal["google_rest_local_diag"] is False
    assert seal["live_google_api_call"] is False


def test_p89_markdown_contains_seal_and_next() -> None:
    markdown = render_local_mvp_seal_markdown(build_local_mvp_seal())
    assert "P89 Local MVP Seal" in markdown
    assert "OK_P89_LOCAL_MVP_SEALED" in markdown
    assert "P90_GOOGLE_SHEETS_READONLY_CONNECTOR_LIVE_DECISION_OR_STOP" in markdown
    assert "NO_LIVE_GOOGLE_API_CALL" in markdown


def test_p89_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_local_mvp_seal(tmp_path)
    assert result["status"] == "OK_P89_LOCAL_MVP_SEALED"
    payload = json.loads((tmp_path / "P89_LOCAL_MVP_SEAL.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "P89_LOCAL_MVP_SEAL.md").read_text(encoding="utf-8")
    assert payload["status"] == "OK_P89_LOCAL_MVP_SEALED"
    assert "P89 Local MVP Seal" in markdown
