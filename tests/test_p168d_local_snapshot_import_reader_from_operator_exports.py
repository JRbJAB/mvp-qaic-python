from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p168d_local_snapshot_import_reader_from_operator_exports import (
    detect_csv_shape,
    build_outputs,
    discover_latest_p168c_export,
    normalize_manifest_rows,
    validate_manifest_rows,
)


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _manifest_rows() -> list[dict[str, str]]:
    return [
        {
            "snapshot_id": "PENDING_OPERATOR_EXPORT",
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "spreadsheet_id": "sheet-1",
            "spreadsheet_title": "MVP",
            "tab_name": "CONFIG",
            "bounded_range": "A1:D100",
            "local_file": "CONFIG.csv",
            "file_type": "CSV_OR_XLSX",
            "row_count": "PENDING",
            "column_count": "PENDING",
            "captured_at": "2026-06-23T00:00:00Z",
            "checksum_sha256": "PENDING",
            "operator_review_status": "PENDING_EXPORT",
        },
        {
            "snapshot_id": "PENDING_OPERATOR_EXPORT",
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "spreadsheet_id": "sheet-1",
            "spreadsheet_title": "MVP",
            "tab_name": "PROMPT_QUEUE",
            "bounded_range": "A1:Z500",
            "local_file": "PROMPT_QUEUE.csv",
            "file_type": "CSV_OR_XLSX",
            "row_count": "PENDING",
            "column_count": "PENDING",
            "captured_at": "2026-06-23T00:00:00Z",
            "checksum_sha256": "PENDING",
            "operator_review_status": "PENDING_EXPORT",
        },
    ]


def _seed_p168c_export(
    root: Path,
    name: str = "P168C_SHEETS_READONLY_EXPORT_IMPORT_OR_API_BINDING_20260623_020202",
    hierarchy_locked: bool = True,
) -> Path:
    export = root / "05_EXPORTS" / name
    export.mkdir(parents=True)
    (export / "P168C_SUMMARY.json").write_text(
        json.dumps(
            {
                "hierarchy_locked": hierarchy_locked,
                "preferred_path_now": "LOCAL_EXPORT_IMPORT_FIRST",
                "google_sheets_write": False,
                "live_google_api_call_from_python": False,
            }
        ),
        encoding="utf-8",
    )
    _write_csv(export / "P168C_EXPORT_IMPORT_MANIFEST_TEMPLATE.csv", _manifest_rows())
    return export


def test_discover_latest_p168c_export_is_deterministic_by_name(tmp_path: Path) -> None:
    _seed_p168c_export(
        tmp_path, "P168C_SHEETS_READONLY_EXPORT_IMPORT_OR_API_BINDING_20260623_010101"
    )
    _seed_p168c_export(
        tmp_path, "P168C_SHEETS_READONLY_EXPORT_IMPORT_OR_API_BINDING_20260623_020202"
    )
    assert discover_latest_p168c_export(tmp_path).name.endswith("020202")  # type: ignore[union-attr]


def test_normalize_manifest_rows_creates_stable_snapshot_ids() -> None:
    rows = normalize_manifest_rows(_manifest_rows())
    assert rows[0]["snapshot_id"].startswith("P168D_CONFIG")
    assert rows[1]["snapshot_id"].startswith("P168D_PROMPT_QUEUE")


def test_detect_csv_shape_counts_rows_and_columns(tmp_path: Path) -> None:
    data = tmp_path / "sample.csv"
    data.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    assert detect_csv_shape(data) == (3, 2)


def test_validate_manifest_rows_waits_when_files_missing(tmp_path: Path) -> None:
    rows = normalize_manifest_rows(_manifest_rows())
    validation = validate_manifest_rows(rows, tmp_path / "exports")
    assert all(row["file_exists"] == "False" for row in validation)
    assert all(row["import_ready"] == "NO" for row in validation)


def test_validate_manifest_rows_prepares_csv_import_queue(tmp_path: Path) -> None:
    operator_dir = tmp_path / "operator"
    operator_dir.mkdir()
    (operator_dir / "CONFIG.csv").write_text("key,value\na,b\n", encoding="utf-8")
    rows = normalize_manifest_rows(_manifest_rows()[:1])
    validation = validate_manifest_rows(rows, operator_dir)
    assert validation[0]["file_exists"] == "True"
    assert validation[0]["reader_status"] == "CSV_READ_OK"
    assert validation[0]["row_count_detected"] == "2"
    assert validation[0]["column_count_detected"] == "2"
    assert validation[0]["checksum_sha256_detected"]
    assert validation[0]["import_ready"] == "YES"


def test_build_outputs_waits_for_operator_exports_without_blockers(tmp_path: Path) -> None:
    _seed_p168c_export(tmp_path)
    export = build_outputs(tmp_path)
    summary = json.loads((export / "P168D_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["hierarchy_locked"] is True
    assert summary["manifest_required_count"] == 2
    assert summary["files_found_count"] == 0
    assert summary["import_ready_count"] == 0
    assert summary["blocker_count"] == 0
    assert summary["google_sheets_write"] is False
    assert summary["live_google_api_call_from_python"] is False
    assert (export / "P168D_OPERATOR_EXPORT_MANIFEST_TEMPLATE.csv").exists()
    assert (export / "P168D_LOCAL_FILE_VALIDATION.csv").exists()


def test_build_outputs_reads_operator_manifest_and_file(tmp_path: Path) -> None:
    _seed_p168c_export(tmp_path)
    operator_dir = tmp_path / "operator"
    operator_dir.mkdir()
    _write_csv(operator_dir / "P168D_OPERATOR_EXPORT_MANIFEST.csv", _manifest_rows()[:1])
    (operator_dir / "CONFIG.csv").write_text("key,value\na,b\n", encoding="utf-8")
    export = build_outputs(tmp_path, operator_export_dir=operator_dir)
    summary = json.loads((export / "P168D_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["manifest_source"] == "OPERATOR_MANIFEST"
    assert summary["files_found_count"] == 1
    assert summary["import_ready_count"] == 1
    assert summary["blocker_count"] == 0


def test_build_outputs_blocks_when_p168c_hierarchy_missing(tmp_path: Path) -> None:
    _seed_p168c_export(tmp_path, hierarchy_locked=False)
    export = build_outputs(tmp_path)
    summary = json.loads((export / "P168D_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["blocker_count"] >= 1
    assert "P168C_HIERARCHY_NOT_LOCKED" in summary["blockers"]
