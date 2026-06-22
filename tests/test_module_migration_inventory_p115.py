import json

from mvp_qaic_py.module_migration_inventory import (
    SAFETY_MARKERS,
    build_boundary_contract,
    build_migration_inventory,
    export_migration_inventory_pack,
)


def test_p115_prompt_and_normalizer_priorities(tmp_path):
    (tmp_path / "mvp_qaic_py").mkdir()
    (tmp_path / "mvp_qaic_py" / "gem_portfolio_prompt_module.py").write_text(
        "# prompt\n", encoding="utf-8"
    )
    (tmp_path / "mvp_qaic_py" / "portfolio_input_normalizer.py").write_text(
        "# normalizer\n", encoding="utf-8"
    )

    inventory = build_migration_inventory(tmp_path)
    by_path = {candidate["path"]: candidate for candidate in inventory["candidates"]}

    assert by_path["mvp_qaic_py/gem_portfolio_prompt_module.py"]["category"] == "PROMPT_GEM_RUNTIME"
    assert by_path["mvp_qaic_py/gem_portfolio_prompt_module.py"]["priority_rank"] == 1
    assert (
        by_path["mvp_qaic_py/portfolio_input_normalizer.py"]["category"]
        == "PORTFOLIO_INPUT_NORMALIZER"
    )
    assert by_path["mvp_qaic_py/portfolio_input_normalizer.py"]["priority_rank"] == 2


def test_p115_revolutx_stays_private_qaic(tmp_path):
    (tmp_path / "qaic_private").mkdir()
    (tmp_path / "qaic_private" / "revolutx_order_execution.py").write_text(
        "# no mvp\n", encoding="utf-8"
    )

    inventory = build_migration_inventory(tmp_path)
    candidate = inventory["candidates"][0]

    assert candidate["category"] == "QAIC_BACKEND_PRIVATE_REVOLUTX"
    assert candidate["migration_decision"] == "OUT_OF_SCOPE_FOR_MVP_KEEP_QAIC_PRIVATE"
    assert candidate["safety_boundary"] == "QAIC_PRIVATE_BACKEND_SEPARATE_FROM_MVP"


def test_p115_index_not_migrated_now(tmp_path):
    (tmp_path / "apps").mkdir()
    (tmp_path / "apps" / "MVPQAIC_Index.html").write_text("<html></html>\n", encoding="utf-8")

    inventory = build_migration_inventory(tmp_path)
    candidate = inventory["candidates"][0]

    assert candidate["category"] == "UI_APPS_SCRIPT_INDEX"
    assert candidate["migration_decision"] == "DO_NOT_MIGRATE_NOW_REVIEW_ONLY"


def test_p115_contract_forbids_live_and_broker_actions():
    contract = build_boundary_contract()
    forbidden = set(contract["mvp_forbidden_scope"])

    assert "clasp_push" in forbidden
    assert "apps_script_live_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert contract["index_policy"] == "DO_NOT_EDIT_OR_MIGRATE_NOW_SEPARATE_BATCH_REQUIRED"


def test_p115_export_pack_and_desktop_ini_skip(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "prompt_gem_runner.py").write_text("# prompt\n", encoding="utf-8")
    (project / "lexique_crypto_signals.csv").write_text("term,definition\n", encoding="utf-8")
    (project / "desktop.ini").write_text("pollution\n", encoding="utf-8")

    out = tmp_path / "export"
    result = export_migration_inventory_pack(out, project)

    assert result["status"] == "EXPORTED"
    assert result["candidate_count"] == 2

    expected = {
        "P115_MODULE_MIGRATION_INVENTORY.json",
        "P115_MODULE_MIGRATION_INVENTORY.csv",
        "P115_MIGRATION_PRIORITY_MATRIX.md",
        "P115_MIGRATION_BOUNDARY_CONTRACT.json",
        "P115_RUNNER_REPORT.md",
    }
    assert expected == {path.name for path in out.iterdir()}

    payload = json.loads((out / "P115_MODULE_MIGRATION_INVENTORY.json").read_text(encoding="utf-8"))
    assert "desktop.ini" not in json.dumps(payload)


def test_p115_safety_markers_are_explicit():
    required = {
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "NO_INDEX_EDIT",
        "NO_CLASP",
        "NO_APPS_SCRIPT_EXECUTION",
        "NO_SHEET_WRITE",
        "NO_PUBLIC_DEPLOY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_AUTO_SIZING",
        "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
        "QAIC_BACKEND_PRIVATE_SEPARATE",
    }

    assert required.issubset(set(SAFETY_MARKERS))
