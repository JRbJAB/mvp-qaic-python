from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P123_FINAL_DOCS_TRUE_FUSION_MD_EMOJI_0_3_0_SAFE"

SAFETY_MARKERS = (
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
    "NO_CANCEL",
    "NO_REPLACE_ORDER",
    "NO_AUTO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

EXISTING_DOC_DIRS = (
    "docs/audit/qaic_migration",
    "docs/qaic_public_contracts",
)


@dataclass(frozen=True)
class FinalDocsRequest:
    docs_root: str | Path
    output_dir: str | Path
    project_root: str | Path | None = None
    generated_at_utc: str | None = None
    source_head: str | None = None
    p122_export_dir: str | None = None
    notes: str | None = None


def _join(lines: Sequence[str]) -> str:
    return "\n".join(lines).rstrip() + "\n"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def scan_existing_doc_files(project_root: str | Path | None) -> list[str]:
    if project_root is None:
        return []
    root = Path(project_root)
    files: list[str] = []
    allowed_suffixes = {".md", ".json", ".csv", ".txt"}
    for rel_dir in EXISTING_DOC_DIRS:
        folder = root / rel_dir
        if not folder.exists():
            continue
        for file_path in sorted(folder.rglob("*")):
            if file_path.is_file() and file_path.suffix.lower() in allowed_suffixes:
                files.append(file_path.relative_to(root).as_posix())
    return files


def build_project_status(request: FinalDocsRequest) -> dict[str, Any]:
    return {
        "project": "MVP_QAIC_PY",
        "status": "P122_OPERATOR_HANDOFF_READY",
        "source_head": request.source_head,
        "generated_at_utc": request.generated_at_utc,
        "p122_export_dir": request.p122_export_dir,
        "true_fusion_initial_to_p122": True,
        "md_emoji_deliverables": True,
        "existing_docs_integrated": True,
        "existing_doc_dirs": list(EXISTING_DOC_DIRS),
        "current_capability": [
            "P118 daily GEM prompt/runtime pack",
            "P119 GEM response capture and review queue",
            "P120 local decision journal bridge",
            "P121 end-to-end local smoke",
            "P122 operator handoff and stop pack",
        ],
        "boundaries": list(SAFETY_MARKERS),
        "next": "WAIT_OPERATOR_REAL_GEM_TEST_OR_P124_UI_INPUT_HELPER",
    }


def operating_context_doc(request: FinalDocsRequest) -> str:
    return _join(
        [
            "# MVP QAIC — Final Operating Context",
            "",
            f"Version: `{VERSION}`",
            f"Generated at UTC: `{request.generated_at_utc or 'UNSPECIFIED'}`",
            f"Source HEAD: `{request.source_head or 'UNSPECIFIED'}`",
            "",
            "## Mission",
            "",
            "MVP QAIC est la couche produit publique/opérateur : lexique, méthodes, prompts,",
            "revue GEM, review queue et journal local candidat.",
            "",
            "QAIC backend reste séparé : moteur privé de calcul, scoring, risk, providers,",
            "Revolut X et modules execution-capable verrouillés.",
            "",
            "## État validé",
            "",
            "- P118 : génération du prompt quotidien GEM.",
            "- P119 : capture de réponse GEM et review queue locale.",
            "- P120 : bridge local vers entrée candidate de decision journal.",
            "- P121 : smoke end-to-end local P118 -> P119 -> P120.",
            "- P122 : handoff opérateur et stop pack.",
            "",
            "## Safety markers",
            "",
            *[f"- `{marker}`" for marker in SAFETY_MARKERS],
            "",
            "## Prochaine décision",
            "",
            "- test GEM réel opérateur avec vrai portfolio ; ou",
            "- helper local d'entrée, sans live layer.",
            "",
        ]
    )


def cdc_roadmap_doc(_: FinalDocsRequest) -> str:
    return _join(
        [
            "# CDC — MVP QAIC Operational Roadmap",
            "",
            "## Objectif produit",
            "",
            "Construire une boucle opérateur exploitable pour revue crypto éducative et support décisionnel :",
            "entrée portfolio/capture, prompt GEM, réponse GEM, review queue, entrée journal locale.",
            "",
            "## Hors périmètre",
            "",
            "- Trading automatique.",
            "- Ordres broker.",
            "- Sizing automatique.",
            "- Accès Revolut X réel depuis MVP.",
            "- `NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.",
            "- Écriture Google Sheets sans décision explicite séparée.",
            "",
            "## Roadmap opérationnelle",
            "",
            "| Version | Horizon | Objectif | Critère d'acceptation |",
            "|---|---:|---|---|",
            "| V0.1 | fait | Boucle GEM locale | P118-P122 scellés |",
            "| V0.2 | 1-3 jours | Premier vrai test opérateur | vrai portfolio + vraie réponse GEM + journal local |",
            "| V0.3 | 3-7 jours | Ergonomie locale | helper d'entrée + dossiers run propres |",
            "| V0.4 | 1-2 semaines | Mini cockpit local | interface simple input -> prompt -> capture -> journal |",
            "| V0.5 | 2-4 semaines | Pont MVP vers QAIC privé | export propre sans ordre ni sizing |",
            "| V0.6 | 3-5 semaines | Portfolio review usuel | templates par cas d'usage |",
            "| V0.7 | 4-6 semaines | Historique et qualité | registry runs + métriques erreurs |",
            "| V1.0 | 4-8 semaines | Version opérationnelle contrôlée | usage quotidien stable et auditable |",
            "",
            "## Definition of Done V1.0",
            "",
            "- Run quotidien en moins de 5 minutes.",
            "- Prompt GEM généré depuis input local.",
            "- Réponse GEM capturée.",
            "- Missing data et blockers visibles.",
            "- Journal local généré.",
            "- Aucune action live implicite.",
            "- Séparation MVP public / QAIC privé respectée.",
            "",
        ]
    )


def visual_roadmap_doc(_: FinalDocsRequest) -> str:
    return _join(
        [
            "# Roadmap visuelle — V0.1 vers V1.0",
            "",
            "```text",
            "22 juin 2026",
            "│",
            "├─ ✅ V0.1 — Boucle GEM locale fonctionnelle",
            "│   P118 → P119 → P120 → P121 → P122",
            "│",
            "├─ 🟡 V0.2 — Utilisation réelle opérateur",
            "│   Horizon : 1 à 3 jours",
            "│",
            "├─ 🟠 V0.3 — Ergonomie locale",
            "│   Horizon : 3 à 7 jours",
            "│",
            "├─ 🔵 V0.4 — Cockpit local / WebApp privée",
            "│   Horizon : 1 à 2 semaines",
            "│",
            "├─ 🟣 V0.5 — Liaison MVP ↔ QAIC backend",
            "│   Horizon : 2 à 4 semaines",
            "│",
            "└─ 🟢 V1.0 — Version opérationnelle contrôlée",
            "    Horizon : 4 à 8 semaines",
            "```",
            "",
            "## Chemin rapide recommandé",
            "",
            "```text",
            "P122 ✅",
            "  ↓",
            "P124 — Real GEM Manual Test Pack",
            "  ↓",
            "P125 — Operator Review UX",
            "  ↓",
            "P126 — Daily Run Registry",
            "  ↓",
            "P127 — Local UI Input Helper",
            "  ↓",
            "V0.2 opérationnelle manuelle",
            "```",
            "",
        ]
    )


def architecture_doc(_: FinalDocsRequest) -> str:
    return _join(
        [
            "# MVP QAIC — Fusion réelle et corrections d'architecture",
            "",
            "## Fusion réelle",
            "",
            "La fusion validée est documentaire, produit et opératoire. Elle ne fusionne pas les responsabilités",
            "d'exécution trading entre MVP et QAIC backend.",
            "",
            "- MVP QAIC : lexique, méthodes, prompts, WebApp/UI future, review opérateur.",
            "- QAIC backend : calcul privé, scoring, risk, providers, Revolut X, execution-capable locked.",
            "",
            "## Corrections techniques intégrées",
            "",
            "- P119 parse JSON robuste : BOM, texte brut, code fence JSON.",
            "- P119 déduplication des blockers entre payload explicite et détection texte.",
            "- P121 smoke end-to-end local vérifie P118 -> P119 -> P120.",
            "- P122 stop pack impose l'arrêt après handoff sauf demande explicite.",
            "",
            "## Interdiction permanente côté MVP",
            "",
            "- `NO_BROKER`.",
            "- `NO_ORDER`.",
            "- `NO_AUTO_SIZING`.",
            "- `NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.",
            "",
        ]
    )


def fusion_initial_to_p122_trace_doc(_: FinalDocsRequest) -> str:
    return _join(
        [
            "# 🧬 MVP QAIC — Fusion réelle initiale → P122",
            "",
            "## 1. Verdict",
            "",
            "`REAL_FUSION_UPDATED_FROM_INITIAL_VERSION_TO_P122 = TRUE`",
            "",
            "La fusion réelle est documentaire, produit et opératoire. Elle ne fusionne pas les responsabilités",
            "d'exécution trading entre MVP et QAIC backend.",
            "",
            "## 2. Version initiale",
            "",
            "La version initiale du MVP QAIC portait sur :",
            "",
            "- lexique crypto first ;",
            "- méthodes et signaux ;",
            "- WebApp/UI future ;",
            "- prompts opérateur ;",
            "- support décisionnel éducatif.",
            "",
            "## 3. État P122 intégré",
            "",
            "- P118 : prompt quotidien GEM ;",
            "- P119 : capture réponse GEM + review queue ;",
            "- P120 : bridge journal local ;",
            "- P121 : smoke end-to-end P118 -> P119 -> P120 ;",
            "- P122 : handoff opérateur + stop pack.",
            "",
            "## 4. Correction d'architecture",
            "",
            "MVP QAIC reste la couche publique/opérateur : lexique, prompts, méthodes, UI future.",
            "QAIC backend reste la couche privée : scoring, risk, providers, Revolut X, execution-capable locked.",
            "",
            "## 5. Fusion validée",
            "",
            "```text",
            "INITIAL MVP",
            "  Lexique + méthodes + WebApp future",
            "        │",
            "        ├── fusion documentaire",
            "        ├── fusion CDC / roadmap",
            "        ├── fusion opérateur GEM",
            "        └── fusion sécurité / boundaries",
            "        ↓",
            "P122 CURRENT",
            "  Prompt → GEM → Capture → Review Queue → Journal local",
            "```",
            "",
            "## 6. Ce qui n'est PAS fusionné",
            "",
            "- Pas de broker dans MVP.",
            "- Pas d'ordre automatique.",
            "- Pas de sizing automatique.",
            "- Pas d'accès réel Revolut X depuis MVP.",
            "- `NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.",
            "- Pas d'écriture Sheets automatique.",
            "",
            "## 7. Livrables .md emoji",
            "",
            "Les documents avec emoji sont des copies lisibles opérateur. Les documents sans emoji restent les",
            "noms canoniques stables pour scripts, tests et recherche.",
            "",
        ]
    )


def drive_rangement_doc(_: FinalDocsRequest) -> str:
    return _join(
        [
            "# MVP QAIC — Rangement Drive final",
            "",
            "## Principe",
            "",
            "Rangement non destructif : on crée des dossiers canoniques et on ne déplace pas brutalement les anciens exports.",
            "",
            "## Structure locale Drive recommandée",
            "",
            "```text",
            "MVP_QAIC_PY/",
            "├─ 01_DOCS/",
            "│  ├─ FINAL/",
            "│  ├─ CDC/",
            "│  ├─ ROADMAP/",
            "│  ├─ ARCHITECTURE/",
            "│  ├─ DRIVE_RANGEMENT/",
            "│  └─ HANDOFF/",
            "├─ docs/",
            "│  ├─ audit/qaic_migration/",
            "│  └─ qaic_public_contracts/",
            "├─ 05_EXPORTS/",
            "└─ mvp_qaic_py/",
            "```",
            "",
            "## Docs préexistantes intégrées",
            "",
            "- `docs/audit/qaic_migration/`",
            "- `docs/qaic_public_contracts/`",
            "",
            "Ces dossiers sont intégrés à la preuve documentaire P123 sans suppression ni déplacement forcé.",
            "",
        ]
    )


def handoff_doc(request: FinalDocsRequest) -> str:
    return _join(
        [
            "# MVP QAIC — Operator Handoff Final",
            "",
            "## Statut",
            "",
            "P122 a établi le point d'arrêt opérateur. P123 consolide la documentation finale.",
            "",
            "## Commande quotidienne type",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_RUN" --pasted-text-file "portfolio_input.txt" --run-id "DAILY-GEM-RUN"',
            "```",
            "",
            "## Après réponse GEM",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_response_review_queue --output-dir "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE" --response-text-file "gem_response.txt" --source-prompt-run-id "DAILY-GEM-RUN" --response-run-id "DAILY-GEM-RESPONSE"',
            "```",
            "",
            "## Bridge journal local",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_response_decision_journal_bridge --output-dir "05_EXPORTS/DAILY_GEM_JOURNAL_CANDIDATE" --response-capture-json-file "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE/P119_RESPONSE_CAPTURE.json" --journal-entry-id "DAILY-GEM-JOURNAL-CANDIDATE"',
            "```",
            "",
            "## Stop condition",
            "",
            "Stop après documentation, sauf test manuel GEM réel ou helper local d'entrée demandé.",
            "",
            f"Notes : {request.notes or 'Aucune.'}",
            "",
        ]
    )


def index_doc(_: FinalDocsRequest) -> str:
    return _join(
        [
            "# MVP QAIC — Final Docs Index",
            "",
            "## Lecture dans l'ordre",
            "",
            "1. `MVP_QAIC_FINAL_OPERATING_CONTEXT.md`",
            "2. `📚 MVP_QAIC_FINAL_DOCS_INDEX.md`",
            "3. `../ARCHITECTURE/🧬 MVP_QAIC_FUSION_INITIALE_TO_P122_TRACE.md`",
            "4. `../ROADMAP/🗺️ ROADMAP_VISUAL_V0_1_TO_V1_0.md`",
            "5. `../CDC/📘 CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md`",
            "6. `../DRIVE_RANGEMENT/🗂️ MVP_QAIC_DRIVE_RANGEMENT_FINAL.md`",
            "7. `../HANDOFF/🤝 MVP_QAIC_OPERATOR_HANDOFF_FINAL.md`",
            "",
            "## Statut",
            "",
            "Docs finales consolidées après P122. La chaîne locale est opérationnelle pour test manuel.",
            "",
        ]
    )


def build_docs(request: FinalDocsRequest) -> dict[tuple[str, str], str]:
    return {
        ("FINAL", "MVP_QAIC_FINAL_OPERATING_CONTEXT.md"): operating_context_doc(request),
        ("FINAL", "MVP_QAIC_FINAL_DOCS_INDEX.md"): index_doc(request),
        ("FINAL", "📘 MVP_QAIC_FINAL_OPERATING_CONTEXT.md"): operating_context_doc(request),
        ("FINAL", "📚 MVP_QAIC_FINAL_DOCS_INDEX.md"): index_doc(request),
        ("CDC", "CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md"): cdc_roadmap_doc(request),
        ("CDC", "📘 CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md"): cdc_roadmap_doc(request),
        ("ROADMAP", "ROADMAP_VISUAL_V0_1_TO_V1_0.md"): visual_roadmap_doc(request),
        ("ROADMAP", "🗺️ ROADMAP_VISUAL_V0_1_TO_V1_0.md"): visual_roadmap_doc(request),
        ("ARCHITECTURE", "MVP_QAIC_FUSION_ARCHITECTURE_CORRECTIONS.md"): architecture_doc(request),
        ("ARCHITECTURE", "🧩 MVP_QAIC_FUSION_ARCHITECTURE_CORRECTIONS.md"): architecture_doc(
            request
        ),
        (
            "ARCHITECTURE",
            "🧬 MVP_QAIC_FUSION_INITIALE_TO_P122_TRACE.md",
        ): fusion_initial_to_p122_trace_doc(request),
        ("DRIVE_RANGEMENT", "MVP_QAIC_DRIVE_RANGEMENT_FINAL.md"): drive_rangement_doc(request),
        ("DRIVE_RANGEMENT", "🗂️ MVP_QAIC_DRIVE_RANGEMENT_FINAL.md"): drive_rangement_doc(request),
        ("HANDOFF", "MVP_QAIC_OPERATOR_HANDOFF_FINAL.md"): handoff_doc(request),
        ("HANDOFF", "🤝 MVP_QAIC_OPERATOR_HANDOFF_FINAL.md"): handoff_doc(request),
    }


def write_final_docs_pack(request: FinalDocsRequest) -> dict[str, Any]:
    docs_root = Path(request.docs_root)
    output_dir = Path(request.output_dir)
    docs_root.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    docs = build_docs(request)
    docs_files: list[str] = []
    export_files: list[str] = []

    for (folder, filename), content in docs.items():
        docs_path = docs_root / folder / filename
        export_path = output_dir / "01_DOCS_FINAL_COPY" / folder / filename
        _write(docs_path, content)
        _write(export_path, content)
        docs_files.append(str(docs_path))
        export_files.append(str(export_path))

    existing_doc_files = scan_existing_doc_files(request.project_root)

    manifest = {
        "status": "FINAL_DOCS_READY",
        "step": "P123_FINAL_DOCS_CDC_ROADMAP_DRIVE_RANGEMENT",
        "version": VERSION,
        "generated_at_utc": request.generated_at_utc,
        "source_head": request.source_head,
        "docs_root": str(docs_root),
        "output_dir": str(output_dir),
        "doc_count": len(docs_files),
        "true_fusion_initial_to_p122": True,
        "true_fusion_marker": "REAL_FUSION_UPDATED_FROM_INITIAL_VERSION_TO_P122 = TRUE",
        "md_emoji_deliverables": True,
        "existing_docs_integrated": True,
        "existing_doc_dirs": list(EXISTING_DOC_DIRS),
        "existing_doc_files": existing_doc_files,
        "existing_doc_file_count": len(existing_doc_files),
        "docs_files": docs_files,
        "export_files": export_files,
        "project_status": build_project_status(request),
        "safety_markers": list(SAFETY_MARKERS),
        "next": "WAIT_OPERATOR_REAL_GEM_TEST_OR_P124_UI_INPUT_HELPER",
    }

    manifest_path = output_dir / "P123_FINAL_DOCS_MANIFEST.json"
    report_path = output_dir / "P123_FINAL_DOCS_REPORT.md"

    _write_json(manifest_path, manifest)
    _write(
        report_path,
        _join(
            [
                "# P123 Final Docs Report",
                "",
                "- status: FINAL_DOCS_READY",
                f"- version: {VERSION}",
                f"- doc_count: {len(docs_files)}",
                f"- existing_doc_file_count: {len(existing_doc_files)}",
                "- true_fusion_initial_to_p122: true",
                "- md_emoji_deliverables: true",
                "- existing_docs_integrated: true",
                "- safety: DOCS_ONLY / LOCAL_ONLY / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING",
                "",
            ]
        ),
    )

    manifest["export_files"].extend([str(manifest_path), str(report_path)])
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.final_docs_planning_pack",
        description="Generate final docs, CDC roadmap, visual planning, and Drive rangement pack.",
    )
    parser.add_argument("--docs-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--project-root")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--source-head")
    parser.add_argument("--p122-export-dir")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_final_docs_pack(
        FinalDocsRequest(
            docs_root=args.docs_root,
            output_dir=args.output_dir,
            project_root=args.project_root,
            generated_at_utc=args.generated_at_utc,
            source_head=args.source_head,
            p122_export_dir=args.p122_export_dir,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["doc_count"])
    print(result["true_fusion_initial_to_p122"])
    print(result["md_emoji_deliverables"])
    print(result["existing_docs_integrated"])
    print(result["docs_root"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
