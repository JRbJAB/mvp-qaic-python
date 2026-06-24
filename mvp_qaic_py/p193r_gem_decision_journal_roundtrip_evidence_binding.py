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


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _evidence_id(kind: str, path: Path) -> str:
    raw = f"{kind}:{path.as_posix()}".lower()
    return "".join(ch if ch.isalnum() else "-" for ch in raw).strip("-")[:150]


def _is_desktop_ini(path: Path) -> bool:
    return path.name.lower() == "desktop.ini"


def _match_terms(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def _collect_evidence(
    root: Path,
    *,
    evidence_type: str,
    terms: list[str],
    max_items: int = 120,
) -> list[dict[str, Any]]:
    base = root / "05_EXPORTS"
    rows: list[dict[str, Any]] = []
    if not base.exists():
        return rows

    candidates: list[Path] = []
    for path in base.rglob("*"):
        if len(candidates) >= max_items * 8:
            break
        if _is_desktop_ini(path):
            continue
        rel = _safe_rel(path, root)
        if _match_terms(rel, terms):
            candidates.append(path)

    candidates = sorted(
        candidates,
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
        reverse=True,
    )

    for path in candidates[:max_items]:
        if not path.exists():
            continue
        rows.append(
            {
                "evidence_id": _evidence_id(evidence_type, path),
                "evidence_type": evidence_type,
                "name": path.name,
                "source_path": _safe_rel(path, root),
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
                "size_bytes": path.stat().st_size if path.is_file() else 0,
                "modified_time_epoch": int(path.stat().st_mtime),
            }
        )

    return rows


def _latest(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    return str(rows[0]["source_path"])


def _evidence_percent(count: int) -> int:
    if count >= 5:
        return 100
    if count >= 3:
        return 90
    if count >= 1:
        return 75
    return 30


def _status(percent: int) -> str:
    if percent >= 90:
        return "EVIDENCE_BOUND_READY"
    if percent >= 75:
        return "EVIDENCE_BOUND_PARTIAL"
    return "EVIDENCE_MISSING"


def _next_action(layer_id: str, status: str) -> str:
    if status == "EVIDENCE_BOUND_READY":
        return "KEEP_TRACKING"
    if layer_id == "GEM_ROUNDTRIP":
        return "ADD_OR_BIND_MORE_ROUNDTRIP_EXPORTS"
    if layer_id == "GEM_DECISION_JOURNAL":
        return "ADD_OR_BIND_DECISION_JOURNAL_EXPORT"
    return "REVIEW"


def build_gem_evidence_binding(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)

    roundtrip_terms = [
        "p185",
        "p186",
        "roundtrip",
        "real_operator_capture_response",
        "real_operator_roundtrip",
    ]
    journal_terms = [
        "decision_journal",
        "journal",
        "p120",
        "p153",
        "p187",
        "p188",
        "real_case",
        "review_gate",
        "human_review",
    ]

    roundtrip_rows = _collect_evidence(
        root,
        evidence_type="GEM_ROUNDTRIP",
        terms=roundtrip_terms,
    )
    journal_rows = _collect_evidence(
        root,
        evidence_type="GEM_DECISION_JOURNAL",
        terms=journal_terms,
    )

    roundtrip_percent = _evidence_percent(len(roundtrip_rows))
    journal_percent = _evidence_percent(len(journal_rows))

    binding_rows = [
        {
            "layer_id": "GEM_ROUNDTRIP",
            "evidence_status": _status(roundtrip_percent),
            "evidence_count": len(roundtrip_rows),
            "evidence_percent": roundtrip_percent,
            "latest_evidence": _latest(roundtrip_rows),
            "next_action": _next_action("GEM_ROUNDTRIP", _status(roundtrip_percent)),
        },
        {
            "layer_id": "GEM_DECISION_JOURNAL",
            "evidence_status": _status(journal_percent),
            "evidence_count": len(journal_rows),
            "evidence_percent": journal_percent,
            "latest_evidence": _latest(journal_rows),
            "next_action": _next_action("GEM_DECISION_JOURNAL", _status(journal_percent)),
        },
    ]

    evidence_rows = sorted(
        [*roundtrip_rows, *journal_rows],
        key=lambda row: (str(row["evidence_type"]), -int(row["modified_time_epoch"])),
    )

    coverage = round((roundtrip_percent + journal_percent) / 2, 1)

    blockers: list[str] = []
    if not roundtrip_rows:
        blockers.append("NO_ROUNDTRIP_EVIDENCE_FOUND")
    if not journal_rows:
        blockers.append("NO_DECISION_JOURNAL_EVIDENCE_FOUND")

    return {
        "STATUS": "OK_P193R_GEM_DECISION_JOURNAL_ROUNDTRIP_EVIDENCE_BINDING_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "binding_layer_count": 2,
        "roundtrip_evidence_count": len(roundtrip_rows),
        "decision_journal_evidence_count": len(journal_rows),
        "evidence_coverage_percent": coverage,
        "binding_rows": binding_rows,
        "evidence_rows": evidence_rows,
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P194R_GEM_RUNTIME_TRACKER_CLOSE_OR_SHEETS_EXPORT_CONTRACT",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_gem_evidence_binding(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P193R_GEM_EVIDENCE_BINDING_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_gem_evidence_binding(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P193R_GEM_EVIDENCE_BINDING.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_csv(
        export_path / "P193R_GEM_EVIDENCE_BINDING.csv",
        payload["binding_rows"],
        [
            "layer_id",
            "evidence_status",
            "evidence_count",
            "evidence_percent",
            "latest_evidence",
            "next_action",
        ],
    )

    _write_csv(
        export_path / "P193R_GEM_ROUNDTRIP_EVIDENCE.csv",
        [row for row in payload["evidence_rows"] if row["evidence_type"] == "GEM_ROUNDTRIP"],
        [
            "evidence_id",
            "evidence_type",
            "name",
            "source_path",
            "is_file",
            "is_dir",
            "size_bytes",
            "modified_time_epoch",
        ],
    )

    _write_csv(
        export_path / "P193R_GEM_DECISION_JOURNAL_EVIDENCE.csv",
        [row for row in payload["evidence_rows"] if row["evidence_type"] == "GEM_DECISION_JOURNAL"],
        [
            "evidence_id",
            "evidence_type",
            "name",
            "source_path",
            "is_file",
            "is_dir",
            "size_bytes",
            "modified_time_epoch",
        ],
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "binding_layer_count",
        "roundtrip_evidence_count",
        "decision_journal_evidence_count",
        "evidence_coverage_percent",
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
    (export_path / "P193R_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# P193R GEM Decision Journal + Roundtrip Evidence Binding",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- roundtrip_evidence_count: {payload['roundtrip_evidence_count']}",
        f"- decision_journal_evidence_count: {payload['decision_journal_evidence_count']}",
        f"- evidence_coverage_percent: {payload['evidence_coverage_percent']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "## Binding rows",
    ]
    for row in payload["binding_rows"]:
        lines.append(
            f"- {row['layer_id']}: {row['evidence_status']} / "
            f"{row['evidence_count']} evidence / latest={row['latest_evidence']}"
        )
    lines.extend(
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
            "- P194R_GEM_RUNTIME_TRACKER_CLOSE_OR_SHEETS_EXPORT_CONTRACT",
        ]
    )
    (export_path / "P193R_REPORT.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P193R"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_evidence_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8101,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_gem_evidence_binding(root)

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
        "STATUS": "OK_P193R_GEM_EVIDENCE_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P193R_GEM_EVIDENCE_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_gem_evidence_binding_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_gem_evidence_binding(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_evidence_route_smoke(project_root)
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
                "binding_layer_count",
                "roundtrip_evidence_count",
                "decision_journal_evidence_count",
                "evidence_coverage_percent",
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
        }
        (export_path / "P193R_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P193R GEM evidence binding.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_gem_evidence_binding_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_gem_evidence_binding(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"ROUNDTRIP_EVIDENCE_COUNT={payload['roundtrip_evidence_count']}")
        print(f"DECISION_JOURNAL_EVIDENCE_COUNT={payload['decision_journal_evidence_count']}")
        print(f"EVIDENCE_COVERAGE_PERCENT={payload['evidence_coverage_percent']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
