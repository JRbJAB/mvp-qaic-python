import csv
import json
import subprocess
import sys

from mvp_qaic_py.daily_run_registry import (
    SAFETY_MARKERS,
    DailyRunRegistryRequest,
    build_registry_rows,
    discover_p124_dirs,
    discover_p125_dirs,
    write_daily_run_registry,
)


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _make_p124(exports, name="P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_000000"):
    p124 = exports / name
    p124.mkdir(parents=True)
    _write_json(
        p124 / "P124_INPUT_HELPER_MANIFEST.json",
        {
            "status": "INPUT_HELPER_READY",
            "run_id": "P124-TEST",
            "ready_for_real_gem_manual_test": True,
            "human_review_only": True,
            "no_sheet_write": True,
            "no_auto_apply_gem_response": True,
            "no_order_no_sizing": True,
        },
    )
    return p124


def _make_p125(exports, p124, status="READY_FOR_OPERATOR_REVIEW"):
    p125 = exports / "P125_REAL_GEM_MANUAL_TEST_REVIEW_UX_20260622_000000"
    p125.mkdir(parents=True)
    _write_json(
        p125 / "P125_RUN_MANIFEST.json",
        {
            "status": status,
            "run_id": "P125-TEST",
            "p124_run_dir": str(p124),
            "finding_count": 0,
            "blocker_count": 0,
            "missing_data_count": 0,
            "human_review_only": True,
            "no_sheet_write": True,
            "no_auto_apply_gem_response": True,
            "no_order_no_sizing": True,
            "next": "REAL_GEM_TEST_OR_P126_DAILY_RUN_REGISTRY",
        },
    )
    return p125


def test_p126_discovers_p124_and_p125_dirs(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p124 = _make_p124(exports)
    p125 = _make_p125(exports, p124)
    assert p124 in discover_p124_dirs(exports)
    assert p125 in discover_p125_dirs(exports)


def test_p126_builds_ready_registry_row(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p124 = _make_p124(exports)
    _make_p125(exports, p124)
    rows = build_registry_rows(exports)
    assert len(rows) == 1
    assert rows[0]["decision_status"] == "READY_FOR_OPERATOR_REVIEW"
    assert rows[0]["ready_for_operator_review"] == "true"
    assert rows[0]["no_sheet_write"] == "true"


def test_p126_includes_p124_pending_when_no_p125(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p124(exports)
    rows = build_registry_rows(exports)
    assert len(rows) == 1
    assert rows[0]["decision_status"] == "PENDING_P125_REVIEW"
    assert rows[0]["run_family"] == "P124_PENDING_P125"


def test_p126_writes_csv_json_report_manifest(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p124 = _make_p124(exports)
    _make_p125(exports, p124)
    result = write_daily_run_registry(
        DailyRunRegistryRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )
    assert result["status"] == "RUN_REGISTRY_READY"
    assert result["row_count"] == 1
    assert result["ready_for_operator_review_count"] == 1
    assert (tmp_path / "out" / "P126_DAILY_RUN_REGISTRY.csv").exists()
    assert (tmp_path / "out" / "P126_DAILY_RUN_REGISTRY.json").exists()
    assert (tmp_path / "out" / "P126_RUN_REGISTRY_REPORT.md").exists()
    assert (tmp_path / "out" / "P126_RUN_REGISTRY_MANIFEST.json").exists()


def test_p126_csv_has_expected_fields(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p124 = _make_p124(exports)
    _make_p125(exports, p124)
    write_daily_run_registry(
        DailyRunRegistryRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )
    with (tmp_path / "out" / "P126_DAILY_RUN_REGISTRY.csv").open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["registry_row_id"] == "P126-ROW-0001"
    assert rows[0]["decision_status"] == "READY_FOR_OPERATOR_REVIEW"


def test_p126_cli_generates_registry(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p124 = _make_p124(exports)
    _make_p125(exports, p124)
    output_dir = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.daily_run_registry",
            "--output-dir",
            str(output_dir),
            "--exports-dir",
            str(exports),
            "--run-id",
            "P126-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "RUN_REGISTRY_READY" in completed.stdout
    assert (output_dir / "P126_RUN_REGISTRY_MANIFEST.json").exists()


def test_p126_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "REGISTRY_ONLY",
        "HUMAN_REVIEW_ONLY",
        "NO_INDEX_EDIT",
        "NO_CLASP",
        "NO_APPS_SCRIPT_EXECUTION",
        "NO_SHEET_WRITE",
        "NO_PUBLIC_DEPLOY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_AUTO_SIZING",
        "NO_AUTO_APPLY_GEM_RESPONSE",
        "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    }
    assert required.issubset(set(SAFETY_MARKERS))
