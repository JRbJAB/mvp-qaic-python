from __future__ import annotations

from mvp_qaic_py.webapp_canonical_index_confirmation import (
    CANONICAL_INDEX_CONFIRMATION_SAFETY,
    build_binding_patch_plan,
    build_confirmation_pack,
    build_confirmation_options,
    render_confirmation_markdown,
    select_top_candidate,
)


def _sample_audit() -> dict:
    return {
        "candidate_count": 71,
        "probable_canonical_count": 10,
        "possible_canonical_count": 66,
        "top_candidate": {
            "relative_path": "03_DEV/APPS_SCRIPT_PULL_ISOLATED/CAND_001/MVPQAIC_Index.html",
            "full_path": "G:/demo/MVPQAIC_Index.html",
            "canonical_score": 95,
            "candidate_role": "probable_canonical_apps_script_mirror",
            "allowed_to_edit": False,
        },
    }


def test_p110b_selects_top_candidate_from_audit() -> None:
    top = select_top_candidate(_sample_audit())

    assert top is not None
    assert top["canonical_score"] == 95
    assert top["allowed_to_edit"] is False


def test_p110b_pack_requires_human_confirmation() -> None:
    pack = build_confirmation_pack(_sample_audit(), now_utc="2026-06-22T00:00:00Z")

    assert pack["decision_status"] == "REVIEW_REQUIRED"
    assert "HUMAN_CONFIRMATION_REQUIRED_BEFORE_ANY_INDEX_PATCH" in pack["reviews"]
    assert pack["top_candidate"]["relative_path"].endswith("MVPQAIC_Index.html")


def test_p110b_confirmation_options_never_apply_now() -> None:
    options = build_confirmation_options()

    assert {item["applies_now"] for item in options} == {False}
    assert {item["requires_human"] for item in options} == {True}


def test_p110b_binding_patch_plan_never_applies_now() -> None:
    plan = build_binding_patch_plan(_sample_audit()["top_candidate"])

    assert plan
    assert {item["apply_now"] for item in plan} == {False}
    assert {item["target_candidate"] for item in plan} == {
        "03_DEV/APPS_SCRIPT_PULL_ISOLATED/CAND_001/MVPQAIC_Index.html"
    }


def test_p110b_markdown_contains_forbidden_actions_and_top_candidate() -> None:
    pack = build_confirmation_pack(_sample_audit(), now_utc="2026-06-22T00:00:00Z")
    markdown = render_confirmation_markdown(pack)

    assert "P110B" in markdown
    assert "MVPQAIC_Index.html" in markdown
    assert "EDIT_INDEX_HTML_NOW" in markdown
    assert "NO_PUBLIC_DEPLOY" in markdown


def test_p110b_safety_flags_locked() -> None:
    assert CANONICAL_INDEX_CONFIRMATION_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "human_confirmation_required": True,
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
