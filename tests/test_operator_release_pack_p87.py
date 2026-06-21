from __future__ import annotations

import json

from mvp_qaic_py.release.operator_release_pack import (
    build_operator_release_pack,
    export_operator_release_pack,
    render_operator_release_pack_markdown,
)


def test_p87_release_pack_ready() -> None:
    pack = build_operator_release_pack()
    assert pack["status"] == "OK_P87_OPERATOR_RELEASE_PACK_READY"
    assert pack["gate_status"] == "OK_P86_OPERATOR_DECISION_GATE_GO"
    assert pack["pack_status"] == "OK_P85A_OPERATOR_OUTPUT_PACK_READY"
    assert pack["bridge_status"] == "OK_P83B_LOCAL_BRIDGE_DRYRUN_MODULE_READY"
    assert pack["contract_status"] == "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
    assert pack["write_route_count"] == 0
    assert pack["human_approval_required_count"] == 1


def test_p87_safety_flags() -> None:
    pack = build_operator_release_pack()
    assert pack["sheet_write"] is False
    assert pack["apps_script_execution"] is False
    assert pack["clasp_push"] is False
    assert pack["broker_execution"] is False
    assert pack["order_execution"] is False
    assert pack["auto_sizing_execution"] is False
    assert pack["google_rest_local_diag"] is False


def test_p87_blocks_invalid_decision() -> None:
    pack = build_operator_release_pack(decision="APPEND_TO_SHEET")
    assert pack["status"] == "BLOCKED_P87_RELEASE_PACK"
    assert pack["write_route_count"] == 0


def test_p87_markdown_contains_release_and_gate() -> None:
    markdown = render_operator_release_pack_markdown(build_operator_release_pack())
    assert "P87 Operator Release Pack" in markdown
    assert "OK_P87_OPERATOR_RELEASE_PACK_READY" in markdown
    assert "P86 Operator Decision Gate" in markdown
    assert "NO_SHEET_WRITE" in markdown


def test_p87_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_operator_release_pack(tmp_path)
    assert result["status"] == "OK_P87_OPERATOR_RELEASE_PACK_READY"
    payload = json.loads((tmp_path / "P87_OPERATOR_RELEASE_PACK.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "P87_OPERATOR_RELEASE_PACK.md").read_text(encoding="utf-8")
    assert payload["status"] == "OK_P87_OPERATOR_RELEASE_PACK_READY"
    assert "P87 Operator Release Pack" in markdown
