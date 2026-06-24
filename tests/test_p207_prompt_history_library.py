from pathlib import Path

from mvp_qaic_py.p207_prompt_history_library import (
    build_prompt_history_library,
    write_prompt_history_library,
)


def test_p207_builds_prompt_history_library(tmp_path: Path) -> None:
    inputs = tmp_path / "01_OPERATOR_INPUTS"
    inputs.mkdir()
    (inputs / "session_prompt_gem.md").write_text(
        "# Prompt GEM\nCopier le prompt\nSauver réponse GEM localement",
        encoding="utf-8",
    )

    payload = build_prompt_history_library(
        tmp_path,
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "OK_P207_PROMPT_HISTORY_LIBRARY_READY"
    assert payload["entry_count"] == 1
    assert payload["entries"][0]["path"] == "01_OPERATOR_INPUTS/session_prompt_gem.md"
    assert payload["local_only"] is True
    assert payload["review_only"] is True
    assert payload["server_started"] is False
    assert payload["browser_started"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p207_empty_library_is_review_not_blocked(tmp_path: Path) -> None:
    payload = build_prompt_history_library(
        tmp_path,
        generated_at="2026-06-24T00:00:00Z",
    )

    assert payload["STATUS"] == "REVIEW_P207_PROMPT_HISTORY_LIBRARY_EMPTY"
    assert payload["entry_count"] == 0
    assert payload["recommended_next"] == "P208_PROMPT_HISTORY_UI_BINDING_FAST_FUSE"


def test_p207_write_outputs_are_isolated(tmp_path: Path) -> None:
    source = tmp_path / "mvp_qaic_py"
    source.mkdir()
    (source / "p177_gem_portfolio_prompt_workflow_usable_smoke.py").write_text(
        'PROMPT = "Prompt GEM local only"',
        encoding="utf-8",
    )

    output = tmp_path / "export"
    payload = write_prompt_history_library(
        tmp_path,
        output,
        generated_at="2026-06-24T00:00:00Z",
    )

    json_path = Path(payload["json_path"])
    md_path = Path(payload["md_path"])

    assert json_path.exists()
    assert md_path.exists()
    assert json_path.parent == output
    assert md_path.parent == output
    assert "Prompt History Library" in md_path.read_text(encoding="utf-8")
