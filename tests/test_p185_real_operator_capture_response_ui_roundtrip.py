from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p185_real_operator_capture_response_ui_roundtrip import (
    build_roundtrip_model,
    export_roundtrip_model,
)


def test_build_roundtrip_model_ready_without_real_files(tmp_path: Path) -> None:
    payload = build_roundtrip_model(tmp_path)

    assert payload["STATUS"] == "OK_P185_REAL_OPERATOR_CAPTURE_RESPONSE_UI_ROUNDTRIP_READY"
    assert payload["roundtrip_ready"] is True
    assert payload["parser_ready"] is True
    assert payload["workflow_stage_count"] == 5
    assert payload["gem_call_executed"] is False
    assert payload["auto_apply_gem_response"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_export_roundtrip_model_counts_files_and_exports(tmp_path: Path) -> None:
    capture_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    response_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    capture_dir.mkdir(parents=True)
    response_dir.mkdir(parents=True)
    (capture_dir / "portfolio.png").write_bytes(b"fake-image")
    (response_dir / "gem_response.json").write_text(
        json.dumps(
            {
                "status": "REVIEW_REQUIRED",
                "image_used": True,
                "reference_currency": "USD",
                "missing_data": [],
                "blockers": ["NO_AUTO_APPLY"],
                "no_order": True,
                "no_sizing": True,
            }
        ),
        encoding="utf-8",
    )
    export_dir = tmp_path / "05_EXPORTS" / "P185_TEST_EXPORT"

    payload = export_roundtrip_model(tmp_path, export_dir=export_dir)

    assert payload["roundtrip_ready"] is True
    assert payload["capture_count"] == 1
    assert payload["response_count"] == 1
    assert payload["parsed_response_count"] == 1
    assert (export_dir / "P185_ROUNDTRIP_MODEL.json").exists()
    assert (export_dir / "P185_SUMMARY.json").exists()
    assert (export_dir / "P185_ROUNDTRIP_REPORT.md").exists()
