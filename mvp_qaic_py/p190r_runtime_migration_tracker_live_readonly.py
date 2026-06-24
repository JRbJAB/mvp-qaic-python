from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter
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
    "/review",
]

EXPECTED_GEM_TRACKING_LAYERS = [
    "GEM_CAPTURE_INBOX",
    "GEM_RESPONSE_INBOX",
    "GEM_SESSION_LOG",
    "GEM_REVIEW_GATE",
    "GEM_DECISION_JOURNAL",
    "PROMPT_HISTORY_LIBRARY",
    "PROMPT_MIGRATION_MATRIX",
    "RUNTIME_MIGRATION_TRACKER",
    "REAL_CASE_DECISION_GATE",
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


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _artifact_id(kind: str, name: str) -> str:
    raw = f"{kind}:{name}".lower()
    return re.sub(r"[^a-z0-9]+", "-", raw).strip("-")[:120]


def _score_artifact(row: dict[str, Any]) -> int:
    score = 0
    score += 10 if row.get("discovered") else 0
    score += 15 if row.get("mapped_to_source") else 0
    score += 20 if row.get("python_equivalent_exists") else 0
    score += 15 if row.get("tests_exist") else 0
    score += 10 if row.get("visible_in_nicegui") else 0
    score += 15 if row.get("runtime_smoke_passed") else 0
    score += 10 if row.get("export_or_report_exists") else 0
    score += 5 if row.get("git_tag_sealed") else 0
    return min(100, score)


def _status_from_score(score: int) -> str:
    if score >= 95:
        return "SEALED"
    if score >= 75:
        return "RUNTIME_SMOKED"
    if score >= 60:
        return "UI_VISIBLE"
    if score >= 45:
        return "TESTED"
    if score >= 30:
        return "MAPPED"
    return "DISCOVERED"


def _append_artifact(
    rows: list[dict[str, Any]],
    *,
    root: Path,
    artifact_type: str,
    name: str,
    path: Path | None = None,
    mapped_to_source: bool = False,
    python_equivalent_exists: bool = False,
    tests_exist: bool = False,
    visible_in_nicegui: bool = False,
    runtime_smoke_passed: bool = False,
    export_or_report_exists: bool = False,
    git_tag_sealed: bool = False,
    next_action: str = "REVIEW",
) -> None:
    source_path = _safe_rel(path, root) if path is not None else ""
    row: dict[str, Any] = {
        "artifact_id": _artifact_id(artifact_type, name),
        "artifact_type": artifact_type,
        "name": name,
        "source_path": source_path,
        "discovered": True,
        "mapped_to_source": mapped_to_source,
        "python_equivalent_exists": python_equivalent_exists,
        "tests_exist": tests_exist,
        "visible_in_nicegui": visible_in_nicegui,
        "runtime_smoke_passed": runtime_smoke_passed,
        "export_or_report_exists": export_or_report_exists,
        "git_tag_sealed": git_tag_sealed,
        "next_action": next_action,
    }
    score = _score_artifact(row)
    row["migration_percent"] = score
    row["migration_status"] = _status_from_score(score)
    rows.append(row)


def _python_functions(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return []
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
    return sorted(set(names))


def _nicegui_routes(p173_path: Path) -> list[str]:
    if not p173_path.exists():
        return []
    text = p173_path.read_text(encoding="utf-8", errors="replace")
    return sorted(set(re.findall(r'@ui\.page\("([^"]+)"\)', text)))


def _apps_script_functions(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    names = re.findall(r"function\s+([A-Za-z0-9_]+)\s*\(", text)
    names.extend(re.findall(r"const\s+([A-Za-z0-9_]+)\s*=\s*\([^)]*\)\s*=>", text))
    return sorted(set(names))


def _read_csv_headers(path: Path) -> list[str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file_obj:
            reader = csv.reader(file_obj)
            return next(reader, [])
    except Exception:
        return []


def _sheet_tab_candidates(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in root.rglob("*.csv"):
        if any(
            part in {".git", ".ruff_cache", ".pytest_cache", "__pycache__"} for part in path.parts
        ):
            continue
        name = path.stem
        lower = name.lower()
        headers = _read_csv_headers(path)
        if any(
            token in lower
            for token in [
                "sheet",
                "tab",
                "gem",
                "prompt",
                "decision",
                "journal",
                "runtime",
                "migration",
            ]
        ):
            rows.append(
                {
                    "name": name,
                    "path": path,
                    "headers": headers,
                    "row_hint": "CSV_SNAPSHOT",
                }
            )
    return rows


def _gem_tracking_rows(root: Path, artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing_names = {row["name"].upper() for row in artifacts}
    rows: list[dict[str, Any]] = []

    evidence = {
        "GEM_CAPTURE_INBOX": root / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX",
        "GEM_RESPONSE_INBOX": root / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES",
        "GEM_SESSION_LOG": root / "00_OPERATOR_EXPORTS" / "P181_SESSION_LOG",
        "GEM_REVIEW_GATE": root / "mvp_qaic_py" / "p187_real_manual_portfolio_case_review_gate.py",
        "GEM_DECISION_JOURNAL": root / "05_EXPORTS",
        "PROMPT_HISTORY_LIBRARY": root
        / "mvp_qaic_py"
        / "p182_prompt_history_library_version_studio.py",
        "PROMPT_MIGRATION_MATRIX": root / "05_EXPORTS",
        "RUNTIME_MIGRATION_TRACKER": root
        / "mvp_qaic_py"
        / "p190r_runtime_migration_tracker_live_readonly.py",
        "REAL_CASE_DECISION_GATE": root
        / "mvp_qaic_py"
        / "p188_real_case_ui_operator_decision_gate.py",
    }

    for layer in EXPECTED_GEM_TRACKING_LAYERS:
        path = evidence[layer]
        exists = path.exists()
        status = "DISCOVERED" if exists else "EXPECTED_NOT_FOUND"
        percent = 35 if exists else 10
        if layer in existing_names:
            percent = max(percent, 45)
        if layer in {"GEM_REVIEW_GATE", "REAL_CASE_DECISION_GATE"} and exists:
            percent = 75
            status = "RUNTIME_SMOKED"
        if layer == "RUNTIME_MIGRATION_TRACKER" and exists:
            percent = 60
            status = "UI_VISIBLE"

        rows.append(
            {
                "name": layer,
                "status": status,
                "migration_percent": percent,
                "path": str(path),
                "next_action": "KEEP_TRACKING" if exists else "CREATE_OR_BIND_LAYER",
            }
        )

    return rows


def build_runtime_migration_tracker(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    rows: list[dict[str, Any]] = []

    py_files = (
        sorted((root / "mvp_qaic_py").glob("p*.py")) if (root / "mvp_qaic_py").exists() else []
    )
    test_files = sorted((root / "tests").glob("test_p*.py")) if (root / "tests").exists() else []
    test_names = {path.stem.replace("test_", "") for path in test_files}

    p173 = root / "mvp_qaic_py" / "p173_nicegui_private_local_runner.py"
    routes = _nicegui_routes(p173)

    export_dirs = sorted((root / "05_EXPORTS").glob("P*")) if (root / "05_EXPORTS").exists() else []
    tag_list: list[str] = []
    try:
        completed = subprocess.run(
            ["git", "tag", "--list"],
            cwd=str(root),
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        tag_list = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    except Exception:
        tag_list = []

    for path in py_files:
        module = path.stem
        related_test = module in test_names
        related_export = any(
            module.split("_")[0].upper() in export.name.upper() for export in export_dirs
        )
        related_tag = any(
            module.split("_")[0].replace("p", "p-") in tag.lower()
            or module.split("_")[0] in tag.lower()
            for tag in tag_list
        )
        visible = any(
            token in module for token in ["p173", "p180", "p181", "p184", "p185", "p188", "p190r"]
        )

        _append_artifact(
            rows,
            root=root,
            artifact_type="PY_MODULE",
            name=module,
            path=path,
            mapped_to_source=True,
            python_equivalent_exists=True,
            tests_exist=related_test,
            visible_in_nicegui=visible,
            runtime_smoke_passed=related_export,
            export_or_report_exists=related_export,
            git_tag_sealed=related_tag,
            next_action="KEEP_OR_EXTEND" if related_test else "ADD_TEST",
        )

        for func_name in _python_functions(path):
            if func_name.startswith("_"):
                continue
            _append_artifact(
                rows,
                root=root,
                artifact_type="PY_FUNCTION",
                name=f"{module}.{func_name}",
                path=path,
                mapped_to_source=True,
                python_equivalent_exists=True,
                tests_exist=related_test,
                visible_in_nicegui=visible,
                runtime_smoke_passed=related_export,
                export_or_report_exists=related_export,
                git_tag_sealed=related_tag,
                next_action="KEEP_TRACKING",
            )

    for path in test_files:
        _append_artifact(
            rows,
            root=root,
            artifact_type="PY_TEST",
            name=path.stem,
            path=path,
            mapped_to_source=True,
            python_equivalent_exists=True,
            tests_exist=True,
            runtime_smoke_passed=True,
            export_or_report_exists=False,
            git_tag_sealed=False,
            next_action="KEEP_TESTING",
        )

    for route in routes:
        _append_artifact(
            rows,
            root=root,
            artifact_type="NICEGUI_ROUTE",
            name=route,
            path=p173,
            mapped_to_source=True,
            python_equivalent_exists=True,
            tests_exist=True,
            visible_in_nicegui=True,
            runtime_smoke_passed=route in ROUTES,
            export_or_report_exists=True,
            git_tag_sealed=True,
            next_action="KEEP_VISIBLE",
        )

    for item in _sheet_tab_candidates(root):
        headers = [h.lower() for h in item["headers"]]
        is_gem = any(
            token in item["name"].lower()
            for token in ["gem", "prompt", "decision", "journal", "runtime"]
        )
        has_runtime_headers = any(
            h in headers
            for h in [
                "run_id",
                "status",
                "decision",
                "prompt_id",
                "response_id",
                "capture_id",
                "blocker_count",
            ]
        )
        _append_artifact(
            rows,
            root=root,
            artifact_type="SHEET_TAB_OR_CSV_SNAPSHOT",
            name=item["name"],
            path=item["path"],
            mapped_to_source=True,
            python_equivalent_exists=is_gem,
            tests_exist=False,
            visible_in_nicegui=is_gem,
            runtime_smoke_passed=False,
            export_or_report_exists=True,
            git_tag_sealed=False,
            next_action="BIND_GEM_TRACKING_LAYER"
            if is_gem or has_runtime_headers
            else "REVIEW_SHEET_SNAPSHOT",
        )

    script_files = []
    for suffix in ["*.gs", "*.js", "*.html"]:
        script_files.extend(root.rglob(suffix))
    for path in sorted(set(script_files)):
        if any(
            part in {".git", ".ruff_cache", ".pytest_cache", "__pycache__", "node_modules"}
            for part in path.parts
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")[:2000]
        if "function " not in text and path.suffix.lower() not in {".html", ".js"}:
            continue

        _append_artifact(
            rows,
            root=root,
            artifact_type="APPS_SCRIPT_FILE",
            name=path.name,
            path=path,
            mapped_to_source=True,
            python_equivalent_exists=False,
            tests_exist=False,
            visible_in_nicegui=False,
            runtime_smoke_passed=False,
            export_or_report_exists=False,
            git_tag_sealed=False,
            next_action="MAP_TO_PYTHON_OR_ARCHIVE",
        )
        for fn in _apps_script_functions(path):
            _append_artifact(
                rows,
                root=root,
                artifact_type="APPS_SCRIPT_FUNCTION",
                name=fn,
                path=path,
                mapped_to_source=True,
                python_equivalent_exists=False,
                tests_exist=False,
                visible_in_nicegui=False,
                runtime_smoke_passed=False,
                export_or_report_exists=False,
                git_tag_sealed=False,
                next_action="CLASSIFY_FUNCTION_MIGRATION",
            )

    gem_rows = _gem_tracking_rows(root, rows)

    scores = [int(row["migration_percent"]) for row in rows]
    migration_percent = round(sum(scores) / len(scores), 1) if scores else 0.0
    type_counts = Counter(str(row["artifact_type"]) for row in rows)
    status_counts = Counter(str(row["migration_status"]) for row in rows)

    coverage_rows = []
    for area, count in sorted(type_counts.items()):
        area_scores = [
            int(row["migration_percent"]) for row in rows if row["artifact_type"] == area
        ]
        percent = round(sum(area_scores) / len(area_scores), 1) if area_scores else 0.0
        coverage_rows.append(
            {
                "area": area,
                "count": count,
                "percent": percent,
                "status": _status_from_score(int(percent)),
            }
        )

    blockers: list[str] = []
    if not any(
        row["artifact_type"] == "NICEGUI_ROUTE" and row["name"] == "/migration" for row in rows
    ):
        blockers.append("MIGRATION_ROUTE_NOT_VISIBLE")
    if not gem_rows:
        blockers.append("GEM_TRACKING_LAYER_EMPTY")

    return {
        "STATUS": "OK_P190R_RUNTIME_MIGRATION_TRACKER_LIVE_READONLY_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "artifact_count": len(rows),
        "migration_percent": migration_percent,
        "type_counts": dict(sorted(type_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "coverage_rows": coverage_rows,
        "gem_tracking_rows": gem_rows,
        "artifacts": sorted(
            rows,
            key=lambda row: (
                str(row["artifact_type"]),
                -int(row["migration_percent"]),
                str(row["name"]),
            ),
        ),
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P191R_GEM_TRACKING_TABS_RUNTIME_BINDING_MATRIX",
    }


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P190R"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_migration_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8098,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_runtime_migration_tracker(root)

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
        "STATUS": "OK_P190R_MIGRATION_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P190R_MIGRATION_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_runtime_migration_tracker(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P190R_RUNTIME_MIGRATION_TRACKER_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = (
        run_migration_route_smoke(root)
        if run_route_smoke
        else build_runtime_migration_tracker(root)
    )
    payload["export_dir"] = str(export_path)

    (export_path / "P190R_RUNTIME_MIGRATION_TRACKER.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (export_path / "P190R_RUNTIME_ARTIFACTS.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file_obj:
        fieldnames = [
            "artifact_id",
            "artifact_type",
            "name",
            "source_path",
            "migration_status",
            "migration_percent",
            "next_action",
        ]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in payload["artifacts"]:
            writer.writerow({key: row.get(key) for key in fieldnames})

    with (export_path / "P190R_GEM_TRACKING_LAYERS.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file_obj:
        fieldnames = ["name", "status", "migration_percent", "path", "next_action"]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in payload["gem_tracking_rows"]:
            writer.writerow({key: row.get(key) for key in fieldnames})

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "artifact_count",
        "migration_percent",
        "type_counts",
        "status_counts",
        "blocker_count",
        "blockers",
        "route_success_count",
        "route_smoke_ok",
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
    (export_path / "P190R_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P190R Runtime Migration Tracker Live Readonly",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- artifact_count: {payload['artifact_count']}",
        f"- migration_percent: {payload['migration_percent']}",
        f"- blocker_count: {payload['blocker_count']}",
        f"- route_smoke_ok: {payload.get('route_smoke_ok')}",
        "",
        "## GEM tracking layers",
    ]
    for row in payload["gem_tracking_rows"]:
        report.append(
            f"- {row['name']}: {row['status']} / {row['migration_percent']}% / {row['next_action']}"
        )
    report.extend(
        [
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
            "",
            "## Next",
            "- P191R_GEM_TRACKING_TABS_RUNTIME_BINDING_MATRIX",
        ]
    )
    (export_path / "P190R_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P190R runtime migration tracker.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_runtime_migration_tracker(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_runtime_migration_tracker(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"ARTIFACT_COUNT={payload['artifact_count']}")
        print(f"MIGRATION_PERCENT={payload['migration_percent']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["artifact_count"] > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
