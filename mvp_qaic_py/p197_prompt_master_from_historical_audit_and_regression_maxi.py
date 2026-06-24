from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
    "/review",
]

SAFETY_FLAGS: dict[str, bool] = {
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
    "source_prompt_modified": False,
}


REGRESSION_RULES: list[dict[str, str]] = [
    {
        "check_id": "NO_INVENTED_PORTFOLIO_NUMBERS",
        "severity": "BLOCKING",
        "rule": "Ne jamais inventer prix, PRU, quantité, PnL, exposition, TP/SL.",
    },
    {
        "check_id": "IMAGE_AND_TEXT_SINGLE_RESPONSE",
        "severity": "BLOCKING",
        "rule": "La capture image fait partie du prompt principal, pas d'étape préliminaire séparée.",
    },
    {
        "check_id": "FRENCH_NARRATIVE_KEEP_JSON_KEYS",
        "severity": "HIGH",
        "rule": "Réponse en français, clés JSON/enums techniques conservés exactement.",
    },
    {
        "check_id": "USD_REFERENCE_CURRENCY",
        "severity": "HIGH",
        "rule": "Devise de référence USD sauf preuve contraire explicite.",
    },
    {
        "check_id": "HUMAN_REVIEW_ONLY",
        "severity": "BLOCKING",
        "rule": "Toujours review-only, jamais ordre, sizing automatique, broker ou exécution réelle.",
    },
    {
        "check_id": "NO_SHEETS_OR_APPS_SCRIPT_SIDE_EFFECT",
        "severity": "BLOCKING",
        "rule": "Aucune écriture Sheets, Apps Script, CLASP, trigger, déploiement public.",
    },
    {
        "check_id": "GEM_RESPONSE_NOT_AUTO_APPLIED",
        "severity": "BLOCKING",
        "rule": "Une réponse GEM est analysée, jamais appliquée automatiquement au prompt source.",
    },
    {
        "check_id": "MISSING_DATA_EXPLICIT",
        "severity": "HIGH",
        "rule": "Marquer les champs manquants REVIEW/UNKNOWN au lieu d'inférer.",
    },
    {
        "check_id": "OUTPUT_HAS_OPERATOR_DECISION",
        "severity": "MEDIUM",
        "rule": "La sortie doit proposer un statut de décision opérateur et les bloqueurs.",
    },
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _sha12(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:12]


def _read_text_limited(path: Path, limit: int = 6000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except Exception:
        return ""


def _classification(path: Path, text: str) -> str:
    rel = path.as_posix().lower()
    lowered = text.lower()
    if "multimodal_gem_image_prompt_usd_contract" in rel:
        return "ACTIVE_RUNTIME_PROMPT"
    if "p189h" in rel or "historical_prompt" in rel or "prompt_migration" in rel:
        return "HISTORICAL_AUDIT_PROMPT"
    if "p182" in rel or "prompt_history" in rel:
        return "PROMPT_LIBRARY_REFERENCE"
    if "prompt" in rel and "05_exports" in rel:
        return "PROMPT_EXPORT_REFERENCE"
    if "prompt" in rel:
        return "PROMPT_SOURCE_CANDIDATE"
    if "gem" in lowered and "json" in lowered:
        return "GEM_RESPONSE_RELATED"
    return "REVIEW_CANDIDATE"


def _score_candidate(path: Path, text: str, classification: str) -> int:
    rel = path.as_posix().lower()
    lowered = text.lower()
    score = 0

    if classification == "ACTIVE_RUNTIME_PROMPT":
        score += 55
    elif classification == "HISTORICAL_AUDIT_PROMPT":
        score += 35
    elif classification == "PROMPT_LIBRARY_REFERENCE":
        score += 30
    elif classification == "PROMPT_EXPORT_REFERENCE":
        score += 24
    elif classification == "PROMPT_SOURCE_CANDIDATE":
        score += 20

    for keyword, points in [
        ("portfolio", 8),
        ("image", 7),
        ("capture", 7),
        ("usd", 6),
        ("json", 6),
        ("review_required", 6),
        ("human", 5),
        ("no broker", 8),
        ("no order", 8),
        ("no sizing", 8),
        ("gem", 5),
        ("réponds en français", 5),
        ("french", 3),
    ]:
        if keyword in lowered:
            score += points

    if path.suffix.lower() == ".py":
        score += 3
    if "05_exports" in rel:
        score -= 2
    if len(text) > 800:
        score += 5

    return max(0, min(score, 100))


def _decision(score: int, classification: str) -> str:
    if classification == "ACTIVE_RUNTIME_PROMPT" and score >= 80:
        return "MASTER_BASE_CANDIDATE"
    if score >= 75:
        return "MERGE_INTO_MASTER_REVIEW"
    if score >= 55:
        return "REFERENCE_REVIEW"
    if score >= 35:
        return "ARCHIVE_OR_LOW_PRIORITY_REVIEW"
    return "IGNORE_OR_TECHNICAL_ARTIFACT"


def _iter_prompt_files(root: Path) -> list[Path]:
    allowed_suffixes = {".py", ".md", ".txt", ".json", ".csv"}
    roots = [
        root / "mvp_qaic_py",
        root / "05_EXPORTS",
        root / "00_OPERATOR_EXPORTS",
    ]
    files: list[Path] = []
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if len(files) >= 500:
                break
            if not path.is_file():
                continue
            if path.name.lower() == "desktop.ini":
                continue
            if path.suffix.lower() not in allowed_suffixes:
                continue
            rel = _safe_rel(path, root).lower()
            if any(
                term in rel for term in ["prompt", "gem", "p182", "p189h", "p197", "multimodal"]
            ):
                files.append(path)
    return sorted(set(files), key=lambda item: _safe_rel(item, root))


def build_prompt_master_historical_regression(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    candidates: list[dict[str, Any]] = []

    for path in _iter_prompt_files(root):
        text = _read_text_limited(path)
        if not text:
            continue
        classification = _classification(path, text)
        score = _score_candidate(path, text, classification)
        candidate = {
            "candidate_id": f"PROMPT_{len(candidates) + 1:04d}_{_sha12(_safe_rel(path, root))}",
            "source_path": _safe_rel(path, root),
            "classification": classification,
            "score": score,
            "decision": _decision(score, classification),
            "sha12": _sha12(text),
            "size_chars_sampled": len(text),
            "contains_no_broker": "no broker" in text.lower() or "broker=false" in text.lower(),
            "contains_no_order": "no order" in text.lower() or "order=false" in text.lower(),
            "contains_no_sizing": "no sizing" in text.lower() or "sizing=false" in text.lower(),
            "contains_usd": "usd" in text.lower(),
            "contains_json": "json" in text.lower(),
        }
        candidates.append(candidate)

    candidates.sort(
        key=lambda row: (
            -int(row["score"]),
            str(row["classification"]),
            str(row["source_path"]),
        )
    )

    selected = (
        candidates[0]
        if candidates
        else {
            "candidate_id": "",
            "source_path": "",
            "classification": "NONE",
            "score": 0,
            "decision": "BLOCKED_NO_PROMPT_CANDIDATE",
            "sha12": "",
        }
    )

    regression_checks: list[dict[str, Any]] = []
    selected_text = ""
    if selected.get("source_path"):
        selected_text = _read_text_limited(root / str(selected["source_path"]), limit=12000)

    lowered = selected_text.lower()
    for rule in REGRESSION_RULES:
        status = "PASS"
        if rule["severity"] == "BLOCKING":
            if rule["check_id"] == "NO_INVENTED_PORTFOLIO_NUMBERS" and "invent" not in lowered:
                status = "REVIEW_REQUIRED"
            if rule["check_id"] == "HUMAN_REVIEW_ONLY" and not (
                "human" in lowered or "review" in lowered
            ):
                status = "REVIEW_REQUIRED"
            if rule["check_id"] == "NO_SHEETS_OR_APPS_SCRIPT_SIDE_EFFECT" and not (
                "sheet" in lowered or "apps script" in lowered or "clasp" in lowered
            ):
                status = "REVIEW_REQUIRED"
            if rule["check_id"] == "GEM_RESPONSE_NOT_AUTO_APPLIED" and "auto" not in lowered:
                status = "REVIEW_REQUIRED"

        regression_checks.append({**rule, "status": status})

    blocking_review_count = sum(
        1 for row in regression_checks if row["severity"] == "BLOCKING" and row["status"] != "PASS"
    )

    master_status = (
        "MASTER_CANDIDATE_READY_FOR_HUMAN_REVIEW"
        if selected.get("candidate_id") and blocking_review_count <= 4
        else "REVIEW_REQUIRED_BEFORE_MASTER"
    )

    blockers: list[str] = []
    if not candidates:
        blockers.append("NO_PROMPT_CANDIDATES_FOUND")
    if not selected.get("candidate_id"):
        blockers.append("NO_SELECTED_MASTER_CANDIDATE")

    return {
        "STATUS": "OK_P197_PROMPT_MASTER_HISTORICAL_REGRESSION_READY"
        if not blockers
        else "BLOCKED_P197_PROMPT_MASTER_HISTORICAL_REGRESSION",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "candidate_count": len(candidates),
        "master_status": master_status,
        "selected_master_candidate": selected,
        "candidates": candidates,
        "regression_check_count": len(regression_checks),
        "blocking_review_count": blocking_review_count,
        "regression_checks": regression_checks,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "prompt_source_modified": False,
        **SAFETY_FLAGS,
        "recommended_next": "P198_SHEETS_EXPORT_DRY_RUN_CONTRACT_PACK_MAXI",
        "parallel_waiting_next": "P196B_REAL_CASE_PORTFOLIO_GEM_REVIEW_AFTER_OPERATOR_INPUTS_MAXI_AFTER_INPUTS",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_prompt_master_historical_regression(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P197_PROMPT_MASTER_HISTORICAL_REGRESSION_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_prompt_master_historical_regression(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P197_PROMPT_MASTER_HISTORICAL_REGRESSION.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    candidate_fields = [
        "candidate_id",
        "source_path",
        "classification",
        "score",
        "decision",
        "sha12",
        "size_chars_sampled",
        "contains_no_broker",
        "contains_no_order",
        "contains_no_sizing",
        "contains_usd",
        "contains_json",
    ]
    _write_csv(
        export_path / "P197_PROMPT_MASTER_CANDIDATES.csv", payload["candidates"], candidate_fields
    )

    _write_csv(
        export_path / "P197_PROMPT_REGRESSION_CHECKLIST.csv",
        payload["regression_checks"],
        ["check_id", "severity", "status", "rule"],
    )

    selected = payload["selected_master_candidate"]
    master_md = [
        "# P197 Prompt Master Candidate",
        "",
        f"- master_status: {payload['master_status']}",
        f"- candidate_id: {selected.get('candidate_id', '')}",
        f"- source_path: {selected.get('source_path', '')}",
        f"- classification: {selected.get('classification', '')}",
        f"- score: {selected.get('score', 0)}",
        f"- decision: {selected.get('decision', '')}",
        "",
        "## Important",
        "- Review-only candidate.",
        "- No prompt source modification.",
        "- No GEM call.",
        "- No Sheets write.",
        "- No broker/order/sizing.",
        "",
        "## Next",
        f"- {payload['recommended_next']}",
    ]
    (export_path / "P197_PROMPT_MASTER_CANDIDATE.md").write_text(
        "\n".join(master_md) + "\n",
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "candidate_count",
        "master_status",
        "regression_check_count",
        "blocking_review_count",
        "blocker_count",
        "blockers",
        "prompt_source_modified",
        "gem_call_executed",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "auto_apply_gem_response",
        "source_prompt_modified",
        "recommended_next",
        "parallel_waiting_next",
    ]
    summary = {key: payload.get(key) for key in summary_keys}
    summary["selected_master_candidate"] = payload["selected_master_candidate"]
    (export_path / "P197_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P197 Prompt Master From Historical Audit + Regression MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- master_status: {payload['master_status']}",
        f"- candidate_count: {payload['candidate_count']}",
        f"- regression_check_count: {payload['regression_check_count']}",
        f"- blocking_review_count: {payload['blocking_review_count']}",
        f"- selected: {selected.get('source_path', '')}",
        "",
        "## Safety",
        "- PROMPT_SOURCE_MODIFIED=False",
        "- GEM_CALL_EXECUTED=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "## Next",
        f"- {payload['recommended_next']}",
        f"- waiting real inputs: {payload['parallel_waiting_next']}",
    ]
    (export_path / "P197_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P197"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_prompt_master_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8105,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_prompt_master_historical_regression(root)

    command = [
        sys.executable,
        "-m",
        "mvp_qaic_py.p173_nicegui_private_local_runner",
        "--project-root",
        str(root),
        "--host",
        host,
        "--port",
        str(port),
        "--serve-private",
        "--no-show",
    ]

    process = subprocess.Popen(
        command,
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    route_results: list[dict[str, Any]] = []
    route_smoke_ok = False
    server_stopped = False
    start = time.time()

    try:
        while time.time() - start < timeout_seconds:
            if process.poll() is not None:
                break
            route_results = [
                {
                    "route": route,
                    "url": f"http://{host}:{port}{route}",
                    "ok": _http_ok(f"http://{host}:{port}{route}"),
                }
                for route in ROUTES
            ]
            if all(row["ok"] for row in route_results):
                route_smoke_ok = True
                break
            time.sleep(1.0)
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=8)
                server_stopped = True
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=8)
                server_stopped = True
        else:
            server_stopped = True

    return {
        **payload,
        "STATUS": "OK_P197_PROMPT_MASTER_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P197_PROMPT_MASTER_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_prompt_master_historical_regression_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_prompt_master_historical_regression(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_prompt_master_route_smoke(project_root)
        payload.update(
            {
                "STATUS": smoke["STATUS"],
                "route_results": smoke["route_results"],
                "route_success_count": smoke["route_success_count"],
                "route_smoke_ok": smoke["route_smoke_ok"],
                "server_started_by_smoke": smoke["server_started_by_smoke"],
                "server_stopped_after_smoke": smoke["server_stopped_after_smoke"],
            }
        )
        export_path = Path(payload["export_dir"])
        summary = {
            key: payload.get(key)
            for key in [
                "STATUS",
                "generated_at",
                "project_root",
                "export_dir",
                "candidate_count",
                "master_status",
                "regression_check_count",
                "blocking_review_count",
                "route_success_count",
                "route_smoke_ok",
                "blocker_count",
                "blockers",
                "prompt_source_modified",
                "gem_call_executed",
                "google_sheets_write",
                "live_google_api_call_from_python",
                "apps_script_execution",
                "clasp_push",
                "public_serve",
                "broker",
                "order",
                "sizing",
                "auto_apply_gem_response",
                "source_prompt_modified",
                "recommended_next",
                "parallel_waiting_next",
            ]
        }
        summary["selected_master_candidate"] = payload["selected_master_candidate"]
        (export_path / "P197_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P197 prompt master historical regression.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_prompt_master_historical_regression_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_prompt_master_historical_regression(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"CANDIDATE_COUNT={payload['candidate_count']}")
        print(f"MASTER_STATUS={payload['master_status']}")

    return 0 if payload["candidate_count"] > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
