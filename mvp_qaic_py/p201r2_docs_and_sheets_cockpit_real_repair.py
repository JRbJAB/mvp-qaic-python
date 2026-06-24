from __future__ import annotations

import argparse
import csv
import html
import json
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SAFETY_FLAGS = {
    "gem_call_executed": False,
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "real_sheet_write_allowed": False,
}

ROUTES = [
    "/",
    "/prompt",
    "/capture",
    "/responses",
    "/sessions",
    "/roundtrip",
    "/real-case",
    "/migration",
    "/gem-tracking",
    "/gem-tracking-operator",
    "/gem-evidence",
    "/runtime-contract",
    "/operator-release",
    "/real-case-inputs",
    "/prompt-master",
    "/sheets-export",
    "/apps-script-map",
    "/dev-roadmap",
    "/release-final",
    "/migration-control",
    "/instructions",
    "/sheets-cockpit-plan",
    "/docs",
    "/notice",
    "/review",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def _safe_rel(path: Path, base: Path) -> str:
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def _status_color(status: str) -> str:
    s = str(status).upper()
    if any(x in s for x in ["READY", "DONE", "OK", "PASS"]):
        return "🟩"
    if any(x in s for x in ["WAIT", "REVIEW", "FUTURE", "NEXT"]):
        return "🟧"
    if any(x in s for x in ["BLOCK", "FAIL", "ERROR", "STOP"]):
        return "🟥"
    return "🟦"


def build_sheets_cockpit_plan() -> list[dict[str, Any]]:
    rows = [
        (
            "QAIC_OPERATOR_COCKPIT",
            "COCKPIT",
            "Vue décisionnelle principale",
            "status, next_action, blocker_count, route, evidence",
            "Créer cockpit opérateur compact en haut",
            "READY_DESIGN",
        ),
        (
            "MIGRATION_CONTROL",
            "COCKPIT",
            "Suivi fait / reste à faire pour onglets, scripts, fonctions",
            "entity_type, name, done, todo, status, color_cell, progress_percent",
            "Priorité affichage en tableau coloré",
            "READY_DESIGN",
        ),
        (
            "INSTRUCTIONS_TRACKER",
            "GOVERNANCE",
            "Suivi des obligations par thème",
            "theme, obligation, status, evidence, correction_rule",
            "Obligatoire avant chaque batch sensible",
            "READY_DESIGN",
        ),
        (
            "DOCS_INDEX",
            "DOCUMENTATION",
            "Index des docs repo + dossier principal",
            "doc_id, scope, path, version, merge_action",
            "Fusionner docs finales/résiduelles",
            "READY_DESIGN",
        ),
        (
            "DOCS_FINAL_FUSED",
            "DOCUMENTATION",
            "Référence documentaire finale",
            "section, version, status, source, updated_at",
            "Miroir dans dossier principal",
            "READY_DESIGN",
        ),
        (
            "GEM_CAPTURE_INBOX",
            "GEM",
            "Réception capture portfolio",
            "capture_id, file_path, timestamp, status",
            "Entrée vraie capture opérateur",
            "READY_DESIGN",
        ),
        (
            "GEM_RESPONSE_INBOX",
            "GEM",
            "Réception réponse GEM",
            "response_id, source_file, parse_status, blockers",
            "Entrée réponse GEM réelle",
            "READY_DESIGN",
        ),
        (
            "GEM_SESSION_LOG",
            "GEM",
            "Sessions prompt / capture / réponse",
            "session_id, prompt_id, capture_id, response_id",
            "Audit roundtrip",
            "READY_DESIGN",
        ),
        (
            "GEM_ROUNDTRIP_STATUS",
            "GEM",
            "Statut roundtrip complet",
            "roundtrip_id, capture_ok, response_ok, review_ok",
            "Détecter où ça bloque",
            "REVIEW",
        ),
        (
            "GEM_REVIEW_GATE",
            "REVIEW",
            "Gate de revue humaine",
            "review_id, status, missing_data, blockers",
            "Jamais auto-apply",
            "READY_DESIGN",
        ),
        (
            "GEM_REAL_CASE_DECISION",
            "REVIEW",
            "Décision cas réel portfolio",
            "decision_id, human_decision, reason, approved",
            "Validation opérateur",
            "WAITING_INPUTS",
        ),
        (
            "GEM_DECISION_JOURNAL",
            "JOURNAL",
            "Journal décisions GEM",
            "decision_id, timestamp, action, evidence, no_order",
            "Trace finale",
            "REVIEW",
        ),
        (
            "PROMPT_MASTER",
            "PROMPT",
            "Prompt source actuel",
            "prompt_id, version, status, patch_marker",
            "Source à protéger",
            "READY_DESIGN",
        ),
        (
            "PROMPT_HISTORY_LIBRARY",
            "PROMPT",
            "Historique versions prompt",
            "prompt_id, source, version, status",
            "Comparer sans casser",
            "READY_DESIGN",
        ),
        (
            "PROMPT_MIGRATION_MATRIX",
            "PROMPT",
            "Migration prompts historiques",
            "source, candidate, action, status",
            "Fusionner/réviser",
            "READY_DESIGN",
        ),
        (
            "RUNTIME_MIGRATION_TRACKER",
            "MIGRATION",
            "Suivi migration runtime",
            "layer, module, route, status, percent",
            "Pilotage migration",
            "READY_DESIGN",
        ),
        (
            "GEM_TRACKING_BINDING_MATRIX",
            "MIGRATION",
            "Binding GEM ↔ Python ↔ Sheets",
            "layer, python_module, sheet_tab, route",
            "Vérifier couverture",
            "READY_DESIGN",
        ),
        (
            "GEM_TRACKING_OPERATOR_VIEW",
            "COCKPIT",
            "Vue opérateur GEM",
            "layer, status, action, evidence",
            "Décision rapide",
            "READY_DESIGN",
        ),
        (
            "GEM_EVIDENCE_BINDING",
            "EVIDENCE",
            "Liens preuves / exports",
            "evidence_id, source, file, status",
            "Audit preuve",
            "READY_DESIGN",
        ),
        (
            "SHEETS_EXPORT_CONTRACT",
            "EXPORT",
            "Contrat export Sheets dry-run",
            "sheet_tab, headers, source, write_allowed",
            "Préparer sans écrire",
            "READY_DESIGN",
        ),
        (
            "SAFETY_FLAGS_AUDIT",
            "SAFETY",
            "Audit flags sécurité",
            "flag, expected, actual, status",
            "Bloquer live non autorisé",
            "READY_DESIGN",
        ),
        (
            "RELEASE_RUNBOOK",
            "RELEASE",
            "Notice opérateur / lancement",
            "step, command, url, status",
            "Usage simple",
            "READY_DESIGN",
        ),
    ]
    out = []
    for idx, (tab, cat, purpose, fields, action, status) in enumerate(rows, 1):
        out.append(
            {
                "priority": idx,
                "sheet_tab": tab,
                "category": cat,
                "purpose": purpose,
                "key_fields": fields,
                "ui_requirements": "freeze header, filters, compact columns, color status, action visible left",
                "data_source": "MVP_QAIC_PY_LOCAL_EXPORTS_THEN_SHEETS_DRY_RUN",
                "status": status,
                "color_cell": _status_color(status),
                "progress_percent": 100
                if status == "READY_DESIGN"
                else 70
                if status == "REVIEW"
                else 45,
                "next_action": action,
                "write_policy": "DRY_RUN_ONLY_NO_LIVE_WRITE",
            }
        )
    return out


def scan_docs(project_root: Path, main_folder: Path | None) -> list[dict[str, Any]]:
    rows = []
    sources = [(project_root, "REPO")]
    if main_folder and main_folder.exists():
        sources.append((main_folder, "MAIN_FOLDER"))

    allowed = {".md", ".html", ".css", ".json", ".csv", ".txt"}
    for base, scope in sources:
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in allowed:
                continue
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            rel = _safe_rel(path, base)
            name = path.name.upper()
            final = "FINAL" in rel.upper() or "NOTICE" in name or "README" in name
            residual = "05_EXPORTS" in rel.upper() or "P1" in name or "P2" in name
            status = (
                "FINAL_CANDIDATE" if final else "RESIDUAL_TO_REVIEW" if residual else "DOC_INDEXED"
            )
            rows.append(
                {
                    "doc_id": f"DOC-{len(rows) + 1:04d}",
                    "scope": scope,
                    "relative_path": rel,
                    "filename": path.name,
                    "suffix": path.suffix.lower(),
                    "doc_status": status,
                    "merge_action": "KEEP_FINAL_OR_MIRROR" if final else "REVIEW_OR_MERGE",
                    "color_cell": _status_color(status),
                }
            )
            if len(rows) >= 800:
                return rows
    return rows


def css_text() -> str:
    return (
        """
:root{--bg:#0f172a;--panel:#111827;--text:#e5e7eb;--muted:#94a3b8;--green:#22c55e;--orange:#f59e0b;--red:#ef4444;--blue:#38bdf8}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI","Noto Sans","DejaVu Sans",Arial,sans-serif;background:#0f172a;color:var(--text);-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
header,main,footer{max-width:1280px;margin:auto;padding:24px}
h1{font-size:34px;margin:0 0 8px;line-height:1.2}
p,li,td,th{line-height:1.45}
.card{background:#111827;border:1px solid rgba(255,255,255,.09);border-radius:16px;padding:16px;margin:10px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
.metric{font-size:30px;font-weight:800}
.badge{display:inline-block;border-radius:999px;padding:5px 10px;margin:3px;font-size:12px;font-weight:700}
.green{background:rgba(34,197,94,.18);color:#86efac}.orange{background:rgba(245,158,11,.18);color:#fcd34d}.red{background:rgba(239,68,68,.18);color:#fca5a5}.blue{background:rgba(56,189,248,.18);color:#7dd3fc}
table{width:100%;border-collapse:collapse;background:#111827;border-radius:12px;overflow:hidden}
th,td{padding:8px 10px;border-bottom:1px solid rgba(255,255,255,.07);vertical-align:top}
th{background:rgba(255,255,255,.05);color:#cbd5e1}
a{color:#7dd3fc}
.code{font-family:Consolas,monospace;background:#020617;border:1px solid rgba(255,255,255,.08);padding:12px;border-radius:12px;overflow:auto}
""".strip()
        + "\n"
    )


def notice_html(summary: dict[str, Any], root: Path) -> str:
    routes = [
        ("/dev-roadmap", "Roadmap visuelle"),
        ("/migration-control", "Cockpit migration : onglets, scripts, fonctions"),
        ("/sheets-cockpit-plan", "Plan des onglets Sheets utiles"),
        ("/instructions", "Obligations / instructions"),
        ("/docs", "Index documentaire"),
        ("/notice", "Notice"),
        ("/release-final", "Release final"),
    ]
    rows = "\n".join(
        f"<tr><td><a href='http://127.0.0.1:8080{r}'>{r}</a></td><td>{html.escape(label)}</td></tr>"
        for r, label in routes
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>MVP QAIC — Notice d’utilisation</title>
<link rel="stylesheet" href="MVP_QAIC_NOTICE_UTILISATION.css">
</head>
<body>
<header>
<h1>MVP QAIC — Notice d’utilisation</h1>
<p>Interface locale privée. Les accents doivent s’afficher correctement : é è à ç ù œ.</p>
<span class="badge green">HUMAN_REVIEW_ONLY</span><span class="badge red">NO LIVE WRITE</span><span class="badge red">NO BROKER</span>
</header>
<main>
<section class="grid">
<div class="card"><div class="metric">{summary.get("doc_count", 0)}</div><p>documents indexés</p></div>
<div class="card"><div class="metric">{summary.get("sheet_cockpit_tab_count", 0)}</div><p>onglets Sheets utiles prévus</p></div>
<div class="card"><div class="metric">{summary.get("residual_doc_count", 0)}</div><p>docs résiduelles à revoir/fusionner</p></div>
</section>
<h2>Démarrer NiceGUI</h2>
<div class="code">cd "{root}"<br>python -m mvp_qaic_py.p173_nicegui_private_local_runner --project-root . --host 127.0.0.1 --port 8080 --serve-private</div>
<h2>Liens utiles</h2>
<table><thead><tr><th>Route</th><th>Usage</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Règles</h2>
<ul>
<li>Aucun ordre, aucun sizing, aucun broker.</li>
<li>Aucune écriture Google Sheets / Apps Script / CLASP sans autorisation explicite.</li>
<li>Les docs finales sont dans <b>docs/FINAL</b> et en miroir dans le dossier principal.</li>
<li>Les onglets Sheets décrits sont des cockpits utiles à créer/importer plus tard, pas des routes Python.</li>
</ul>
</main>
<footer>Généré {html.escape(_utc_now())}</footer>
</body>
</html>
"""


def final_docs_md(summary: dict[str, Any]) -> str:
    return f"""# MVP QAIC — Documentation finale fusionnée

Statut : `FINAL_FUSED_DRAFT_READY`

## Ce document règle

- Gestion documentaire dans `MVP_QAIC_PY/docs`.
- Miroir documentaire dans le dossier principal MVP QAIC.
- Notice HTML/CSS d’utilisation.
- Plan des onglets Sheets utiles et nécessaires.
- Liste des versions résiduelles à fusionner/revoir.

## Chiffres

- Documents indexés : `{summary.get("doc_count", 0)}`
- Documents résiduels : `{summary.get("residual_doc_count", 0)}`
- Onglets Sheets utiles planifiés : `{summary.get("sheet_cockpit_tab_count", 0)}`

## Priorités d’onglets Sheets

1. `QAIC_OPERATOR_COCKPIT`
2. `MIGRATION_CONTROL`
3. `INSTRUCTIONS_TRACKER`
4. `DOCS_INDEX`
5. `GEM_CAPTURE_INBOX`
6. `GEM_RESPONSE_INBOX`
7. `GEM_REVIEW_GATE`
8. `GEM_DECISION_JOURNAL`
9. `PROMPT_MASTER`
10. `RUNTIME_MIGRATION_TRACKER`

## Sécurité

- `GOOGLE_SHEETS_WRITE=False`
- `APPS_SCRIPT_EXECUTION=False`
- `CLASP_PUSH=False`
- `BROKER=False`
- `ORDER=False`
- `SIZING=False`
"""


def build_payload(
    project_root: str | Path, main_folder: str | Path | None = None
) -> dict[str, Any]:
    root = Path(project_root)
    main = Path(main_folder) if main_folder else None
    sheet_rows = build_sheets_cockpit_plan()
    doc_rows = scan_docs(root, main)
    residual = [row for row in doc_rows if row["merge_action"] == "REVIEW_OR_MERGE"]
    return {
        "STATUS": "OK_P201R2_DOCS_AND_SHEETS_COCKPIT_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "main_folder": str(main) if main else "",
        "main_folder_exists": bool(main and main.exists()),
        "sheet_cockpit_rows": sheet_rows,
        "doc_rows": doc_rows,
        "residual_doc_rows": residual,
        "sheet_cockpit_tab_count": len(sheet_rows),
        "doc_count": len(doc_rows),
        "residual_doc_count": len(residual),
        **SAFETY_FLAGS,
        "recommended_next": "P202_UI_REAL_SCREEN_VALIDATION_AND_SHEETS_IMPORT_REVIEW",
    }


def export_payload(
    project_root: str | Path, main_folder: str | Path, export_dir: str | Path | None = None
) -> dict[str, Any]:
    root = Path(project_root)
    main = Path(main_folder)
    export = (
        Path(export_dir)
        if export_dir
        else root / "05_EXPORTS" / f"P201R2_DOCS_SHEETS_COCKPIT_{_stamp()}"
    )
    export.mkdir(parents=True, exist_ok=True)

    payload = build_payload(root, main)

    docs_final = root / "docs" / "FINAL"
    docs_index = root / "docs" / "INDEX"
    docs_gov = root / "docs" / "GOVERNANCE"
    for folder in [docs_final, docs_index, docs_gov]:
        folder.mkdir(parents=True, exist_ok=True)

    summary = {
        "STATUS": payload["STATUS"],
        "generated_at": payload["generated_at"],
        "doc_count": payload["doc_count"],
        "residual_doc_count": payload["residual_doc_count"],
        "sheet_cockpit_tab_count": payload["sheet_cockpit_tab_count"],
        "main_folder_exists": payload["main_folder_exists"],
        **SAFETY_FLAGS,
        "recommended_next": payload["recommended_next"],
    }

    (docs_final / "MVP_QAIC_NOTICE_UTILISATION.css").write_text(css_text(), encoding="utf-8")
    (docs_final / "MVP_QAIC_NOTICE_UTILISATION.html").write_text(
        notice_html(summary, root), encoding="utf-8"
    )
    (docs_final / "MVP_QAIC_DOCS_FINAL_FUSED.md").write_text(
        final_docs_md(summary), encoding="utf-8"
    )
    _write_csv(
        docs_final / "MVP_QAIC_SHEETS_COCKPIT_BLUEPRINT.csv",
        payload["sheet_cockpit_rows"],
        [
            "priority",
            "sheet_tab",
            "category",
            "purpose",
            "key_fields",
            "ui_requirements",
            "data_source",
            "status",
            "color_cell",
            "progress_percent",
            "next_action",
            "write_policy",
        ],
    )
    (docs_final / "MVP_QAIC_SHEETS_COCKPIT_BLUEPRINT.md").write_text(
        "# MVP QAIC — Plan des onglets Sheets utiles\n\n"
        + "\n".join(
            f"- `{r['sheet_tab']}` — {r['purpose']} — `{r['status']}`"
            for r in payload["sheet_cockpit_rows"]
        )
        + "\n",
        encoding="utf-8",
    )
    _write_csv(
        docs_index / "MVP_QAIC_DOC_INDEX.csv",
        payload["doc_rows"],
        [
            "doc_id",
            "scope",
            "relative_path",
            "filename",
            "suffix",
            "doc_status",
            "merge_action",
            "color_cell",
        ],
    )
    _write_csv(
        docs_index / "MVP_QAIC_RESIDUAL_DOCS_TO_MERGE.csv",
        payload["residual_doc_rows"],
        [
            "doc_id",
            "scope",
            "relative_path",
            "filename",
            "suffix",
            "doc_status",
            "merge_action",
            "color_cell",
        ],
    )
    _write_json(docs_index / "MVP_QAIC_DOC_INDEX.json", payload)
    (docs_gov / "MVP_QAIC_DOC_GOVERNANCE.md").write_text(
        "# MVP QAIC — Gouvernance documentaire\n\n- docs/FINAL = final local.\n- docs/INDEX = index et résiduels.\n- Dossier principal = miroir opérateur.\n- Aucune suppression automatique.\n",
        encoding="utf-8",
    )

    main_target = main / "01_DOCS" / "FINAL_FUSED" / "MVP_QAIC_PY"
    main_target.mkdir(parents=True, exist_ok=True)
    mirrored = []
    for source in [
        docs_final / "MVP_QAIC_NOTICE_UTILISATION.css",
        docs_final / "MVP_QAIC_NOTICE_UTILISATION.html",
        docs_final / "MVP_QAIC_DOCS_FINAL_FUSED.md",
        docs_final / "MVP_QAIC_SHEETS_COCKPIT_BLUEPRINT.csv",
        docs_final / "MVP_QAIC_SHEETS_COCKPIT_BLUEPRINT.md",
        docs_index / "MVP_QAIC_DOC_INDEX.csv",
        docs_index / "MVP_QAIC_RESIDUAL_DOCS_TO_MERGE.csv",
        docs_gov / "MVP_QAIC_DOC_GOVERNANCE.md",
    ]:
        target = main_target / source.name
        shutil.copy2(source, target)
        mirrored.append(str(target))

    payload.update(
        {
            "export_dir": str(export),
            "main_mirror_dir": str(main_target),
            "main_mirror_files": mirrored,
            "main_folder_write_ok": True,
        }
    )
    _write_json(export / "P201R2_DOCS_SHEETS_COCKPIT.json", payload)
    _write_json(
        export / "P201R2_SUMMARY.json",
        {
            **summary,
            "export_dir": str(export),
            "main_mirror_dir": str(main_target),
            "main_folder_write_ok": True,
        },
    )
    _write_csv(
        export / "P201R2_SHEETS_COCKPIT_BLUEPRINT.csv",
        payload["sheet_cockpit_rows"],
        [
            "priority",
            "sheet_tab",
            "category",
            "purpose",
            "key_fields",
            "ui_requirements",
            "data_source",
            "status",
            "color_cell",
            "progress_percent",
            "next_action",
            "write_policy",
        ],
    )
    _write_csv(
        export / "P201R2_DOC_INDEX.csv",
        payload["doc_rows"],
        [
            "doc_id",
            "scope",
            "relative_path",
            "filename",
            "suffix",
            "doc_status",
            "merge_action",
            "color_cell",
        ],
    )
    (export / "P201R2_REPORT.md").write_text(final_docs_md(summary), encoding="utf-8")
    return payload


def _http_ok(url: str) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P201R2"})
    for timeout in (12.0, 24.0):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return 200 <= int(response.status) < 500
        except Exception:
            time.sleep(0.5)
    return False


def route_smoke(project_root: str | Path, port: int = 8113) -> dict[str, Any]:
    root = Path(project_root)
    cmd = [
        sys.executable,
        "-m",
        "mvp_qaic_py.p173_nicegui_private_local_runner",
        "--project-root",
        str(root),
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--serve-private",
        "--no-show",
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    results = []
    ok = False
    try:
        start = time.time()
        while time.time() - start < 180:
            if proc.poll() is not None:
                break
            results = [{"route": r, "ok": _http_ok(f"http://127.0.0.1:{port}{r}")} for r in ROUTES]
            if all(x["ok"] for x in results):
                ok = True
                break
            time.sleep(1.5)
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
    return {
        "route_smoke_ok": ok,
        "route_success_count": sum(1 for x in results if x["ok"]),
        "route_results": results,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", default=".")
    p.add_argument("--main-folder", required=False)
    p.add_argument("--export-dir", default=None)
    p.add_argument("--write-export", action="store_true")
    p.add_argument("--run-route-smoke", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    payload = (
        export_payload(args.project_root, args.main_folder, args.export_dir)
        if args.write_export
        else build_payload(args.project_root, args.main_folder)
    )
    if args.run_route_smoke:
        payload.update(route_smoke(args.project_root))
        if "export_dir" in payload:
            _write_json(
                Path(payload["export_dir"]) / "P201R2_SUMMARY.json",
                {
                    "STATUS": "OK_P201R2_ROUTE_SMOKE"
                    if payload["route_smoke_ok"]
                    else "BLOCKED_P201R2_ROUTE_SMOKE",
                    "doc_count": payload["doc_count"],
                    "residual_doc_count": payload["residual_doc_count"],
                    "sheet_cockpit_tab_count": payload["sheet_cockpit_tab_count"],
                    "main_folder_write_ok": payload.get("main_folder_write_ok", False),
                    "route_success_count": payload["route_success_count"],
                    "route_smoke_ok": payload["route_smoke_ok"],
                    **SAFETY_FLAGS,
                    "recommended_next": payload["recommended_next"],
                },
            )
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
    return (
        0
        if payload.get("sheet_cockpit_tab_count", 0) >= 20 and not payload["google_sheets_write"]
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
