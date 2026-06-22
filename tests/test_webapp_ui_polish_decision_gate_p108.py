from __future__ import annotations

from mvp_qaic_py.webapp_ui_polish_decision_gate import (
    UI_POLISH_DECISION_SAFETY,
    build_ui_polish_decision_pack,
    build_ui_polish_requirements,
    detect_canonical_index_candidates,
    render_ui_polish_requirements_markdown,
    summarize_ui_polish_decision,
)


def test_p108_detects_canonical_index_candidates_bounded(tmp_path) -> None:
    (tmp_path / "Index.html").write_text("<html></html>", encoding="utf-8")
    (tmp_path / "random.html").write_text("<html></html>", encoding="utf-8")

    candidates = detect_canonical_index_candidates(tmp_path)

    assert len(candidates) == 1
    assert candidates[0]["relative_path"] == "Index.html"
    assert candidates[0]["allowed_to_edit"] is False


def test_p108_requirements_include_binding_and_public_deploy_gate() -> None:
    requirements = build_ui_polish_requirements()
    ids = {item["requirement_id"] for item in requirements}

    assert "ui_shell_preserve_canonical_index" in ids
    assert "bind_data_packs" in ids
    assert "public_deploy_explicit_gate" in ids


def test_p108_decision_pack_review_required_when_index_missing(tmp_path) -> None:
    pack = build_ui_polish_decision_pack(repo_root=tmp_path, now_utc="2026-06-22T00:00:00Z")
    summary = summarize_ui_polish_decision(pack)

    assert pack["decision_status"] == "REVIEW_REQUIRED"
    assert "CANONICAL_INDEX_CANDIDATE_NOT_FOUND_IN_REPO_LOCAL_SCAN" in pack["reviews"]
    assert summary["no_index_html_edit"] is True
    assert summary["no_public_deploy"] is True


def test_p108_decision_pack_ready_when_index_candidate_exists(tmp_path) -> None:
    (tmp_path / "Index.html").write_text("<html></html>", encoding="utf-8")

    pack = build_ui_polish_decision_pack(repo_root=tmp_path, now_utc="2026-06-22T00:00:00Z")

    assert pack["decision_status"] == "UI_POLISH_READY_FOR_HUMAN_REVIEW"
    assert pack["reviews"] == []
    assert pack["blockers"] == []
    assert pack["canonical_index_candidates"][0]["relative_path"] == "Index.html"


def test_p108_markdown_lists_allowed_and_forbidden_actions(tmp_path) -> None:
    pack = build_ui_polish_decision_pack(repo_root=tmp_path, now_utc="2026-06-22T00:00:00Z")
    markdown = render_ui_polish_requirements_markdown(pack)

    assert "P108 UI Polish Decision Gate" in markdown
    assert "NO_INDEX_HTML_EDIT" in markdown
    assert "OVERWRITE_INDEX_HTML" in markdown
    assert "HUMAN_REVIEW_CANONICAL_INDEX" in markdown


def test_p108_safety_flags_locked() -> None:
    assert UI_POLISH_DECISION_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "canonical_webapp_index_do_not_overwrite": True,
        "ui_polish_decision_gate_only": True,
        "public_deploy_blocked_until_explicit_approval": True,
        "no_index_html_edit": True,
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
