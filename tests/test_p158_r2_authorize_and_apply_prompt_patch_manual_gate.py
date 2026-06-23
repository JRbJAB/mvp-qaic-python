from __future__ import annotations

from mvp_qaic_py.p158_r2_authorize_and_apply_prompt_patch_manual_gate import (
    PATCH_MARKER,
    apply_patch_block_to_prompt_source,
    boolish,
    validate_p158_summary,
)


def test_boolish_accepts_operator_values() -> None:
    assert boolish(True) is True
    assert boolish("YES") is True
    assert boolish("true") is True
    assert boolish("NO") is False


def test_validate_p158_summary_accepts_uppercase_ready_manual_gate() -> None:
    summary = {
        "P158_STATUS": "P158_STOP_WAITING_MANUAL_APPLY_AUTHORIZATION",
        "PATCH_CANDIDATE_FOUND": True,
        "PATCH_SAFE_FOR_REVIEW": True,
        "CANDIDATE_READY_FOR_MANUAL_APPLY": True,
        "SOURCE_PATCH_APPLIED": False,
        "PROMPT_SOURCE_MODIFIED": False,
        "GOOGLE_SHEETS_WRITE": False,
        "PUBLIC_DEPLOY": False,
    }
    assert validate_p158_summary(summary) == []


def test_validate_p158_summary_accepts_lowercase_dataclass_asdict_keys() -> None:
    summary = {
        "status": "P158_STOP_WAITING_MANUAL_APPLY_AUTHORIZATION",
        "patch_candidate_found": True,
        "patch_safe_for_review": True,
        "candidate_ready_for_manual_apply": True,
        "source_patch_applied": False,
        "prompt_source_modified": False,
        "google_sheets_write": False,
        "public_deploy": False,
    }
    assert validate_p158_summary(summary) == []


def test_validate_p158_summary_blocks_unsafe_prior_apply() -> None:
    summary = {
        "status": "P158_STOP_WAITING_MANUAL_APPLY_AUTHORIZATION",
        "patch_candidate_found": True,
        "patch_safe_for_review": True,
        "candidate_ready_for_manual_apply": True,
        "source_patch_applied": True,
        "prompt_source_modified": False,
        "google_sheets_write": False,
        "public_deploy": False,
    }
    assert "P158_ALREADY_SOURCE_PATCH_APPLIED" in validate_p158_summary(summary)


def test_apply_patch_block_inserts_inside_triple_quoted_prompt() -> None:
    source = 'PROMPT = """# P132 GEM Multimodal Portfolio Prompt\n\n## Hard rules\n\nExisting rule.\n"""\n'
    patched, changed, mode = apply_patch_block_to_prompt_source(source)
    assert changed is True
    assert PATCH_MARKER in patched
    assert mode == "inserted_inside_prompt_hard_rules"
    assert patched.index("## Hard rules") < patched.index(PATCH_MARKER)


def test_apply_patch_block_is_idempotent() -> None:
    source = 'PROMPT = """# P132 GEM Multimodal Portfolio Prompt\n\n## Hard rules\n\nExisting rule.\n"""\n'
    patched, changed, _ = apply_patch_block_to_prompt_source(source)
    assert changed is True
    patched_again, changed_again, mode_again = apply_patch_block_to_prompt_source(patched)
    assert changed_again is False
    assert mode_again == "already_present"
    assert patched_again == patched


def test_apply_patch_block_falls_back_to_valid_python_constant() -> None:
    source = "# P132 GEM Multimodal Portfolio Prompt\n\n## Hard rules\n\n# comment only\n"
    patched, changed, mode = apply_patch_block_to_prompt_source(source)
    assert changed is True
    assert PATCH_MARKER in patched
    assert "P158_R5_RUNTIME_CLARIFICATION_PATCH" in patched
    assert mode == "appended_python_addendum_constant"


def test_patch_text_does_not_create_forbidden_runtime_flags() -> None:
    source = 'PROMPT = """# P132 GEM Multimodal Portfolio Prompt\n\n## Hard rules\n\nExisting rule.\n"""\n'
    patched, _, _ = apply_patch_block_to_prompt_source(source)
    forbidden = [
        "AUTO_BROKER_EXECUTION=true",
        "GOOGLE_SHEETS_WRITE=true",
        "PUBLIC_DEPLOY=true",
        "NO_AUTO_APPLY_GEM_RESPONSE=false",
    ]
    upper = patched.upper()
    for marker in forbidden:
        assert marker.upper() not in upper
