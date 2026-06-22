from __future__ import annotations

from mvp_qaic_py.webapp_canonical_index_confirmation_seal import (
    CANONICAL_INDEX_CONFIRMATION_SEAL_SAFETY,
    build_canonical_confirmation_decision,
    extract_top_candidate,
    render_confirmation_seal_markdown,
)


def _sample_pack() -> dict:
    return {
        "top_candidate": {
            "relative_path": "03_DEV/APPS_SCRIPT_PULL_ISOLATED/CAND_001/MVPQAIC_Index.html",
            "full_path": "G:/demo/MVPQAIC_Index.html",
            "canonical_score": 95,
            "candidate_role": "probable_canonical_apps_script_mirror",
            "allowed_to_edit": False,
        }
    }


def test_p111_r1_extracts_top_candidate() -> None:
    top = extract_top_candidate(_sample_pack())

    assert top is not None
    assert top["canonical_score"] == 95
    assert top["relative_path"].endswith("MVPQAIC_Index.html")


def test_p111_r1_accepts_top_candidate_after_p112() -> None:
    decision = build_canonical_confirmation_decision(
        _sample_pack(),
        human_decision="ACCEPT_TOP_CANDIDATE_AS_CANONICAL",
        now_utc="2026-06-22T00:00:00Z",
    )

    assert decision["decision_status"] == "CONFIRMED_CANONICAL_TARGET_CONTRACT_READY"
    assert decision["binding_target_contract"]["patch_allowed_now"] is False
    assert decision["binding_target_contract"]["reconciled_after_p112"] is True
    assert "P111_R1_RECONCILE_AFTER_P112_ALREADY_SEALED" in decision["reviews"]


def test_p111_r1_blocks_when_not_accepted() -> None:
    decision = build_canonical_confirmation_decision(
        _sample_pack(),
        human_decision="NEEDS_MORE_REVIEW",
        now_utc="2026-06-22T00:00:00Z",
    )

    assert decision["decision_status"] == "BLOCKED"
    assert "TOP_CANDIDATE_NOT_ACCEPTED" in decision["blockers"]


def test_p111_r1_markdown_contains_no_patch_or_deploy_policy() -> None:
    decision = build_canonical_confirmation_decision(
        _sample_pack(),
        human_decision="ACCEPT_TOP_CANDIDATE_AS_CANONICAL",
        now_utc="2026-06-22T00:00:00Z",
    )
    markdown = render_confirmation_seal_markdown(decision)

    assert "P111-R1" in markdown
    assert "reconciles the sequence without rollback" in markdown
    assert "NO_INDEX_HTML_EDIT" in markdown
    assert "ROLLBACK_P112_WITHOUT_REASON" in markdown
    assert "public_deploy: `BLOCKED`" in markdown


def test_p111_r1_safety_flags_locked() -> None:
    assert CANONICAL_INDEX_CONFIRMATION_SEAL_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "canonical_index_confirmation_only": True,
        "binding_target_contract_only": True,
        "after_p112_reconcile": True,
        "no_index_html_edit": True,
        "no_index_html_generation": True,
        "no_source_patch_apply": True,
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
