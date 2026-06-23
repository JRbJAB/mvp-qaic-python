from pathlib import Path

from mvp_qaic_py.p168f_operator_export_capture_or_wait import (
    DROPZONE_RELATIVE,
    build_capture,
    inspect_dropzone,
    latest_export_dir,
    required_exports,
)


def test_required_exports_are_five_and_mvp_only() -> None:
    rows = required_exports()
    assert len(rows) == 5
    assert all(row.source_domain == "MVP_QAIC_PY" for row in rows)
    assert all(row.export_format == "CSV_UTF8" for row in rows)


def test_inspect_dropzone_waits_when_files_are_missing(tmp_path: Path) -> None:
    dropzone, statuses = inspect_dropzone(tmp_path)
    assert dropzone == tmp_path / DROPZONE_RELATIVE
    assert len(statuses) == 5
    assert sum(1 for status in statuses if status.found) == 0
    assert {status.validation_status for status in statuses} == {"WAITING_OPERATOR_EXPORT"}


def test_inspect_dropzone_detects_existing_non_empty_file(tmp_path: Path) -> None:
    dropzone = tmp_path / DROPZONE_RELATIVE
    dropzone.mkdir(parents=True)
    first = required_exports()[0]
    (dropzone / first.expected_file_name).write_text("key,value\nmode,TEST\n", encoding="utf-8")

    _, statuses = inspect_dropzone(tmp_path)

    found = [status for status in statuses if status.found]
    assert len(found) == 1
    assert found[0].snapshot_id == first.snapshot_id
    assert found[0].validation_status == "FOUND_PENDING_SCHEMA_VALIDATION"


def test_build_capture_creates_waiting_outputs_without_cache(tmp_path: Path) -> None:
    summary = build_capture(tmp_path, stamp="20260623_010203")

    assert summary["status"] == "P168F_OPERATOR_EXPORT_CAPTURE_READY_WAIT_OPERATOR_FILES_READONLY"
    assert summary["hierarchy_locked"] is True
    assert summary["required_snapshot_count"] == 5
    assert summary["files_found_count"] == 0
    assert summary["ready_snapshot_count"] == 0
    assert summary["waiting_snapshot_count"] == 5
    assert summary["cache_files_created_count"] == 0
    assert summary["google_sheets_write"] is False
    assert summary["live_google_api_call_from_python"] is False
    assert summary["blocker_count"] == 0

    output_dir = Path(str(summary["output_dir"]))
    assert (output_dir / "P168F_REQUIRED_EXPORTS_MANIFEST.csv").exists()
    assert (output_dir / "P168F_LOCAL_EXPORT_FILE_STATUS.csv").exists()
    assert (output_dir / "P168F_OPERATOR_EXPORT_CAPTURE_CHECKLIST.csv").exists()
    assert (output_dir / "P168F_OPERATOR_EXPORT_INSTRUCTIONS.md").exists()
    assert (output_dir / "P168F_CAPTURE_STATUS_REPORT.md").exists()
    assert (output_dir / "P168F_SUMMARY.json").exists()


def test_build_capture_counts_existing_file_and_still_readonly(tmp_path: Path) -> None:
    dropzone = tmp_path / DROPZONE_RELATIVE
    dropzone.mkdir(parents=True)
    (dropzone / "MVP_QAIC_CONFIG.csv").write_text("key,value\nmode,TEST\n", encoding="utf-8")

    summary = build_capture(tmp_path, stamp="20260623_010204")

    assert summary["files_found_count"] == 1
    assert summary["ready_snapshot_count"] == 1
    assert summary["waiting_snapshot_count"] == 4
    assert summary["cache_files_created_count"] == 0
    assert summary["runtime_prompt_modified"] is False
    assert summary["apply_allowed"] is False


def test_latest_export_dir_is_deterministic_by_name(tmp_path: Path) -> None:
    older = (
        tmp_path
        / "05_EXPORTS"
        / "P168E_LOCAL_CACHE_BUILD_FROM_VALIDATED_SNAPSHOTS_OR_WAIT_20260623_010101"
    )
    newer = (
        tmp_path
        / "05_EXPORTS"
        / "P168E_LOCAL_CACHE_BUILD_FROM_VALIDATED_SNAPSHOTS_OR_WAIT_20260623_020202"
    )
    older.mkdir(parents=True)
    newer.mkdir(parents=True)

    result = latest_export_dir(
        tmp_path, "P168E_LOCAL_CACHE_BUILD_FROM_VALIDATED_SNAPSHOTS_OR_WAIT_"
    )

    assert result is not None
    assert result.name.endswith("020202")


def test_dropzone_readme_is_created(tmp_path: Path) -> None:
    summary = build_capture(tmp_path, stamp="20260623_010205")
    readme = Path(str(summary["dropzone_dir"])) / "README_P168F_DROPZONE.md"

    assert readme.exists()
    text = readme.read_text(encoding="utf-8")
    assert "MVP_QAIC_CONFIG.csv" in text
    assert "No Google Sheets write" in text or "Do not write back" in text
