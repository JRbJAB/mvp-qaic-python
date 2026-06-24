from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p195r_operator_release_runtime_tracker_next_selector_maxi import (
    build_operator_release_runtime_tracker,
)


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


INPUT_ROOT_REL = "00_OPERATOR_EXPORTS/P196_REAL_CASE_PORTFOLIO_GEM_INPUTS"

INPUT_CONTRACT: list[dict[str, Any]] = [
    {
        "input_id": "portfolio_capture_image",
        "required": True,
        "folder": "CAPTURES",
        "extensions": [".png", ".jpg", ".jpeg", ".webp"],
        "operator_action": "Ajouter une capture écran portfolio Revolut X ou équivalent.",
    },
    {
        "input_id": "gem_response_paste",
        "required": True,
        "folder": "RESPONSES",
        "extensions": [".txt", ".md", ".json"],
        "operator_action": "Coller la réponse GEM réelle dans un fichier texte ou JSON.",
    },
    {
        "input_id": "copied_interface_text",
        "required": False,
        "folder": "TEXT",
        "extensions": [".txt", ".md", ".csv"],
        "operator_action": "Ajouter le texte copié de l'interface si disponible.",
    },
    {
        "input_id": "operator_notes",
        "required": False,
        "folder": "NOTES",
        "extensions": [".txt", ".md"],
        "operator_action": "Ajouter contexte opérateur, anomalies, hypothèses et contraintes.",
    },
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _input_root(project_root: Path) -> Path:
    return project_root / INPUT_ROOT_REL


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def ensure_real_case_input_folders(project_root: str | Path) -> list[dict[str, Any]]:
    root = Path(project_root)
    created: list[dict[str, Any]] = []
    for spec in INPUT_CONTRACT:
        folder = _input_root(root) / str(spec["folder"])
        folder.mkdir(parents=True, exist_ok=True)
        readme = folder / "README_INPUTS.md"
        if not readme.exists():
            readme.write_text(
                "\n".join(
                    [
                        f"# {spec['input_id']}",
                        "",
                        f"required: {spec['required']}",
                        f"allowed_extensions: {', '.join(spec['extensions'])}",
                        f"operator_action: {spec['operator_action']}",
                        "",
                        "Safety: local private only. Do not add secrets. Do not execute broker/order/sizing.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
        created.append(
            {
                "input_id": spec["input_id"],
                "folder": _safe_rel(folder, root),
                "readme": _safe_rel(readme, root),
            }
        )
    return created


def _count_matching_files(folder: Path, extensions: list[str]) -> tuple[int, list[str]]:
    if not folder.exists():
        return 0, []
    matches: list[str] = []
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        if item.name.lower() in {"desktop.ini", "readme_inputs.md"}:
            continue
        if item.suffix.lower() in {ext.lower() for ext in extensions}:
            matches.append(item.name)
    return len(matches), matches


def build_real_case_portfolio_gem_inputs(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    release = build_operator_release_runtime_tracker(root)
    input_rows: list[dict[str, Any]] = []

    required_ready = True
    capture_count = 0
    response_count = 0

    for spec in INPUT_CONTRACT:
        folder = _input_root(root) / str(spec["folder"])
        count, examples = _count_matching_files(folder, list(spec["extensions"]))
        status = "FOUND" if count > 0 else "WAITING_INPUT"
        if bool(spec["required"]) and count <= 0:
            required_ready = False
        if spec["input_id"] == "portfolio_capture_image":
            capture_count = count
        if spec["input_id"] == "gem_response_paste":
            response_count = count

        input_rows.append(
            {
                "input_id": spec["input_id"],
                "required": bool(spec["required"]),
                "status": status,
                "file_count": count,
                "examples": ";".join(examples[:5]),
                "local_path": _safe_rel(folder, root),
                "allowed_extensions": ",".join(spec["extensions"]),
                "operator_action": spec["operator_action"],
            }
        )

    ready_for_review = (
        required_ready
        and bool(release.get("operator_runtime_release_allowed"))
        and capture_count >= 1
        and response_count >= 1
    )
    input_status = (
        "READY_FOR_REAL_CASE_REVIEW"
        if ready_for_review
        else "WAITING_OPERATOR_CAPTURE_AND_GEM_RESPONSE"
    )

    operator_steps = [
        {
            "step": 1,
            "action": f"Déposer une capture image dans {INPUT_ROOT_REL}/CAPTURES",
            "status": "DONE" if capture_count else "WAITING",
        },
        {
            "step": 2,
            "action": "Exécuter manuellement le prompt GEM hors Python, puis coller la réponse dans RESPONSES.",
            "status": "DONE" if response_count else "WAITING",
        },
        {
            "step": 3,
            "action": "Ajouter texte copié/notes si disponible.",
            "status": "OPTIONAL",
        },
        {
            "step": 4,
            "action": "Relancer ce statut pour passer vers P196B review réelle.",
            "status": "READY" if ready_for_review else "WAITING_INPUTS",
        },
    ]

    blockers: list[str] = []
    if capture_count < 1:
        blockers.append("WAITING_PORTFOLIO_CAPTURE_IMAGE")
    if response_count < 1:
        blockers.append("WAITING_REAL_GEM_RESPONSE_PASTE")
    if not bool(release.get("operator_runtime_release_allowed")):
        blockers.append("OPERATOR_RUNTIME_NOT_RELEASED")

    return {
        "STATUS": "OK_P196_REAL_CASE_PORTFOLIO_GEM_INPUTS_READY"
        if not blockers
        else "WAITING_P196_REAL_CASE_PORTFOLIO_GEM_INPUTS",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "input_root": str(_input_root(root)),
        "input_status": input_status,
        "ready_for_review": ready_for_review,
        "capture_count": capture_count,
        "response_count": response_count,
        "input_contract_rows": input_rows,
        "operator_steps": operator_steps,
        "operator_release_status": release.get("operator_release_status"),
        "runtime_close_percent": release.get("runtime_close_percent"),
        "selected_previous_next_pack": release.get("selected_next_pack"),
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P196B_REAL_CASE_PORTFOLIO_GEM_REVIEW_AFTER_OPERATOR_INPUTS_MAXI"
        if ready_for_review
        else "WAIT_OPERATOR_CAPTURE_AND_GEM_RESPONSE_THEN_RERUN_P196",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_real_case_portfolio_gem_inputs(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    prepare_folders: bool = False,
) -> dict[str, Any]:
    root = Path(project_root)
    if prepare_folders:
        ensure_real_case_input_folders(root)

    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P196_REAL_CASE_PORTFOLIO_GEM_INPUTS_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_real_case_portfolio_gem_inputs(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P196_REAL_CASE_PORTFOLIO_GEM_INPUTS.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_csv(
        export_path / "P196_INPUT_CONTRACT.csv",
        payload["input_contract_rows"],
        [
            "input_id",
            "required",
            "status",
            "file_count",
            "examples",
            "local_path",
            "allowed_extensions",
            "operator_action",
        ],
    )

    _write_csv(
        export_path / "P196_OPERATOR_STEPS.csv",
        payload["operator_steps"],
        ["step", "action", "status"],
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "input_root",
        "input_status",
        "ready_for_review",
        "capture_count",
        "response_count",
        "operator_release_status",
        "runtime_close_percent",
        "blocker_count",
        "blockers",
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
    ]
    summary = {key: payload.get(key) for key in summary_keys}
    (export_path / "P196_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P196 Real Case Portfolio GEM Operator Inputs MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- input_status: {payload['input_status']}",
        f"- ready_for_review: {payload['ready_for_review']}",
        f"- capture_count: {payload['capture_count']}",
        f"- response_count: {payload['response_count']}",
        f"- recommended_next: {payload['recommended_next']}",
        "",
        "## Operator folders",
        f"- {INPUT_ROOT_REL}/CAPTURES",
        f"- {INPUT_ROOT_REL}/RESPONSES",
        f"- {INPUT_ROOT_REL}/TEXT",
        f"- {INPUT_ROOT_REL}/NOTES",
        "",
        "## Safety",
        "- GEM_CALL_EXECUTED=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
    ]
    (export_path / "P196_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P196"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_real_case_inputs_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8104,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_real_case_portfolio_gem_inputs(root)

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
        "STATUS": "OK_P196_REAL_CASE_INPUTS_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P196_REAL_CASE_INPUTS_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_real_case_portfolio_gem_inputs_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    prepare_folders: bool = False,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_real_case_portfolio_gem_inputs(
        project_root,
        export_dir=export_dir,
        prepare_folders=prepare_folders,
    )
    if run_route_smoke:
        smoke = run_real_case_inputs_route_smoke(project_root)
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
                "input_root",
                "input_status",
                "ready_for_review",
                "capture_count",
                "response_count",
                "operator_release_status",
                "runtime_close_percent",
                "route_success_count",
                "route_smoke_ok",
                "blocker_count",
                "blockers",
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
            ]
        }
        (export_path / "P196_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P196 real case portfolio GEM operator inputs.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--prepare-folders", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_real_case_portfolio_gem_inputs_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            prepare_folders=args.prepare_folders,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_real_case_portfolio_gem_inputs(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"INPUT_STATUS={payload['input_status']}")
        print(f"READY_FOR_REVIEW={payload['ready_for_review']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
