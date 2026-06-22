from __future__ import annotations

from mvp_qaic_py.webapp_canonical_index_locator import (
    CANONICAL_INDEX_LOCATOR_SAFETY,
    build_locator_audit,
    load_locator_roots_json,
    locate_index_candidates,
    normalize_locator_roots,
    score_locator_candidate,
)


def test_p110a_scores_apps_script_mirror_as_probable() -> None:
    result = score_locator_candidate(
        "03_DEV/APPS_SCRIPT_MIRROR/Index.html",
        "mvp qaic root",
    )

    assert result["candidate_role"] == "probable_canonical_apps_script_mirror"
    assert result["canonical_score"] == 95


def test_p110a_scores_exports_as_not_canonical() -> None:
    result = score_locator_candidate(
        "05_EXPORTS/P106/STATIC_PREVIEW/index.html",
        "python repo",
    )

    assert result["candidate_role"] == "python_generated_export_not_canonical"
    assert result["canonical_score"] == 0


def test_p110a_locates_candidates_across_roots(tmp_path) -> None:
    py_root = tmp_path / "MVP_QAIC_PY"
    mvp_root = tmp_path / "MVP_QAIC"
    mirror = mvp_root / "03_DEV" / "APPS_SCRIPT_MIRROR"
    export = py_root / "05_EXPORTS" / "P106"
    mirror.mkdir(parents=True)
    export.mkdir(parents=True)
    (mirror / "Index.html").write_text("<html></html>", encoding="utf-8")
    (export / "index.html").write_text("<html></html>", encoding="utf-8")

    candidates = locate_index_candidates(
        [
            {"root_id": "python_repo", "path": str(py_root), "role": "python repo"},
            {"root_id": "mvp_root", "path": str(mvp_root), "role": "mvp qaic root"},
        ]
    )

    assert len(candidates) == 2
    assert candidates[0]["canonical_score"] == 95
    assert candidates[0]["allowed_to_edit"] is False


def test_p110a_audit_review_required_even_when_candidate_found(tmp_path) -> None:
    mirror = tmp_path / "03_DEV" / "APPS_SCRIPT_MIRROR"
    mirror.mkdir(parents=True)
    (mirror / "Index.html").write_text("<html></html>", encoding="utf-8")

    audit = build_locator_audit(
        roots=[{"root_id": "mvp_root", "path": str(tmp_path), "role": "mvp qaic root"}],
        now_utc="2026-06-22T00:00:00Z",
    )

    assert audit["decision_status"] == "CANONICAL_INDEX_CANDIDATE_FOUND_REVIEW_REQUIRED"
    assert audit["top_candidate"]["canonical_score"] == 95
    assert audit["top_candidate"]["allowed_to_edit"] is False


def test_p110a_load_locator_roots_json_accepts_utf8_bom(tmp_path) -> None:
    path = tmp_path / "roots.json"
    path.write_text(
        '[{"root_id":"demo","path":"X:/demo","role":"mvp qaic root"}]',
        encoding="utf-8-sig",
    )

    roots = load_locator_roots_json(path)

    assert roots == [{"root_id": "demo", "path": "X:/demo", "role": "mvp qaic root"}]


def test_p110a_normalize_roots_and_safety_locked() -> None:
    roots = normalize_locator_roots([{"path": "X:/demo"}])

    assert roots[0]["root_id"] == "root_01"
    assert CANONICAL_INDEX_LOCATOR_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "bounded_local_readonly_locator": True,
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
