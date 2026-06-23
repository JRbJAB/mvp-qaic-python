from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p143b_data_preview_source_expansion import (
    STATUS_BOUND,
    SourceExpansionRequest,
    build_expanded_binding,
    normalize,
    run_expansion,
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
                "primary_columns": ["prompt_id", "raw_prompt_text"],
            },
            {
                "page_id": "runtime",
                "title": "🤖 AI_RUNTIME_REFERENCE",
                "route": "/cockpit/runtime",
                "domain": "contracts",
                "primary_columns": ["runtime_id"],
            },
        ],
    }


def _root(tmp_path: Path) -> Path:
    root = tmp_path / "exports"
    root.mkdir()
    with (root / "PROMPT_LIBRARY.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["prompt_id", "raw_prompt_text"])
        writer.writeheader()
        writer.writerow({"prompt_id": "p1", "raw_prompt_text": "hello"})
    return root


def test_normalize():
    assert normalize("📘 PROMPT_LIBRARY") == "prompt_library"


def test_build_expanded_binding_matches_and_fallbacks(tmp_path: Path):
    binding = build_expanded_binding(_spec(), _root(tmp_path), max_preview_rows=5, max_sources=50)
    assert binding["status"] == STATUS_BOUND
    assert binding["bound_page_count"] == 2
    assert binding["csv_match_page_count"] == 1
    assert binding["metadata_fallback_page_count"] == 1
    assert binding["safety"]["google_sheets_write"] is False


def test_run_expansion_writes_outputs(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(_spec()), encoding="utf-8")
    out = tmp_path / "out"
    binding = run_expansion(
        SourceExpansionRequest(
            p142_spec_path=spec_path,
            source_root=_root(tmp_path),
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
            max_preview_rows=5,
            max_sources=50,
        )
    )
    assert binding["status"] == STATUS_BOUND
    assert (out / "P143B_DATA_PREVIEW_EXPANDED_BINDING.json").exists()
    assert (out / "P143B_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(_spec()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p143b_data_preview_source_expansion",
            "--p142-spec",
            str(spec_path),
            "--source-root",
            str(_root(tmp_path)),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_BOUND in completed.stdout
    assert "google_sheets_write=false" in completed.stdout
