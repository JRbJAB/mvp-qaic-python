from __future__ import annotations

from mvp_qaic_py.webapp_canonical_binding_admin import (
    BINDING_ADMIN_SAFETY,
    build_admin_status,
    build_binding_admin_files,
    build_canonical_binding_contract,
    render_admin_monitor_html,
    summarize_binding_admin,
    validate_no_canonical_index_generated,
    write_binding_admin_files,
)


def test_p107_r1_canonical_binding_declares_index_do_not_overwrite() -> None:
    contract = build_canonical_binding_contract(now_utc="2026-06-22T00:00:00Z")

    assert contract["status"] == "CANONICAL_BINDING_READY"
    assert contract["canonical_ui"]["file_name"] == "Index.html"
    assert contract["canonical_ui"]["policy"] == "DO_NOT_OVERWRITE_FROM_PYTHON"
    assert "index.html" in contract["forbidden_generated_files"]
    assert "admin/ADMIN_MONITOR.html" in contract["allowed_generated_files"]


def test_p107_r1_admin_status_has_gates_and_safety() -> None:
    status = build_admin_status(now_utc="2026-06-22T00:00:00Z")
    gate_ids = {gate["gate_id"] for gate in status["gates"]}

    assert status["status"] == "ADMIN_MONITOR_READY"
    assert "canonical_index_not_generated" in gate_ids
    assert "admin_monitor_generated" in gate_ids
    assert status["safety"]["no_public_deploy"] is True


def test_p107_r1_builds_admin_html_but_no_index_html() -> None:
    files = build_binding_admin_files(now_utc="2026-06-22T00:00:00Z")
    validation = validate_no_canonical_index_generated(files)

    assert validation["status"] == "PASS"
    assert "admin/ADMIN_MONITOR.html" in files
    assert "index.html" not in files
    assert "Index.html" not in files
    assert "WEBAPP_BINDING_CONTRACT.md" in files


def test_p107_r1_admin_html_mentions_not_replacing_canonical_index() -> None:
    html = render_admin_monitor_html(build_admin_status(now_utc="2026-06-22T00:00:00Z"))

    assert "Admin Monitor" in html
    assert "ne remplace pas l'Index.html WebApp validé" in html
    assert "DO_NOT_OVERWRITE_FROM_PYTHON" in html


def test_p107_r1_write_binding_admin_files_to_tmp_path(tmp_path) -> None:
    written = write_binding_admin_files(tmp_path, now_utc="2026-06-22T00:00:00Z")
    summary = summarize_binding_admin(tmp_path, written)

    assert summary["file_count"] == 8
    assert summary["has_admin_monitor"] is True
    assert summary["has_binding_contract"] is True
    assert summary["has_webapp_pack"] is True
    assert summary["has_no_index_html"] is True
    assert (tmp_path / "admin" / "ADMIN_MONITOR.html").exists()
    assert not (tmp_path / "index.html").exists()


def test_p107_r1_safety_flags_locked() -> None:
    assert BINDING_ADMIN_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "canonical_webapp_index_do_not_overwrite": True,
        "admin_html_allowed": True,
        "no_index_html_generation": True,
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
        "local_admin_monitor_only": True,
    }
