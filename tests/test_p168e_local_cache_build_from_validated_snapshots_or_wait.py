from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p168e_local_cache_build_from_validated_snapshots_or_wait import (
    build_outputs,
    cache_one_snapshot,
    discover_latest_p168d_export,
    read_csv_snapshot,
    safe_snapshot_filename,
)


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _seed_p168d_export(
    root: Path,
    name: str = "P168D_LOCAL_SNAPSHOT_IMPORT_READER_FROM_OPERATOR_EXPORTS_20260623_020202",
    *,
    hierarchy_locked: bool = True,
    ready: bool = False,
    source_file: Path | None = None,
) -> Path:
    export = root / "05_EXPORTS" / name
    export.mkdir(parents=True)
    (export / "P168D_SUMMARY.json").write_text(
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
    waiting_rows = [
        {
            "snapshot_id": "P168D_CONFIG_001",
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "tab_name": "CONFIG",
            "bounded_range": "A1:D100",
            "local_file": "CONFIG.csv",
            "resolved_path": str(root / "operator" / "CONFIG.csv"),
            "file_exists": "False",
            "file_type": "CSV_OR_XLSX",
            "reader_status": "WAITING_FOR_OPERATOR_EXPORT",
            "row_count_detected": "",
            "column_count_detected": "",
            "checksum_sha256_detected": "",
            "operator_review_status": "PENDING_EXPORT",
            "import_ready": "NO",
            "issue_code": "MISSING_LOCAL_FILE",
            "issue_message": "Operator export is required.",
        }
    ]
    ready_rows: list[dict[str, str]] = []
    if ready:
        assert source_file is not None
        waiting_rows = []
        ready_rows = [
            {
                "snapshot_id": "P168D_CONFIG_001",
                "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
                "spreadsheet_id": "sheet-1",
                "spreadsheet_title": "MVP",
                "tab_name": "CONFIG",
                "bounded_range": "A1:D100",
                "local_file": source_file.name,
                "resolved_path": str(source_file),
                "file_type": "CSV",
                "row_count_detected": "3",
                "column_count_detected": "2",
                "checksum_sha256_detected": "abc",
                "import_stage": "READY_FOR_LOCAL_CACHE_IMPORT",
                "write_allowed": "NO",
            }
        ]
    _write_csv(
        export / "P168D_LOCAL_FILE_VALIDATION.csv",
        waiting_rows
        or [
            {
                "snapshot_id": "P168D_CONFIG_001",
                "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
                "tab_name": "CONFIG",
                "bounded_range": "A1:D100",
                "local_file": source_file.name if source_file else "CONFIG.csv",
                "resolved_path": str(source_file)
                if source_file
                else str(root / "operator" / "CONFIG.csv"),
                "file_exists": "True" if source_file else "False",
                "file_type": "CSV",
                "reader_status": "CSV_READ_OK" if source_file else "WAITING_FOR_OPERATOR_EXPORT",
                "row_count_detected": "3" if source_file else "",
                "column_count_detected": "2" if source_file else "",
                "checksum_sha256_detected": "abc" if source_file else "",
                "operator_review_status": "PENDING_EXPORT",
                "import_ready": "YES" if source_file else "NO",
                "issue_code": "",
                "issue_message": "",
            }
        ],
    )
    if ready_rows:
        _write_csv(export / "P168D_READY_IMPORT_QUEUE.csv", ready_rows)
    else:
        with (export / "P168D_READY_IMPORT_QUEUE.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "snapshot_id",
                    "source_key",
                    "spreadsheet_id",
                    "spreadsheet_title",
                    "tab_name",
                    "bounded_range",
                    "local_file",
                    "resolved_path",
                    "file_type",
                    "row_count_detected",
                    "column_count_detected",
                    "checksum_sha256_detected",
                    "import_stage",
                    "write_allowed",
                ],
            )
            writer.writeheader()
    return export


def test_discover_latest_p168d_export_is_deterministic_by_name(tmp_path: Path) -> None:
    _seed_p168d_export(
        tmp_path, "P168D_LOCAL_SNAPSHOT_IMPORT_READER_FROM_OPERATOR_EXPORTS_20260623_010101"
    )
    _seed_p168d_export(
        tmp_path, "P168D_LOCAL_SNAPSHOT_IMPORT_READER_FROM_OPERATOR_EXPORTS_20260623_020202"
    )
    assert discover_latest_p168d_export(tmp_path).name.endswith("020202")  # type: ignore[union-attr]


def test_safe_snapshot_filename_removes_unsafe_chars() -> None:
    assert safe_snapshot_filename("CONFIG / A1:D100") == "CONFIG___A1_D100"


def test_read_csv_snapshot_counts_data_rows_and_columns(tmp_path: Path) -> None:
    csv_file = tmp_path / "CONFIG.csv"
    csv_file.write_text("key,value\na,b\nc,d\n", encoding="utf-8")
    headers, records, row_count, column_count = read_csv_snapshot(csv_file)
    assert headers == ["key", "value"]
    assert len(records) == 2
    assert row_count == 2
    assert column_count == 2


def test_cache_one_snapshot_creates_json_cache(tmp_path: Path) -> None:
    source = tmp_path / "CONFIG.csv"
    source.write_text("key,value\na,b\n", encoding="utf-8")
    row = {
        "snapshot_id": "P168D_CONFIG_001",
        "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
        "tab_name": "CONFIG",
        "bounded_range": "A1:D100",
        "resolved_path": str(source),
        "file_type": "CSV",
    }
    index, validation = cache_one_snapshot(row, tmp_path / "cache")
    assert index["cache_status"] == "LOCAL_CACHE_CREATED"
    assert validation["cache_file_created"] == "True"
    assert Path(index["cache_file"]).exists()


def test_build_outputs_waits_without_validated_exports(tmp_path: Path) -> None:
    _seed_p168d_export(tmp_path)
    export = build_outputs(tmp_path)
    summary = json.loads((export / "P168E_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["hierarchy_locked"] is True
    assert summary["ready_snapshot_count"] == 0
    assert summary["waiting_snapshot_count"] == 1
    assert summary["cache_files_created_count"] == 0
    assert summary["blocker_count"] == 0
    assert summary["google_sheets_write"] is False
    assert summary["live_google_api_call_from_python"] is False
    assert (export / "P168E_WAITING_EXPORTS_CHECKLIST.csv").exists()


def test_build_outputs_creates_cache_from_ready_csv(tmp_path: Path) -> None:
    source = tmp_path / "operator" / "CONFIG.csv"
    source.parent.mkdir()
    source.write_text("key,value\na,b\nc,d\n", encoding="utf-8")
    _seed_p168d_export(tmp_path, ready=True, source_file=source)
    export = build_outputs(tmp_path)
    summary = json.loads((export / "P168E_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["ready_snapshot_count"] == 1
    assert summary["cache_files_created_count"] == 1
    assert summary["blocker_count"] == 0
    index_rows = list(
        csv.DictReader((export / "P168E_LOCAL_CACHE_INDEX.csv").open(encoding="utf-8"))
    )
    assert index_rows[0]["cache_status"] == "LOCAL_CACHE_CREATED"
    assert Path(index_rows[0]["cache_file"]).exists()


def test_build_outputs_blocks_when_p168d_hierarchy_missing(tmp_path: Path) -> None:
    _seed_p168d_export(tmp_path, hierarchy_locked=False)
    export = build_outputs(tmp_path)
    summary = json.loads((export / "P168E_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["blocker_count"] >= 1
    assert "P168D_HIERARCHY_NOT_LOCKED" in summary["blockers"]
