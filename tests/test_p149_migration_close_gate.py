from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p149_migration_close_gate import (
    REQUIRED_EXPORT_PREFIXES,
    STATUS_READY,
    CloseGateRequest,
    build_close_report,
    collect_evidence,
    run_close_gate,
)


def _strategy():
    return {
        "status": "P148_SYNC_STRATEGY_READONLY_RENDERED",
        "p149_readiness": {"migration_close_gate_ready": True},
        "policy": {
            "future_sheet_write_requires_explicit_go": True,
            "write_back_allowed_now": False,
        },
        "safety": {"google_sheets_write": False},
    }


def _exports_root(tmp_path: Path) -> Path:
    root = tmp_path / "exports"
    root.mkdir()
    for prefix in REQUIRED_EXPORT_PREFIXES:
        folder = root / f"{prefix}20260623"
        folder.mkdir()
        (folder / "evidence.txt").write_text("ok", encoding="utf-8")
    return root


def test_build_close_report_ready(tmp_path: Path):
    evidence = collect_evidence(_exports_root(tmp_path))
    report = build_close_report(_strategy(), evidence)
    assert report["status"] == STATUS_READY
    assert report["migration_close_ready"] is True
    assert report["blocker_count"] == 0
    assert report["safety"]["google_sheets_write"] is False


def test_run_close_gate_writes_outputs(tmp_path: Path):
    strategy_path = tmp_path / "p148.json"
    strategy_path.write_text(json.dumps(_strategy()), encoding="utf-8")
    out = tmp_path / "out"
    report = run_close_gate(
        CloseGateRequest(
            p148_strategy_path=strategy_path,
            exports_root=_exports_root(tmp_path),
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert report["status"] == STATUS_READY
    assert (out / "P149_MIGRATION_CLOSE_GATE_REPORT.json").exists()
    assert (out / "P149_MIGRATION_TIMELINE.csv").exists()
    assert (out / "P149_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    strategy_path = tmp_path / "p148.json"
    strategy_path.write_text(json.dumps(_strategy()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p149_migration_close_gate",
            "--p148-strategy",
            str(strategy_path),
            "--exports-root",
            str(_exports_root(tmp_path)),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_READY in completed.stdout
    assert "migration_close_ready=true" in completed.stdout
