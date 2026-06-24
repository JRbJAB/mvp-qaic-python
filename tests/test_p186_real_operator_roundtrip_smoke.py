from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p186_real_operator_roundtrip_smoke import (
    build_p186_roundtrip_smoke,
    create_controlled_roundtrip_inputs,
    export_p186_roundtrip_smoke,
)


def test_create_controlled_roundtrip_inputs_writes_files(tmp_path: Path) -> None:
    payload = create_controlled_roundtrip_inputs(tmp_path)

    assert payload["capture_exists"] is True
    assert payload["response_exists"] is True
    assert Path(payload["capture_path"]).exists()
    assert Path(payload["response_path"]).exists()
    assert payload["parsed_response"]["blocker_count"] == 0
    assert payload["parsed_response"]["has_no_order"] is True
    assert payload["parsed_response"]["has_no_sizing"] is True


def test_build_p186_roundtrip_smoke_ready(tmp_path: Path) -> None:
    payload = build_p186_roundtrip_smoke(tmp_path)

    assert payload["STATUS"] == (
        "OK_P186_REAL_OPERATOR_ROUNDTRIP_SMOKE_WITH_CAPTURE_AND_RESPONSE_READY"
    )
    assert payload["smoke_ready"] is True
    assert payload["capture_count"] == 1
    assert payload["response_count"] == 1
    assert payload["parsed_response_count"] == 1
    assert payload["blocker_count"] == 0
    assert payload["gem_call_executed"] is False
    assert payload["auto_apply_gem_response"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_export_p186_roundtrip_smoke_writes_expected_files(tmp_path: Path) -> None:
    export_dir = tmp_path / "05_EXPORTS" / "P186_TEST_EXPORT"

    payload = export_p186_roundtrip_smoke(tmp_path, export_dir=export_dir)

    assert payload["smoke_ready"] is True
    assert (export_dir / "P186_ROUNDTRIP_SMOKE_RESULT.json").exists()
    assert (export_dir / "P186_SUMMARY.json").exists()
    assert (export_dir / "P186_ROUNDTRIP_SMOKE_REPORT.md").exists()
