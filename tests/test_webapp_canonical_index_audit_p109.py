from __future__ import annotations

from mvp_qaic_py.webapp_canonical_index_audit import (
    CANONICAL_INDEX_AUDIT_SAFETY,
    build_canonical_index_audit_pack,
    build_patch_plan_requirements,
    classify_index_candidate,
    find_index_candidates,
    render_patch_plan_markdown,
    summarize_canonical_index_audit,
)


def test_p109_classifies_generated_exports_as_not_canonical() -> None:
    result = classify_index_candidate("05_EXPORTS/P106/STATIC_PREVIEW/index.html")

    assert result["candidate_role"] == "generated_export_not_canonical"
    assert result["canonical_score"] == 0
    assert result["allowed_to_edit"] is False


def test_p109_finds_and_dedupes_index_candidates(tmp_path) -> None:
    (tmp_path / "Index.html").write_text("<html></html>", encoding="utf-8")
    (tmp_path / "05_EXPORTS").mkdir()
    (tmp_path / "05_EXPORTS" / "index.html").write_text("<html></html>", encoding="utf-8")

    candidates = find_index_candidates(tmp_path)

    assert len(candidates) == 2
    assert candidates[0]["relative_path"] == "Index.html"
    assert candidates[0]["allowed_to_edit"] is False


def test_p109_audit_ready_when_possible_canonical_found(tmp_path) -> None:
    (tmp_path / "Index.html").write_text("<html></html>", encoding="utf-8")

    audit = build_canonical_index_audit_pack(
        repo_root=tmp_path,
        now_utc="2026-06-22T00:00:00Z",
    )
    summary = summarize_canonical_index_audit(audit)

    assert audit["decision_status"] == "CANONICAL_INDEX_AUDIT_READY"
    assert summary["possible_canonical_count"] == 1
    assert summary["no_index_html_edit"] is True


def test_p109_audit_review_when_no_canonical_found(tmp_path) -> None:
    audit = build_canonical_index_audit_pack(
        repo_root=tmp_path,
        now_utc="2026-06-22T00:00:00Z",
    )

    assert audit["decision_status"] == "REVIEW_REQUIRED"
    assert "NO_CONFIRMED_CANONICAL_INDEX_CANDIDATE_FOUND" in audit["reviews"]


def test_p109_patch_plan_markdown_contains_forbidden_actions(tmp_path) -> None:
    audit = build_canonical_index_audit_pack(
        repo_root=tmp_path,
        now_utc="2026-06-22T00:00:00Z",
    )
    markdown = render_patch_plan_markdown(audit)

    assert "P109" in markdown
    assert "NO_INDEX_HTML_EDIT" in markdown
    assert "EDIT_INDEX_HTML_NOW" in markdown
    assert "PUBLIC_DEPLOY_WITHOUT_APPROVAL" in markdown


def test_p109_requirements_and_safety_flags_locked() -> None:
    requirements = build_patch_plan_requirements()
    ids = {item["requirement_id"] for item in requirements}

    assert "confirm_canonical_index" in ids
    assert "bind_json_data_packs" in ids
    assert CANONICAL_INDEX_AUDIT_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "readonly_audit_only": True,
        "patch_plan_only": True,
        "no_index_html_edit": True,
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
    }
