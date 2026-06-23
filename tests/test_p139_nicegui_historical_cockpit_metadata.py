from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p139_nicegui_historical_cockpit_metadata import (
    STATUS_CAPTURED,
    build_payload,
    quote_sheet_name,
    run_capture,
    CaptureRequest,
)


def _metadata():
    return {
        "spreadsheetId": "sheet123",
        "properties": {"title": "DEV", "locale": "fr_FR", "timeZone": "Europe/Paris"},
        "sheets": [
            {
                "properties": {
                    "sheetId": 1,
                    "title": "📘 PROMPT_LIBRARY",
                    "index": 0,
                    "sheetType": "GRID",
                    "gridProperties": {
                        "rowCount": 100,
                        "columnCount": 20,
                        "frozenRowCount": 1,
                        "frozenColumnCount": 2,
                    },
                },
                "conditionalFormats": [{}, {}],
                "filterViews": [{}],
                "protectedRanges": [{}],
            },
            {
                "properties": {
                    "sheetId": 2,
                    "title": "OTHER",
                    "index": 1,
                    "sheetType": "GRID",
                    "gridProperties": {"rowCount": 10, "columnCount": 3},
                },
            },
        ],
    }


def test_quote_sheet_name_escapes_single_quote():
    assert quote_sheet_name("O'Reilly") == "'O''Reilly'"


def test_build_payload_detects_cockpit_routes_and_safety():
    payload = build_payload(
        _metadata(),
        {"📘 PROMPT_LIBRARY": [["prompt_id", "raw_prompt_text", "status"]]},
        run_id="R",
        generated_at_utc="2026-06-23T00:00:00Z",
        spreadsheet_id="sheet123",
        max_header_rows=5,
        live_read=True,
    )

    assert payload["status"] == STATUS_CAPTURED
    assert payload["live_google_sheets_read"] is True
    assert payload["google_sheets_write"] is False
    assert payload["safety"]["broker"] is False
    assert payload["cockpit_source_tab_count"] == 1
    assert payload["sheets"][0]["detected_column_count"] == 3
    assert payload["sheets"][0]["frozen_column_count"] == 2
    assert payload["nicegui_replica_spec"]["routes"][0]["route"].startswith("/cockpit/")


def test_run_capture_offline_writes_expected_files(tmp_path: Path):
    metadata_path = tmp_path / "metadata.json"
    values_path = tmp_path / "values.json"
    out = tmp_path / "out"
    metadata_path.write_text(json.dumps(_metadata()), encoding="utf-8")
    values_path.write_text(
        json.dumps({"📘 PROMPT_LIBRARY": [["prompt_id", "raw_prompt_text"]]}), encoding="utf-8"
    )

    payload = run_capture(
        CaptureRequest(
            spreadsheet_id="sheet123",
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
            max_header_rows=5,
            repo_root=None,
            live_read=False,
        ),
        metadata_json=metadata_path,
        values_json=values_path,
    )

    assert payload["status"] == STATUS_CAPTURED
    assert (out / "P139_UI_METADATA_PAYLOAD.json").exists()
    assert (out / "P139_SHEET_UI_METADATA.csv").exists()
    assert (out / "P139_NICEGUI_UI_REPLICA_SPEC.md").exists()
    assert (out / "P139_SUMMARY.json").exists()


def test_cli_offline(tmp_path: Path):
    metadata_path = tmp_path / "metadata.json"
    values_path = tmp_path / "values.json"
    out = tmp_path / "out"
    metadata_path.write_text(json.dumps(_metadata()), encoding="utf-8")
    values_path.write_text(json.dumps({"📘 PROMPT_LIBRARY": [["prompt_id"]]}), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p139_nicegui_historical_cockpit_metadata",
            "--output-dir",
            str(out),
            "--metadata-json",
            str(metadata_path),
            "--values-json",
            str(values_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert STATUS_CAPTURED in completed.stdout
    assert "google_sheets_write=false" in completed.stdout
