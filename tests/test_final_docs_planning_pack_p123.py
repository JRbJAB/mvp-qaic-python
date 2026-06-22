import json
import subprocess
import sys

from mvp_qaic_py.final_docs_planning_pack import (
    SAFETY_MARKERS,
    EXISTING_DOC_DIRS,
    FinalDocsRequest,
    build_docs,
    build_project_status,
    scan_existing_doc_files,
    write_final_docs_pack,
)


def test_p123_builds_all_canonical_and_emoji_docs(tmp_path):
    result = write_final_docs_pack(
        FinalDocsRequest(
            docs_root=tmp_path / "docs",
            output_dir=tmp_path / "export",
            generated_at_utc="2026-06-22T00:00:00Z",
            source_head="abc123",
        )
    )

    assert result["status"] == "FINAL_DOCS_READY"
    assert result["doc_count"] == 15
    assert result["true_fusion_initial_to_p122"] is True
    assert result["md_emoji_deliverables"] is True

    assert (tmp_path / "docs" / "FINAL" / "MVP_QAIC_FINAL_OPERATING_CONTEXT.md").exists()
    assert (tmp_path / "docs" / "FINAL" / "📚 MVP_QAIC_FINAL_DOCS_INDEX.md").exists()
    assert (tmp_path / "docs" / "CDC" / "📘 CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md").exists()
    assert (tmp_path / "docs" / "ROADMAP" / "🗺️ ROADMAP_VISUAL_V0_1_TO_V1_0.md").exists()
    assert (
        tmp_path / "docs" / "ARCHITECTURE" / "🧬 MVP_QAIC_FUSION_INITIALE_TO_P122_TRACE.md"
    ).exists()
    assert (tmp_path / "export" / "P123_FINAL_DOCS_MANIFEST.json").exists()


def test_p123_true_fusion_and_emoji_md_deliverables(tmp_path):
    write_final_docs_pack(
        FinalDocsRequest(docs_root=tmp_path / "docs", output_dir=tmp_path / "export")
    )

    fusion_trace = (
        tmp_path / "docs" / "ARCHITECTURE" / "🧬 MVP_QAIC_FUSION_INITIALE_TO_P122_TRACE.md"
    )
    emoji_roadmap = tmp_path / "docs" / "ROADMAP" / "🗺️ ROADMAP_VISUAL_V0_1_TO_V1_0.md"
    emoji_handoff = tmp_path / "docs" / "HANDOFF" / "🤝 MVP_QAIC_OPERATOR_HANDOFF_FINAL.md"

    assert fusion_trace.exists()
    assert emoji_roadmap.exists()
    assert emoji_handoff.exists()

    fusion_text = fusion_trace.read_text(encoding="utf-8")
    assert "REAL_FUSION_UPDATED_FROM_INITIAL_VERSION_TO_P122 = TRUE" in fusion_text
    assert "Version initiale" in fusion_text
    assert "État P122 intégré" in fusion_text
    assert "QAIC backend" in fusion_text
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in fusion_text


def test_p123_existing_docs_are_detected_and_integrated(tmp_path):
    audit_dir = tmp_path / "docs" / "audit" / "qaic_migration"
    public_dir = tmp_path / "docs" / "qaic_public_contracts"
    audit_dir.mkdir(parents=True)
    public_dir.mkdir(parents=True)
    (audit_dir / "audit.md").write_text("# audit", encoding="utf-8")
    (public_dir / "contract.json").write_text("{}", encoding="utf-8")

    files = scan_existing_doc_files(tmp_path)
    assert "docs/audit/qaic_migration/audit.md" in files
    assert "docs/qaic_public_contracts/contract.json" in files

    result = write_final_docs_pack(
        FinalDocsRequest(
            docs_root=tmp_path / "01_DOCS",
            output_dir=tmp_path / "export",
            project_root=tmp_path,
        )
    )

    assert result["existing_docs_integrated"] is True
    assert result["existing_doc_file_count"] == 2


def test_p123_docs_include_planning_cdc_and_v1(tmp_path):
    result = write_final_docs_pack(
        FinalDocsRequest(docs_root=tmp_path / "docs", output_dir=tmp_path / "export")
    )

    roadmap = (tmp_path / "docs" / "ROADMAP" / "🗺️ ROADMAP_VISUAL_V0_1_TO_V1_0.md").read_text(
        encoding="utf-8"
    )
    cdc = (tmp_path / "docs" / "CDC" / "📘 CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md").read_text(
        encoding="utf-8"
    )

    assert "V0.1" in roadmap
    assert "V1.0" in roadmap
    assert "4 à 8 semaines" in roadmap
    assert "Definition of Done V1.0" in cdc
    assert result["next"] == "WAIT_OPERATOR_REAL_GEM_TEST_OR_P124_UI_INPUT_HELPER"


def test_p123_architecture_doc_contains_fusion_and_boundaries(tmp_path):
    write_final_docs_pack(
        FinalDocsRequest(docs_root=tmp_path / "docs", output_dir=tmp_path / "export")
    )
    architecture = (
        tmp_path / "docs" / "ARCHITECTURE" / "🧩 MVP_QAIC_FUSION_ARCHITECTURE_CORRECTIONS.md"
    ).read_text(encoding="utf-8")

    assert "Fusion réelle" in architecture
    assert "MVP QAIC" in architecture
    assert "QAIC backend" in architecture
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in architecture


def test_p123_drive_rangement_doc_is_non_destructive(tmp_path):
    write_final_docs_pack(
        FinalDocsRequest(docs_root=tmp_path / "docs", output_dir=tmp_path / "export")
    )
    drive = (
        tmp_path / "docs" / "DRIVE_RANGEMENT" / "🗂️ MVP_QAIC_DRIVE_RANGEMENT_FINAL.md"
    ).read_text(encoding="utf-8")

    assert "Rangement non destructif" in drive
    assert "01_DOCS" in drive
    assert "05_EXPORTS" in drive
    assert "docs/audit/qaic_migration" in drive
    assert "docs/qaic_public_contracts" in drive


def test_p123_project_status_contains_p118_to_p122_and_safety():
    status = build_project_status(
        FinalDocsRequest(docs_root="docs", output_dir="out", source_head="head")
    )
    text = json.dumps(status, ensure_ascii=False)

    assert "P118" in text
    assert "P119" in text
    assert "P120" in text
    assert "P121" in text
    assert "P122" in text
    assert "NO_SHEET_WRITE" in text
    assert "NO_BROKER" in text
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in text


def test_p123_cli_generates_docs(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.final_docs_planning_pack",
            "--docs-root",
            str(tmp_path / "docs"),
            "--output-dir",
            str(tmp_path / "export"),
            "--project-root",
            str(tmp_path),
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
            "--source-head",
            "abc123",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "FINAL_DOCS_READY" in completed.stdout
    assert "True" in completed.stdout
    assert (tmp_path / "docs" / "FINAL" / "📚 MVP_QAIC_FINAL_DOCS_INDEX.md").exists()


def test_p123_safety_markers_are_explicit():
    required = {
        "DOCS_ONLY",
        "LOCAL_ONLY",
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "TRUE_FUSION_INITIAL_TO_P122",
        "MD_EMOJI_DELIVERABLES",
        "EXISTING_DOCS_INTEGRATED",
        "NO_INDEX_EDIT",
        "NO_CLASP",
        "NO_APPS_SCRIPT_EXECUTION",
        "NO_SHEET_WRITE",
        "NO_PUBLIC_DEPLOY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_AUTO_SIZING",
        "NO_AUTO_APPLY_GEM_RESPONSE",
        "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    }

    assert required.issubset(set(SAFETY_MARKERS))
    assert "docs/audit/qaic_migration" in EXISTING_DOC_DIRS
    assert "docs/qaic_public_contracts" in EXISTING_DOC_DIRS


def test_p123_build_docs_has_fifteen_entries():
    docs = build_docs(FinalDocsRequest(docs_root="docs", output_dir="out"))
    assert len(docs) == 15
