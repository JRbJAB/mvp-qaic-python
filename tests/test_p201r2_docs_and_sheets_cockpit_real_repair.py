from pathlib import Path
import mvp_qaic_py.p201r2_docs_and_sheets_cockpit_real_repair as p201r2


def test_sheet_cockpit_plan_has_real_sheets_tabs():
    rows = p201r2.build_sheets_cockpit_plan()
    names = {r["sheet_tab"] for r in rows}
    assert "QAIC_OPERATOR_COCKPIT" in names
    assert "MIGRATION_CONTROL" in names
    assert "INSTRUCTIONS_TRACKER" in names
    assert "DOCS_INDEX" in names
    assert "GEM_DECISION_JOURNAL" in names
    assert len(rows) >= 20
    assert all(r["write_policy"] == "DRY_RUN_ONLY_NO_LIVE_WRITE" for r in rows)


def test_notice_utf8_accents_and_routes(tmp_path: Path):
    content = p201r2.notice_html(
        {"doc_count": 1, "sheet_cockpit_tab_count": 22, "residual_doc_count": 0}, tmp_path
    )
    assert 'charset="utf-8"' in content
    assert "é è à ç ù œ" in content
    assert "/sheets-cockpit-plan" in content
    assert "/migration-control" in content


def test_export_writes_repo_and_main_docs(tmp_path: Path):
    repo = tmp_path / "repo"
    main = tmp_path / "main"
    repo.mkdir()
    main.mkdir()
    (repo / "README.md").write_text("# test", encoding="utf-8")
    payload = p201r2.export_payload(repo, main, repo / "05_EXPORTS" / "P201R2_TEST")
    assert payload["sheet_cockpit_tab_count"] >= 20
    assert payload["main_folder_write_ok"] is True
    assert (repo / "docs" / "FINAL" / "MVP_QAIC_NOTICE_UTILISATION.html").exists()
    assert (repo / "docs" / "FINAL" / "MVP_QAIC_SHEETS_COCKPIT_BLUEPRINT.csv").exists()
    assert (
        main / "01_DOCS" / "FINAL_FUSED" / "MVP_QAIC_PY" / "MVP_QAIC_NOTICE_UTILISATION.html"
    ).exists()
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False
