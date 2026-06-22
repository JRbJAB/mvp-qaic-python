from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P126_DAILY_RUN_REGISTRY_LOCAL_ONLY_0_1_1_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "REGISTRY_ONLY",
    "HUMAN_REVIEW_ONLY",
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

P124_PATTERNS = (
    "P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_*",
    "LOCAL_TEST_FILLED_P124_REAL_GEM_*",
)

P125_PATTERNS = (
    "P125_REAL_GEM_MANUAL_TEST_REVIEW_UX_*",
    "LOCAL_TEST_P125_REVIEW_READY_*",
)

REGISTRY_FIELDS = (
    "registry_row_id",
    "run_family",
    "p124_run_dir",
    "p125_review_dir",
    "p124_status",
    "p125_status",
    "decision_status",
    "ready_for_real_gem_manual_test",
    "ready_for_operator_review",
    "finding_count",
    "blocker_count",
    "missing_data_count",
    "human_review_only",
    "no_sheet_write",
    "no_auto_apply_gem_response",
    "no_order_no_sizing",
    "next",
)


@dataclass(frozen=True)
class DailyRunRegistryRequest:
    output_dir: str | Path
    exports_dir: str | Path
    run_id: str = "P126-DAILY-RUN-REGISTRY"
    generated_at_utc: str | None = None
    limit: int = 50
    notes: str | None = None


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _discover_dirs(exports_dir: Path, patterns: Sequence[str]) -> list[Path]:
    found: list[Path] = []
    if not exports_dir.exists():
        return found
    for pattern in patterns:
        found.extend(path for path in exports_dir.glob(pattern) if path.is_dir())
    unique = {str(path.resolve()): path for path in found}
    return sorted(unique.values(), key=lambda path: path.stat().st_mtime, reverse=True)


def discover_p124_dirs(exports_dir: str | Path) -> list[Path]:
    return _discover_dirs(Path(exports_dir), P124_PATTERNS)


def discover_p125_dirs(exports_dir: str | Path) -> list[Path]:
    return _discover_dirs(Path(exports_dir), P125_PATTERNS)


def _normalize_path(value: Any) -> str:
    if not value:
        return ""
    try:
        return str(Path(str(value)).resolve())
    except OSError:
        return str(value)


def _bool_text(value: Any) -> str:
    return "true" if bool(value) else "false"


def _int_text(value: Any) -> str:
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return "0"


def _p124_manifest(path: Path) -> dict[str, Any]:
    return _read_json(path / "P124_INPUT_HELPER_MANIFEST.json")


def _p125_manifest(path: Path) -> dict[str, Any]:
    return _read_json(path / "P125_RUN_MANIFEST.json")


def _row_from_p125(
    row_id: int,
    p125_dir: Path,
    p125: Mapping[str, Any],
    p124_by_path: Mapping[str, Mapping[str, Any]],
) -> dict[str, str]:
    p124_path = _normalize_path(p125.get("p124_run_dir"))
    p124 = p124_by_path.get(p124_path, {})
    decision_status = str(p125.get("status") or "UNKNOWN")
    ready_for_review = decision_status == "READY_FOR_OPERATOR_REVIEW"
    return {
        "registry_row_id": f"P126-ROW-{row_id:04d}",
        "run_family": "P124_P125_REVIEW",
        "p124_run_dir": p124_path,
        "p125_review_dir": str(p125_dir),
        "p124_status": str(p124.get("status") or "UNKNOWN"),
        "p125_status": decision_status,
        "decision_status": decision_status,
        "ready_for_real_gem_manual_test": _bool_text(p124.get("ready_for_real_gem_manual_test")),
        "ready_for_operator_review": _bool_text(ready_for_review),
        "finding_count": _int_text(p125.get("finding_count")),
        "blocker_count": _int_text(p125.get("blocker_count")),
        "missing_data_count": _int_text(p125.get("missing_data_count")),
        "human_review_only": _bool_text(p125.get("human_review_only", True)),
        "no_sheet_write": _bool_text(p125.get("no_sheet_write", True)),
        "no_auto_apply_gem_response": _bool_text(p125.get("no_auto_apply_gem_response", True)),
        "no_order_no_sizing": _bool_text(p125.get("no_order_no_sizing", True)),
        "next": str(p125.get("next") or "REAL_GEM_TEST_OR_P126_DAILY_RUN_REGISTRY"),
    }


def _row_from_p124_only(row_id: int, p124_dir: Path, p124: Mapping[str, Any]) -> dict[str, str]:
    return {
        "registry_row_id": f"P126-ROW-{row_id:04d}",
        "run_family": "P124_PENDING_P125",
        "p124_run_dir": str(p124_dir),
        "p125_review_dir": "",
        "p124_status": str(p124.get("status") or "UNKNOWN"),
        "p125_status": "PENDING_P125_REVIEW",
        "decision_status": "PENDING_P125_REVIEW",
        "ready_for_real_gem_manual_test": _bool_text(p124.get("ready_for_real_gem_manual_test")),
        "ready_for_operator_review": "false",
        "finding_count": "0",
        "blocker_count": "0",
        "missing_data_count": "0",
        "human_review_only": "true",
        "no_sheet_write": _bool_text(p124.get("no_sheet_write", True)),
        "no_auto_apply_gem_response": _bool_text(p124.get("no_auto_apply_gem_response", True)),
        "no_order_no_sizing": _bool_text(p124.get("no_order_no_sizing", True)),
        "next": "RUN_P125_REVIEW",
    }


def build_registry_rows(exports_dir: str | Path, limit: int = 50) -> list[dict[str, str]]:
    root = Path(exports_dir)
    p124_dirs = discover_p124_dirs(root)
    p125_dirs = discover_p125_dirs(root)

    p124_by_path: dict[str, Mapping[str, Any]] = {}
    p124_dir_by_path: dict[str, Path] = {}
    for p124_dir in p124_dirs:
        normalized = str(p124_dir.resolve())
        p124_by_path[normalized] = _p124_manifest(p124_dir)
        p124_dir_by_path[normalized] = p124_dir

    rows: list[dict[str, str]] = []
    seen_p124: set[str] = set()
    row_id = 1

    for p125_dir in p125_dirs[:limit]:
        p125 = _p125_manifest(p125_dir)
        if not p125:
            continue
        row = _row_from_p125(row_id, p125_dir, p125, p124_by_path)
        rows.append(row)
        if row["p124_run_dir"]:
            seen_p124.add(_normalize_path(row["p124_run_dir"]))
        row_id += 1

    for normalized, p124 in p124_by_path.items():
        if normalized in seen_p124:
            continue
        rows.append(_row_from_p124_only(row_id, p124_dir_by_path[normalized], p124))
        row_id += 1

    return rows[:limit]


def _write_registry_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(REGISTRY_FIELDS))
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in REGISTRY_FIELDS})


def _report_markdown(rows: list[dict[str, str]]) -> str:
    ready_count = len([row for row in rows if row["ready_for_operator_review"] == "true"])
    blocked_count = len(
        [row for row in rows if row["decision_status"] == "BLOCKED_REVIEW_REQUIRED"]
    )
    pending_count = len([row for row in rows if row["decision_status"].startswith("PENDING")])
    lines = [
        "# P126 Daily Run Registry Report",
        "",
        f"- row_count: `{len(rows)}`",
        f"- ready_for_operator_review_count: `{ready_count}`",
        f"- blocked_review_required_count: `{blocked_count}`",
        f"- pending_count: `{pending_count}`",
        "- local_only: `true`",
        "- no_sheet_write: `true`",
        "- no_auto_apply_gem_response: `true`",
        "- no_order_no_sizing: `true`",
        "",
        "## Rows",
        "",
    ]
    if rows:
        for row in rows:
            lines.append(
                "- "
                + row["registry_row_id"]
                + " | "
                + row["decision_status"]
                + " | ready="
                + row["ready_for_operator_review"]
                + " | findings="
                + row["finding_count"]
            )
    else:
        lines.append("- No P124/P125 runs discovered.")
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "- HUMAN_REVIEW_ONLY",
            "- NO_SHEET_WRITE",
            "- NO_AUTO_APPLY_GEM_RESPONSE",
            "- NO_BROKER",
            "- NO_ORDER",
            "- NO_AUTO_SIZING",
            "- NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
            "",
        ]
    )
    return "\n".join(lines)


def write_daily_run_registry(request: DailyRunRegistryRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    exports = Path(request.exports_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = build_registry_rows(exports, limit=request.limit)

    csv_path = out / "P126_DAILY_RUN_REGISTRY.csv"
    json_path = out / "P126_DAILY_RUN_REGISTRY.json"
    report_path = out / "P126_RUN_REGISTRY_REPORT.md"
    manifest_path = out / "P126_RUN_REGISTRY_MANIFEST.json"

    _write_registry_csv(csv_path, rows)
    _write_json(json_path, {"version": VERSION, "rows": rows})
    _write(report_path, _report_markdown(rows))

    ready_count = len([row for row in rows if row["ready_for_operator_review"] == "true"])
    blocked_count = len(
        [row for row in rows if row["decision_status"] == "BLOCKED_REVIEW_REQUIRED"]
    )
    pending_count = len([row for row in rows if row["decision_status"].startswith("PENDING")])

    manifest = {
        "status": "RUN_REGISTRY_READY",
        "step": "P126_DAILY_RUN_REGISTRY_LOCAL_ONLY",
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": request.generated_at_utc,
        "output_dir": str(out),
        "exports_dir": str(exports),
        "row_count": len(rows),
        "ready_for_operator_review_count": ready_count,
        "blocked_review_required_count": blocked_count,
        "pending_count": pending_count,
        "human_review_only": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "no_order_no_sizing": True,
        "safety_markers": list(SAFETY_MARKERS),
        "files": [str(csv_path), str(json_path), str(report_path)],
        "next": "P127_OPERATOR_RUN_SHORTCUT_OR_REAL_GEM_TEST",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.daily_run_registry",
        description="Create a local P126 daily run registry from P124/P125 export folders.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--exports-dir", required=True)
    parser.add_argument("--run-id", default="P126-DAILY-RUN-REGISTRY")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_daily_run_registry(
        DailyRunRegistryRequest(
            output_dir=args.output_dir,
            exports_dir=args.exports_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            limit=args.limit,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["row_count"])
    print(result["ready_for_operator_review_count"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
