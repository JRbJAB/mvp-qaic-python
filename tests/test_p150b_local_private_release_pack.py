from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p150b_local_private_release_pack import (
    RELEASE_PREFIXES,
    STATUS_READY,
    ReleasePackRequest,
    build_manifest,
    collect_release_evidence,
    run_release_pack,
)


def _selector():
    return {
        "status": "P150_PUBLIC_PREP_SELECTOR_OR_STOP_READY_READONLY",
        "recommended_next": "P150B_LOCAL_PRIVATE_RELEASE_PACK",
        "blocker_count": 0,
        "safety": {"google_sheets_write": False, "public_deploy": False},
    }


def _exports_root(tmp_path: Path) -> Path:
    root = tmp_path / "exports"
    root.mkdir()
    for prefix in RELEASE_PREFIXES:
        folder = root / f"{prefix}20260623"
        folder.mkdir()
        (folder / f"{prefix.rstrip('_')}_SUMMARY.json").write_text("{}", encoding="utf-8")
    return root


def test_build_manifest_ready(tmp_path: Path):
    evidence = collect_release_evidence(_exports_root(tmp_path))
    manifest = build_manifest(_selector(), evidence)
    assert manifest["status"] == STATUS_READY
    assert manifest["blocker_count"] == 0
    assert manifest["safety"]["google_sheets_write"] is False
    assert manifest["safety"]["public_deploy"] is False


def test_run_release_pack_writes_outputs_and_zip(tmp_path: Path):
    selector_path = tmp_path / "selector.json"
    selector_path.write_text(json.dumps(_selector()), encoding="utf-8")
    out = tmp_path / "out"
    manifest = run_release_pack(
        ReleasePackRequest(
            p150_selector_path=selector_path,
            exports_root=_exports_root(tmp_path),
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert manifest["status"] == STATUS_READY
    assert (out / "P150B_RELEASE_MANIFEST.json").exists()
    assert (out / "P150B_SUMMARY.json").exists()
    assert (out / "P150B_LOCAL_PRIVATE_RELEASE_PACK.zip").exists()


def test_cli(tmp_path: Path):
    selector_path = tmp_path / "selector.json"
    selector_path.write_text(json.dumps(_selector()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p150b_local_private_release_pack",
            "--p150-selector",
            str(selector_path),
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
    assert "public_deploy=false" in completed.stdout
