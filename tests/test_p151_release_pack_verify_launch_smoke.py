from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from mvp_qaic_py.p151_release_pack_verify_launch_smoke import (
    REQUIRED_EVIDENCE_PREFIXES,
    REQUIRED_ZIP_ENTRIES,
    STATUS_READY,
    VerifyRequest,
    build_report,
    run_verify,
)


def _manifest():
    return {
        "status": "P150B_LOCAL_PRIVATE_RELEASE_PACK_READY",
        "release_name": "MVP_QAIC_LOCAL_PRIVATE_PROMPT_COCKPIT_RELEASE_P150B",
        "blocker_count": 0,
        "safety": {"google_sheets_write": False, "public_deploy": False, "broker": False},
    }


def _release_zip(tmp_path: Path) -> Path:
    path = tmp_path / "release.zip"
    with ZipFile(path, "w") as archive:
        for entry in REQUIRED_ZIP_ENTRIES:
            archive.writestr(entry, "ok")
        for prefix in REQUIRED_EVIDENCE_PREFIXES:
            archive.writestr(prefix + "evidence.json", "{}")
    return path


def _exports_root(tmp_path: Path) -> Path:
    root = tmp_path / "exports"
    folder = root / "P147_OPERATOR_POLISH_20260623"
    folder.mkdir(parents=True)
    (folder / "P147_NICEGUI_OPERATOR_POLISH_APP.py").write_text("print('ok')", encoding="utf-8")
    return root


def test_build_report_ready(tmp_path: Path):
    zip_path = _release_zip(tmp_path)
    with ZipFile(zip_path, "r") as archive:
        entries = sorted(archive.namelist())
    report = build_report(_manifest(), entries, _exports_root(tmp_path), zip_path)
    assert report["status"] == STATUS_READY
    assert report["launch_smoke_ready"] is True
    assert report["blocker_count"] == 0
    assert report["safety"]["google_sheets_write"] is False


def test_run_verify_writes_outputs(tmp_path: Path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_manifest()), encoding="utf-8")
    out = tmp_path / "out"
    report = run_verify(
        VerifyRequest(
            p150b_manifest_path=manifest_path,
            release_zip_path=_release_zip(tmp_path),
            exports_root=_exports_root(tmp_path),
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert report["status"] == STATUS_READY
    assert (out / "P151_RELEASE_PACK_VERIFY_REPORT.json").exists()
    assert (out / "P151_LOCAL_LAUNCH_SMOKE.ps1").exists()
    assert (out / "P151_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_manifest()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p151_release_pack_verify_launch_smoke",
            "--p150b-manifest",
            str(manifest_path),
            "--release-zip",
            str(_release_zip(tmp_path)),
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
    assert "server_launch_executed=false" in completed.stdout
