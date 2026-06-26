from __future__ import annotations
import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STEP = "P_REFLEX_12F_R3_NO_SCAN_EXPLICIT_REPO_GLOBAL_MIGRATION_MATRIX"
STATUS_LEGEND = {
    "MIGRATE_NOW": {
        "fr": "À migrer maintenant",
        "meaning": "Important pour le MVP privé Reflex/Python.",
    },
    "MIGRATE_LATER": {"fr": "À migrer plus tard", "meaning": "Utile mais non bloquant."},
    "KEEP_SHEETS_MANUAL": {
        "fr": "Garder dans Sheets en contrôle manuel",
        "meaning": "Sheets garde une valeur de revue humaine/export.",
    },
    "KEEP_AS_EXPORT_SOURCE": {
        "fr": "Garder comme source d’export lecture seule",
        "meaning": "Alimente Python/Reflex sans mutation automatique.",
    },
    "PYTHON_REWRITE": {"fr": "Réécrire en Python", "meaning": "Sortir la logique d’Apps Script."},
    "REFLEX_UI_BINDING": {
        "fr": "Brancher dans l’interface Reflex",
        "meaning": "Créer route/panneau/filtre UI.",
    },
    "BIGQUERY_FUTURE_CANDIDATE": {
        "fr": "Candidat BigQuery futur",
        "meaning": "Logs, historiques, snapshots, analytics.",
    },
    "RETIRE_NO_VALUE": {
        "fr": "Ne pas migrer / sans intérêt confirmé",
        "meaning": "Legacy, doublon ou faible valeur.",
    },
    "NO_MIGRATION_NEEDED": {
        "fr": "Pas de migration nécessaire",
        "meaning": "Fichier technique ou déjà couvert.",
    },
    "REVIEW_REQUIRED": {
        "fr": "Revue nécessaire",
        "meaning": "Risque/couverture/dépendance à vérifier.",
    },
}
SEED_SHEETS_COCKPITS = [
    (
        "Mission Control",
        "Cockpit accueil/pilotage MVP",
        "REFLEX_UI_BINDING",
        "REFLEX_UI",
        "Déjà présent partiellement ; compléter liens et statuts.",
    ),
    (
        "Dev Tracking",
        "Lots Pxxx, commits, tags, gates, incidents",
        "MIGRATE_NOW",
        "REFLEX_UI + LOCAL_DOCS",
        "À alimenter depuis Git, 05_EXPORTS et seal reports.",
    ),
    (
        "CDC Tracker",
        "CDC produit / architecture / routes",
        "MIGRATE_NOW",
        "REFLEX_UI + DOCS",
        "Conserver JSON machine + affichage lisible.",
    ),
    (
        "Migration Tracker",
        "Migration Sheets/Apps Script vers Python/Reflex",
        "MIGRATE_NOW",
        "REFLEX_UI + DOCS",
        "Doit devenir la vue globale enrichie par CSV CLASP.",
    ),
    (
        "Auto-update Trackers",
        "Statut sync locale docs/exports/runtime",
        "MIGRATE_NOW",
        "REFLEX_UI",
        "Fondation posée en P12E-R2G.",
    ),
    (
        "Prompt Cockpit",
        "Prompt, contexte, human-review",
        "MIGRATE_NOW",
        "REFLEX_UI + PYTHON",
        "Cœur MVP privé.",
    ),
    (
        "Benchmark AI Trade",
        "Benchmark réponses IA et scoring qualité",
        "MIGRATE_LATER",
        "PYTHON + REFLEX_UI",
        "Secondaire après migration globale.",
    ),
    (
        "Decision Journal",
        "Journal décision human-review",
        "MIGRATE_NOW",
        "PYTHON + LOCAL_EXPORT + FUTURE_BIGQUERY",
        "Préparer export/BigQuery futur.",
    ),
    (
        "Prompt History Library",
        "Bibliothèque prompts/versions",
        "MIGRATE_LATER",
        "PYTHON + REFLEX_UI",
        "Audit prompt et régression.",
    ),
    (
        "Response Draft",
        "Brouillons de réponses/corrections",
        "MIGRATE_LATER",
        "PYTHON + REFLEX_UI",
        "Boucle de correction humaine.",
    ),
    (
        "Lexique / Knowledge Base",
        "Lexique, topics, recherche KB",
        "MIGRATE_NOW",
        "PYTHON + REFLEX_UI",
        "Valeur MVP publique future.",
    ),
    (
        "Runtime Cockpit",
        "État runtime/imports/smokes/ports",
        "MIGRATE_NOW",
        "REFLEX_UI",
        "Essentiel opérateur privé.",
    ),
    (
        "Runtime Bridge Status",
        "Ponts locaux/exports/bridge",
        "MIGRATE_NOW",
        "REFLEX_UI + LOCAL_DOCS",
        "À lier aux trackers auto-update.",
    ),
    (
        "WebApp Readiness",
        "Préparation qualité WebApp",
        "MIGRATE_NOW",
        "REFLEX_UI",
        "Checklist release privée.",
    ),
    (
        "Revolut X Readonly Views",
        "Balances/trades lecture seule",
        "KEEP_SHEETS_MANUAL",
        "SHEETS_EXPORT + FUTURE_PYTHON",
        "Pas d’ordre/sizing ; revue/export seulement.",
    ),
    (
        "Legacy Script Registry",
        "Registre scripts Apps Script",
        "KEEP_AS_EXPORT_SOURCE",
        "LOCAL_CSV + REFLEX_UI",
        "Source inventaire jusqu’à fermeture migration.",
    ),
    (
        "Legacy Sheets Control Tabs",
        "Onglets contrôle historiques",
        "REVIEW_REQUIRED",
        "SHEETS_MANUAL",
        "Ne rien supprimer sans preuve.",
    ),
    (
        "BigQuery Historical Snapshots",
        "Historique, logs, daily snapshots",
        "BIGQUERY_FUTURE_CANDIDATE",
        "BIGQUERY",
        "Volumétrie, audit et backtests.",
    ),
    (
        "BigQuery Decision Facts",
        "Faits décisions et outcomes",
        "BIGQUERY_FUTURE_CANDIDATE",
        "BIGQUERY",
        "Audit décisionnel long terme.",
    ),
]
FEATURE_RULES = {
    "PROMPT_ENGINE": ("MIGRATE_NOW", "PYTHON + REFLEX_UI", "Cœur prompt/human-review MVP."),
    "QAIC_BRIDGE": (
        "PYTHON_REWRITE",
        "PYTHON_SERVICE + READONLY_EXPORT",
        "Logique métier à sortir d’Apps Script.",
    ),
    "KNOWLEDGE_SEARCH": ("MIGRATE_NOW", "PYTHON + REFLEX_UI", "KB/Lexique dans WebApp."),
    "JOURNAL": (
        "MIGRATE_NOW",
        "PYTHON + LOCAL_EXPORT + FUTURE_BIGQUERY",
        "Journal décision traçable hors Sheets.",
    ),
    "SCRIPT_REGISTRY": ("KEEP_AS_EXPORT_SOURCE", "LOCAL_CSV + REFLEX_UI", "Inventaire utile."),
    "AUDIT_INVENTORY": ("KEEP_AS_EXPORT_SOURCE", "LOCAL_DOCS + REFLEX_UI", "Audit et preuves."),
    "SETUP_FOUNDATION": (
        "REVIEW_REQUIRED",
        "PYTHON_REWRITE_OR_RETIRE",
        "Fondation legacy à vérifier.",
    ),
    "IMPORT_SEEDS": ("REVIEW_REQUIRED", "LOCAL_EXPORT", "Import seed souvent one-shot."),
    "FORMATTING": (
        "RETIRE_NO_VALUE",
        "REFLEX_NATIVE_UI",
        "Mise en forme Sheets non migrée telle quelle.",
    ),
    "MANIFEST": ("NO_MIGRATION_NEEDED", "TECHNICAL", "Fichier technique Apps Script."),
}


@dataclass
class MatrixRow:
    row_id: str
    scope: str
    source_name: str
    source_type: str
    module_family: str
    function_name: str
    function_visibility: str
    severity: str
    risk_score: int
    migration_status: str
    migration_status_fr: str
    target_layer: str
    current_coverage: str
    rationale: str
    next_action: str
    evidence: str


def yn(v: Any) -> bool:
    return str(v or "").strip().upper() in {"YES", "TRUE", "1", "Y"}


def status_fr(s: str) -> str:
    return STATUS_LEGEND.get(s, {}).get("fr", s)


def safe_int(v: Any) -> int:
    try:
        return int(float(str(v or "0").replace(",", ".")))
    except Exception:
        return 0


def risk_score(row: dict[str, str]) -> int:
    score = safe_int(row.get("risk_hit_count")) * 2
    sev = str(row.get("severity", "")).upper()
    score += 8 if sev == "HIGH" else 4 if sev == "MEDIUM" else 0
    for k, w in [
        ("writes_sheet_likely", 8),
        ("calls_spreadsheet", 4),
        ("calls_bigquery", 6),
        ("calls_drive", 4),
        ("calls_properties", 3),
        ("has_delete_or_clear_risk", 10),
        ("has_network_logic", 6),
        ("has_trigger_logic", 6),
    ]:
        if yn(row.get(k)):
            score += w
    return score


def classify_script(row):
    family = row.get("module_family") or "<blank>"
    status, target, why = FEATURE_RULES.get(
        family, ("REVIEW_REQUIRED", "REVIEW", "Famille non classée.")
    )
    if risk_score(row) >= 24 and status not in {"NO_MIGRATION_NEEDED", "RETIRE_NO_VALUE"}:
        status = "PYTHON_REWRITE" if family == "QAIC_BRIDGE" else status
        why += " Risque élevé : revue stricte avant retrait ou migration."
    return status, target, why


def classify_function(row):
    family = row.get("module_family") or "<blank>"
    name = row.get("function_name") or ""
    status, target, why = FEATURE_RULES.get(
        family, ("REVIEW_REQUIRED", "REVIEW", "Fonction non classée.")
    )
    lname = name.lower()
    if "menu" in lname or name in {"onOpen", "onInstall"}:
        return (
            "REVIEW_REQUIRED",
            "REFLEX_UI_OR_RETIRE",
            "Fonction menu/trigger : vérifier usage réel.",
        )
    return status, target, why


def read_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_matrix(repo_root: Path):
    csv_path = repo_root / "docs" / "MVPQAIC_CLASP_IMPORTS_ALL.csv"
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)
    raw = read_rows(csv_path)
    out = []
    for i, (name, desc, status, target, why) in enumerate(SEED_SHEETS_COCKPITS, 1):
        out.append(
            MatrixRow(
                f"SHEET_COCKPIT_{i:03d}",
                "SHEETS_COCKPIT",
                name,
                "SEEDED_COCKPIT_OR_PLATFORM_VIEW",
                "SHEETS_OR_TARGET_PLATFORM",
                "",
                "",
                "REVIEW",
                0,
                status,
                status_fr(status),
                target,
                "SEEDED_FROM_PROJECT_CONTEXT_REQUIRES_OPERATOR_REVIEW",
                why,
                "Valider couverture réelle, intérêt métier, puis rattacher à route Reflex ou statut no-migrate.",
                desc,
            )
        )
    scripts = [r for r in raw if r.get("record_type") == "SCRIPT_INVENTORY"]
    funcs = [r for r in raw if r.get("record_type") == "FUNCTION_INDEX"]
    byfam = defaultdict(list)
    for r in scripts:
        byfam[r.get("module_family") or "<blank>"].append(r)
    for i, (fam, items) in enumerate(sorted(byfam.items()), 1):
        status, target, why = FEATURE_RULES.get(
            fam, ("REVIEW_REQUIRED", "REVIEW", "Famille non classée.")
        )
        total_funcs = sum(safe_int(x.get("total_function_count")) for x in items)
        total_risk = sum(safe_int(x.get("risk_hit_count")) for x in items)
        out.append(
            MatrixRow(
                f"FEATURE_CLUSTER_{i:03d}",
                "FEATURE_CLUSTER",
                fam,
                "MODULE_FAMILY_AGGREGATE",
                fam,
                "",
                "",
                "HIGH" if total_risk > 20 else "INFO",
                total_risk,
                status,
                status_fr(status),
                target,
                f"scripts={len(items)} functions={total_funcs} risk_hits={total_risk}",
                why,
                "Décider par famille : migrer, conserver export, réécrire Python, ou retirer.",
                ", ".join(sorted(x.get("script_file_name", "") for x in items)[:8]),
            )
        )
    for i, r in enumerate(scripts, 1):
        status, target, why = classify_script(r)
        flags = [
            k
            for k in [
                "calls_spreadsheet",
                "calls_bigquery",
                "calls_drive",
                "calls_properties",
                "writes_sheet_likely",
                "has_delete_or_clear_risk",
            ]
            if yn(r.get(k))
        ]
        out.append(
            MatrixRow(
                f"APPS_SCRIPT_FILE_{i:03d}",
                "APPS_SCRIPT_FILE",
                r.get("script_file_name") or r.get("script_id") or f"script_{i}",
                "APPS_SCRIPT_FILE",
                r.get("module_family", ""),
                "",
                "",
                r.get("severity", ""),
                risk_score(r),
                status,
                status_fr(status),
                target,
                "DISCOVERED_FROM_CLASP_CSV",
                why,
                "Revue opérateur : confirmer keep/migrate/retire avant suppression ou réécriture.",
                f"functions={r.get('total_function_count', '')} risk_hits={r.get('risk_hit_count', '')} flags={';'.join(flags)}",
            )
        )
    for i, r in enumerate(funcs, 1):
        status, target, why = classify_function(r)
        out.append(
            MatrixRow(
                f"APPS_SCRIPT_FUNCTION_{i:04d}",
                "APPS_SCRIPT_FUNCTION",
                r.get("script_file_name") or r.get("script_id") or "",
                "APPS_SCRIPT_FUNCTION",
                r.get("module_family", ""),
                r.get("function_name") or f"function_{i}",
                r.get("function_visibility", ""),
                r.get("severity", ""),
                0,
                status,
                status_fr(status),
                target,
                "DISCOVERED_FROM_FUNCTION_INDEX",
                why,
                "Grouper par fonctionnalité et confirmer équivalent Python/Reflex ou retrait.",
                f"line={r.get('line_number', '')} prefix={r.get('function_prefix', '')}",
            )
        )
    for i, (name, status, target, why) in enumerate(
        [
            (
                "BigQuery event log",
                "BIGQUERY_FUTURE_CANDIDATE",
                "BIGQUERY",
                "Logs runs/gates/erreurs/smokes.",
            ),
            (
                "BigQuery decision facts",
                "BIGQUERY_FUTURE_CANDIDATE",
                "BIGQUERY",
                "Journal décisionnel et validations humaines.",
            ),
            (
                "BigQuery historical snapshots",
                "BIGQUERY_FUTURE_CANDIDATE",
                "BIGQUERY",
                "Historique pour backtests/audit.",
            ),
            (
                "Python migration service",
                "MIGRATE_LATER",
                "PYTHON_SERVICE",
                "Conversion fonctions Apps Script vers modules Python.",
            ),
            (
                "Reflex migration workbench",
                "MIGRATE_NOW",
                "REFLEX_UI",
                "Interface de tri opérateur des décisions migration.",
            ),
        ],
        1,
    ):
        out.append(
            MatrixRow(
                f"FUTURE_ARCH_{i:03d}",
                "FUTURE_ARCHITECTURE",
                name,
                "TARGET_ARCHITECTURE",
                "FUTURE_PLATFORM",
                "",
                "",
                "INFO",
                0,
                status,
                status_fr(status),
                target,
                "SUGGESTED_OR_PLANNED",
                why,
                "Valider dans CDC puis transformer en contrats de données/tests.",
                "ARCHITECTURE_RECOMMENDATION",
            )
        )
    rows = [asdict(x) for x in out]
    return {
        "step": STEP,
        "status": "GLOBAL_MIGRATION_MATRIX_READY_FOR_OPERATOR_REVIEW",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status_policy": "Keep machine statuses in English; display French labels in UI via migration_status_fr.",
        "source_csv": "docs/MVPQAIC_CLASP_IMPORTS_ALL.csv",
        "legend": STATUS_LEGEND,
        "summary": {
            "total_rows": len(rows),
            "by_scope": dict(Counter(r["scope"] for r in rows).most_common()),
            "by_status": dict(Counter(r["migration_status"] for r in rows).most_common()),
            "by_target_layer": dict(Counter(r["target_layer"] for r in rows).most_common()),
            "by_module_family": dict(Counter(r["module_family"] for r in rows).most_common()),
            "source_csv_rows": len(raw),
            "script_inventory_count": len(scripts),
            "function_index_count": len(funcs),
        },
        "rows": rows,
    }


def write_outputs(repo_root: Path):
    payload = build_matrix(repo_root)
    docs = repo_root / "docs"
    docs.mkdir(exist_ok=True)
    rows = payload["rows"]
    (docs / "MIGRATION_GLOBAL_MATRIX.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (docs / "MIGRATION_GLOBAL_MATRIX_SUMMARY.json").write_text(
        json.dumps(payload["summary"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (docs / "MIGRATION_STATUS_LEGEND.json").write_text(
        json.dumps(payload["legend"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (docs / "MIGRATION_GLOBAL_MATRIX.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    md = [
        "# Matrice globale de migration — Sheets / Apps Script / Python / Reflex / BigQuery",
        "",
        f"- Status: `{payload['status']}`",
        f"- Generated at: `{payload['generated_at']}`",
        "- Politique statuts: statuts machine en anglais + libellés français en UI.",
        "",
        "## Synthèse",
        "",
    ]
    for k, v in payload["summary"].items():
        md.append(f"- `{k}`: `{v}`")
    md += ["", "## Légende statuts", ""]
    for k, m in STATUS_LEGEND.items():
        md.append(f"- `{k}` / {m['fr']} — {m['meaning']}")
    md += ["", "## Premières lignes à revoir", ""]
    selected = [
        r for r in rows if r["scope"] in {"SHEETS_COCKPIT", "FUTURE_ARCHITECTURE"}
    ] + sorted(
        [r for r in rows if r["scope"] == "APPS_SCRIPT_FILE"],
        key=lambda r: r["risk_score"],
        reverse=True,
    )[:30]
    for r in selected[:90]:
        md.append(
            f"- `{r['row_id']}` `{r['scope']}` **{r['source_name']}** → `{r['migration_status']}` ({r['migration_status_fr']}) → `{r['target_layer']}` — {r['rationale']}"
        )
    (docs / "MIGRATION_GLOBAL_MATRIX.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return payload


def patch_route(repo_root: Path):
    package = repo_root / "mvp_qaic_reflex_ui"
    files = list(package.glob("*.py"))
    files.sort(key=lambda p: (p.name != "mvp_qaic_reflex_ui.py", p.name))
    block = """\n# P_REFLEX_12F_BEGIN_GLOBAL_MIGRATION_ROUTE\ntry:\n    from mvp_qaic_reflex_ui.global_migration_page import global_migration_page\n    {app}.add_page(global_migration_page, route="/migration/global", title="Migration globale")\nexcept Exception:\n    pass\n# P_REFLEX_12F_END_GLOBAL_MIGRATION_ROUTE\n"""
    for p in files:
        txt = p.read_text(encoding="utf-8", errors="replace")
        if "/migration/global" in txt:
            return {
                "status": "UNCHANGED_ALREADY_PRESENT",
                "path": p.relative_to(repo_root).as_posix(),
            }
        m = re.search(
            r"(?m)^\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:rx\.)?App\s*\(", txt
        ) or re.search(r"(?m)^\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\.add_page\s*\(", txt)
        if m:
            p.write_text(txt.rstrip() + "\n" + block.format(app=m.group("name")), encoding="utf-8")
            return {
                "status": "PATCHED",
                "path": p.relative_to(repo_root).as_posix(),
                "app_name": m.group("name"),
            }
    c = package / "p_reflex_12f_migration_route_contract.py"
    c.write_text(
        'from __future__ import annotations\nfrom typing import Any\nfrom mvp_qaic_reflex_ui.global_migration_page import global_migration_page\nGLOBAL_MIGRATION_ROUTE = "/migration/global"\ndef register_p12f_global_migration_route(app: Any) -> Any:\n    app.add_page(global_migration_page, route=GLOBAL_MIGRATION_ROUTE, title="Migration globale")\n    return app\n',
        encoding="utf-8",
    )
    return {"status": "FALLBACK_CONTRACT_CREATED", "path": c.relative_to(repo_root).as_posix()}


def write_module_files(repo_root: Path, route_patch: bool):
    pkg = repo_root / "mvp_qaic_reflex_ui"
    tests = repo_root / "tests"
    pkg.mkdir(exist_ok=True)
    tests.mkdir(exist_ok=True)
    (pkg / "migration_global_matrix.py").write_text(
        Path(__file__).read_text(encoding="utf-8"), encoding="utf-8"
    )
    page = """from __future__ import annotations\nfrom pathlib import Path\nfrom typing import Any\nfrom mvp_qaic_reflex_ui.migration_global_matrix import build_matrix\ntry:\n    import reflex as rx\nexcept Exception:  # noqa: BLE001\n    rx = None  # type: ignore[assignment]\nGLOBAL_MIGRATION_ROUTE = "/migration/global"\ndef _require_reflex() -> Any:\n    if rx is None: raise RuntimeError("reflex is required to render this page")\n    return rx\ndef _rows(rows, scope, limit): return [r for r in rows if r.get("scope")==scope][:limit]\ndef global_migration_page() -> Any:\n    reflex=_require_reflex(); payload=build_matrix(Path.cwd()); summary=payload.get("summary",{}); rows=payload.get("rows",[])\n    cockpit=_rows(rows,"SHEETS_COCKPIT",50); future=_rows(rows,"FUTURE_ARCHITECTURE",20); scripts=sorted([r for r in rows if r.get("scope")=="APPS_SCRIPT_FILE"], key=lambda r:int(r.get("risk_score") or 0), reverse=True)[:35]\n    def card(r):\n        return reflex.card(reflex.vstack(reflex.hstack(reflex.badge(str(r.get("scope",""))), reflex.badge(str(r.get("migration_status",""))), reflex.text(str(r.get("migration_status_fr","")), size="2"), spacing="2", flex_wrap="wrap"), reflex.heading(str(r.get("source_name","")), size="3"), reflex.text(str(r.get("target_layer","")), size="2"), reflex.text(str(r.get("rationale","")), size="2"), reflex.text(str(r.get("next_action","")), size="2"), spacing="2"), width="100%")\n    return reflex.container(reflex.vstack(reflex.heading("Migration globale", size="6"), reflex.text("Vue consolidée Sheets, Apps Script, fonctions, fonctionnalités, Python/Reflex et BigQuery futur. Statuts machine anglais + libellés français.", size="2"), reflex.hstack(reflex.badge(f"rows={summary.get('total_rows')}"), reflex.badge(f"scripts={summary.get('script_inventory_count')}"), reflex.badge(f"functions={summary.get('function_index_count')}"), spacing="3", flex_wrap="wrap"), reflex.heading("Cockpits Sheets / vues essentielles", size="4"), *[card(r) for r in cockpit], reflex.heading("Scripts Apps Script prioritaires", size="4"), *[card(r) for r in scripts], reflex.heading("Évolutions architecture / BigQuery", size="4"), *[card(r) for r in future], spacing="4", width="100%"), size="4", padding_y="1.5rem")\n"""
    (pkg / "global_migration_page.py").write_text(page, encoding="utf-8")
    test1 = """from __future__ import annotations\nimport csv\nfrom pathlib import Path\nfrom mvp_qaic_reflex_ui.migration_global_matrix import build_matrix, status_fr, write_outputs\ndef _write_csv(path: Path) -> None:\n    path.parent.mkdir(parents=True, exist_ok=True); fields=["record_type","script_file_name","script_id","module_family","function_name","function_visibility","line_number","severity","total_function_count","risk_hit_count","calls_spreadsheet","writes_sheet_likely"]\n    rows=[{"record_type":"SCRIPT_INVENTORY","script_file_name":"mvpqaic_23_gpt_response_intake_core.js","module_family":"PROMPT_ENGINE","severity":"HIGH","total_function_count":"12","risk_hit_count":"3","calls_spreadsheet":"YES","writes_sheet_likely":"YES"},{"record_type":"FUNCTION_INDEX","script_file_name":"mvpqaic_23_gpt_response_intake_core.js","module_family":"PROMPT_ENGINE","function_name":"MVPQAIC_Run","function_visibility":"PUBLIC","line_number":"10","severity":"INFO"}]\n    with path.open("w", encoding="utf-8", newline="") as f: writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)\ndef test_global_migration_matrix_has_bilingual_status_and_all_scopes(tmp_path: Path) -> None:\n    _write_csv(tmp_path/"docs"/"MVPQAIC_CLASP_IMPORTS_ALL.csv"); payload=build_matrix(tmp_path); scopes={r["scope"] for r in payload["rows"]}\n    assert {"SHEETS_COCKPIT","APPS_SCRIPT_FILE","APPS_SCRIPT_FUNCTION","FEATURE_CLUSTER","FUTURE_ARCHITECTURE"}.issubset(scopes)\n    assert payload["status_policy"].startswith("Keep machine statuses in English"); assert status_fr("MIGRATE_NOW") == "À migrer maintenant"\ndef test_global_migration_matrix_writes_docs_outputs(tmp_path: Path) -> None:\n    _write_csv(tmp_path/"docs"/"MVPQAIC_CLASP_IMPORTS_ALL.csv"); payload=write_outputs(tmp_path); assert payload["summary"]["script_inventory_count"] == 1\n    assert (tmp_path/"docs"/"MIGRATION_GLOBAL_MATRIX.csv").exists(); assert (tmp_path/"docs"/"MIGRATION_GLOBAL_MATRIX.json").exists(); assert (tmp_path/"docs"/"MIGRATION_GLOBAL_MATRIX.md").exists()\n"""
    (tests / "test_p_reflex_12f_global_migration_matrix.py").write_text(test1, encoding="utf-8")
    test2 = """from __future__ import annotations\nfrom pathlib import Path\ndef test_p12f_global_migration_route_or_contract_present() -> None:\n    package=Path.cwd()/"mvp_qaic_reflex_ui"; text="\\n".join(p.read_text(encoding="utf-8", errors="replace") for p in package.glob("*.py"))\n    assert "/migration/global" in text; assert "global_migration_page" in text\ndef test_p12f_statuses_keep_machine_english_and_french_labels() -> None:\n    from mvp_qaic_reflex_ui.migration_global_matrix import STATUS_LEGEND\n    assert "MIGRATE_NOW" in STATUS_LEGEND; assert STATUS_LEGEND["MIGRATE_NOW"]["fr"]; assert "RETIRE_NO_VALUE" in STATUS_LEGEND; assert "BIGQUERY_FUTURE_CANDIDATE" in STATUS_LEGEND\n"""
    (tests / "test_p_reflex_12f_migration_route_contract.py").write_text(test2, encoding="utf-8")
    return {
        "route_result": patch_route(repo_root) if route_patch else {"status": "SKIPPED_BY_PARAM"}
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--route-patch", action="store_true")
    ap.add_argument("--no-route-patch", action="store_true")
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    if args.write:
        payload = write_outputs(repo)
        print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
        return 0
    result = write_module_files(repo, route_patch=args.route_patch and not args.no_route_patch)
    payload = write_outputs(repo)
    result["summary"] = payload["summary"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
