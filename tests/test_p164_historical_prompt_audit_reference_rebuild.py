from __future__ import annotations

import csv
from pathlib import Path

from mvp_qaic_py.p164_historical_prompt_audit_reference_rebuild import (
    PROMPT_SOURCE_ID_CURRENT,
    build_and_write_export,
    build_inventory,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_p164_demotes_p132_p133_runtime_contract_only(tmp_path: Path) -> None:
    _write(
        tmp_path / "mvp_qaic_py" / "multimodal_gem_image_prompt_usd_contract.py",
        "P132 P133 portfolio prompt image json hard rules",
    )
    _write(
        tmp_path / "archives" / "prompt_global_ancien.md",
        "Demande globale en plusieurs points GEM portfolio capture image JSON human_review no broker no order no sizing",
    )
    rows = build_inventory(tmp_path)
    kinds = {r.rel_path: r.source_kind for r in rows}
    assert (
        kinds["mvp_qaic_py/multimodal_gem_image_prompt_usd_contract.py"]
        == "CURRENT_RUNTIME_CONTRACT_REFERENCE"
    )
    assert "HISTORICAL" in kinds["archives/prompt_global_ancien.md"]


def test_p164_writes_reference_candidate_review_only(tmp_path: Path) -> None:
    _write(
        tmp_path / "old_prompts" / "prompt_global_ancien.md",
        "Prompt global: demande globale en plusieurs points. GEM portfolio capture écran Revolut image JSON risque décision REVIEW_REQUIRED.",
    )
    summary = build_and_write_export(tmp_path)
    assert summary["STATUS"].startswith("OK_P164")
    assert summary["P132_P133_DEMOTED_TO_RUNTIME_CONTRACT_ONLY"] is True
    assert summary["REFERENCE_PROMPT_CANDIDATE_CREATED"] is True
    assert summary["RUNTIME_PROMPT_MODIFIED"] is False
    assert summary["APPLY_ALLOWED"] is False
    candidate = Path(str(summary["REFERENCE_PROMPT_CANDIDATE_FILE"])).read_text(encoding="utf-8")
    assert "Objectif global en plusieurs points" in candidate
    assert "HUMAN_REVIEW_ONLY" in candidate
    assert "NO_BROKER_EXECUTION" in candidate


def test_p164_inventory_csv_contains_scores(tmp_path: Path) -> None:
    _write(
        tmp_path / "archive" / "prompt_reference_historique.txt",
        "Mission globale portfolio GEM avec plusieurs points extraction contrôle décision JSON risque.",
    )
    summary = build_and_write_export(tmp_path)
    with Path(str(summary["INVENTORY_FILE"])).open(encoding="utf-8", newline="") as h:
        rows = list(csv.DictReader(h))
    assert rows
    assert rows[0]["rel_path"] == "archive/prompt_reference_historique.txt"
    assert int(rows[0]["score"]) > 0


def test_p164_summary_preserves_no_live_actions(tmp_path: Path) -> None:
    _write(
        tmp_path / "archive" / "prompt_historique.md",
        "demande globale plusieurs points gem portfolio image json human review no broker no order no sizing",
    )
    summary = build_and_write_export(tmp_path)
    assert summary["GOOGLE_SHEETS_WRITE"] is False
    assert summary["PUBLIC_DEPLOY"] is False
    assert summary["NO_APPS_SCRIPT_EXECUTION"] is True
    assert summary["NO_CLASP_PUSH"] is True
    assert summary["NO_BROKER"] is True
    assert summary["NO_ORDER"] is True
    assert summary["NO_SIZING"] is True


def test_p164_current_prompt_id_constant_is_present() -> None:
    assert PROMPT_SOURCE_ID_CURRENT == "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
