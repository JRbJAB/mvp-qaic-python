from __future__ import annotations

import json

from mvp_qaic_py.webapp_static_preview_export import (
    STATIC_PREVIEW_SAFETY,
    build_static_preview_bundle,
    build_static_preview_files,
    render_index_html,
    summarize_static_preview,
    write_static_preview_files,
)


def test_p106_static_preview_bundle_contains_public_scope_and_safety() -> None:
    bundle = build_static_preview_bundle(now_utc="2026-06-22T00:00:00Z")

    assert bundle["scope"]["mvp"] == "lexique_webapp_prompts_methods_benchmark_public"
    assert bundle["scope"]["qaic_private"] == "backend_quant_risk_revolutx_execution_locked"
    assert bundle["safety"]["no_revolutx_real_access"] is True
    assert bundle["safety"]["no_public_deploy"] is True
    assert len(bundle["routes"]) >= 5
    assert len(bundle["sections"]) >= 8


def test_p106_render_index_html_has_required_public_sections() -> None:
    html = render_index_html(build_static_preview_bundle(now_utc="2026-06-22T00:00:00Z"))

    assert "MVP QAIC — WebApp Preview" in html
    assert "Benchmark prompt" in html
    assert "Lexique context" in html
    assert "Méthodes context" in html
    assert "no RevolutX réel" in html


def test_p106_build_static_preview_files_contains_expected_files() -> None:
    files = build_static_preview_files(now_utc="2026-06-22T00:00:00Z")

    assert set(files) == {
        "index.html",
        "data/webapp_pack.json",
        "data/context_pack.json",
        "data/prompt_payload.json",
        "preview_manifest.json",
        "README_PREVIEW.md",
    }

    manifest = json.loads(files["preview_manifest.json"])
    assert manifest["file_count" if "file_count" in manifest else "route_count"]


def test_p106_write_static_preview_files_to_tmp_path(tmp_path) -> None:
    written = write_static_preview_files(tmp_path, now_utc="2026-06-22T00:00:00Z")
    summary = summarize_static_preview(tmp_path, written)

    assert summary["file_count"] == 6
    assert summary["has_index"] is True
    assert summary["has_webapp_pack"] is True
    assert summary["has_context_pack"] is True
    assert summary["has_prompt_payload"] is True
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "data" / "webapp_pack.json").exists()


def test_p106_static_preview_safety_flags_locked() -> None:
    assert STATIC_PREVIEW_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "no_revolutx_real_access": True,
        "no_broker": True,
        "no_order": True,
        "no_cancel": True,
        "no_replace_order": True,
        "no_auto_sizing": True,
        "no_secret_log": True,
        "no_sheet_write": True,
        "no_apps_script_execution": True,
        "no_clasp": True,
        "no_public_deploy": True,
        "local_static_preview_only": True,
    }
