from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p143_data_preview_binding_local_readonly import (
    STATUS_BOUND,
    BindingRequest,
    build_binding,
    normalize_name,
    run_binding,
)


def _spec():
    return {
        "status": "P142_UI_FIDELITY_SHELL_RENDERED",
        "pages": [
            {
                "page_id": "library",
                "title": "📘 PROMPT_LIBRARY",
                "route": "/cockpit/library",
                "domain": "library",
            },
            {
                "page_id": "runtime",
                "title": "🤖 AI_RUNTIME_REFERENCE",
                "route": "/cockpit/runtime",
                "domain": "contracts",
            },
        ],
    }


def _csv_root(tmp_path: Path) -> Path:
    root = tmp_path / "csv"
    root.mkdir()
    with (root / "PROMPT_LIBRARY.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["prompt_id", "raw_prompt_text"])
        writer.writeheader()
        writer.writerow({"prompt_id": "p1", "raw_prompt_text": "hello"})
    return root


def test_normalize_name_removes_emoji():
    assert normalize_name("📘 PROMPT_LIBRARY") == "prompt_library"


def test_build_binding_matches_local_csv(tmp_path: Path):
    binding = build_binding(_spec(), _csv_root(tmp_path), max_preview_rows=5)
    assert binding["status"] == STATUS_BOUND
    assert binding["source_csv_count"] == 1
    assert binding["matched_page_count"] == 1
    assert binding["unmatched_page_count"] == 1
    assert binding["bindings"][0]["preview_row_count"] == 1
    assert binding["safety"]["google_sheets_write"] is False


def test_run_binding_writes_outputs(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(_spec()), encoding="utf-8")
    out = tmp_path / "out"
    binding = run_binding(
        BindingRequest(
            p142_spec_path=spec_path,
            source_csv_root=_csv_root(tmp_path),
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
            max_preview_rows=5,
        )
    )
    assert binding["status"] == STATUS_BOUND
    assert (out / "P143_DATA_PREVIEW_BINDING.json").exists()
    assert (out / "P143_NICEGUI_DATA_PREVIEW_APP.py").exists()
    assert (out / "P143_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(_spec()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p143_data_preview_binding_local_readonly",
            "--p142-spec",
            str(spec_path),
            "--source-csv-root",
            str(_csv_root(tmp_path)),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_BOUND in completed.stdout
    assert "google_sheets_write=false" in completed.stdout
