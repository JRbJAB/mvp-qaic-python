from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P125_REAL_GEM_MANUAL_TEST_REVIEW_UX_0_1_0_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "HUMAN_REVIEW_ONLY",
    "REVIEW_UX_ONLY",
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

FORBIDDEN_TERMS = (
    "place order",
    "execute order",
    "submit order",
    "buy automatically",
    "sell automatically",
    "auto sizing",
    "revolut x real access",
    "broker execution",
)


@dataclass(frozen=True)
class ManualTestReviewRequest:
    output_dir: str | Path
    p124_run_dir: str | Path | None = None
    exports_dir: str | Path | None = None
    run_id: str = "P125-REVIEW"
    generated_at_utc: str | None = None
    notes: str | None = None


def discover_latest_p124_run_dir(exports_dir: str | Path) -> Path | None:
    root = Path(exports_dir)
    if not root.exists():
        return None
    candidates = [
        path for path in root.glob("P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_*") if path.is_dir()
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[0]


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8-sig")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _is_template_portfolio(text: str) -> bool:
    normalized = text.lower()
    return (
        "portfolio input for mvp qaic gem manual test" in normalized
        and "paste or type the portfolio snapshot here" in normalized
    )


def _is_template_gem_response(text: str) -> bool:
    normalized = text.lower()
    return "gem response paste area" in normalized and "paste the gem response here" in normalized


def _find_forbidden_terms(text: str) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for term in FORBIDDEN_TERMS:
        if term in lowered:
            found.append(f"FORBIDDEN_TERM_REVIEW:{term}")
    return found


def _status_from_findings(
    portfolio_missing: bool,
    gem_response_missing: bool,
    forbidden_findings: list[str],
) -> str:
    if forbidden_findings:
        return "BLOCKED_REVIEW_REQUIRED"
    if portfolio_missing:
        return "PENDING_PORTFOLIO_INPUT"
    if gem_response_missing:
        return "PENDING_GEM_RESPONSE"
    return "READY_FOR_OPERATOR_REVIEW"


def build_review_contract() -> dict[str, Any]:
    return {
        "contract": "P125_REAL_GEM_MANUAL_TEST_REVIEW_UX_PACK",
        "version": VERSION,
        "status": "REVIEW_UX_READY",
        "purpose": "Review a P124 local input helper folder and prepare operator dashboard for real GEM manual test.",
        "inputs": [
            "P124 folder",
            "portfolio_input.txt",
            "gem_response.txt",
            "P124_OPERATOR_COMMANDS.md",
        ],
        "outputs": [
            "P125_OPERATOR_REVIEW_DASHBOARD.md",
            "P125_REAL_GEM_TEST_SUMMARY.md",
            "P125_MISSING_DATA_AND_BLOCKERS.csv",
            "P125_NEXT_ACTIONS.md",
            "P125_REVIEW_CONTRACT.json",
            "P125_RUN_MANIFEST.json",
        ],
        "forbidden": [
            "auto_apply_gem_response",
            "apps_script_execution",
            "sheet_write",
            "clasp_push",
            "public_deploy",
            "broker_execution",
            "order_execution",
            "cancel_order",
            "replace_order",
            "auto_sizing",
            "revolutx_real_access_from_mvp",
            "secret_logging",
        ],
        "safety_markers": list(SAFETY_MARKERS),
    }


def _build_rows(
    portfolio_missing: bool,
    gem_response_missing: bool,
    forbidden_findings: list[str],
    p124_dir_missing: bool,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if p124_dir_missing:
        rows.append(
            {
                "kind": "missing_data",
                "code": "P124_RUN_DIR_MISSING",
                "severity": "BLOCKING",
                "detail": "No P124 run directory was provided or discovered.",
                "operator_action": "Run P124 or pass --p124-run-dir.",
            }
        )
    if portfolio_missing:
        rows.append(
            {
                "kind": "missing_data",
                "code": "PORTFOLIO_INPUT_NOT_FILLED",
                "severity": "REVIEW",
                "detail": "portfolio_input.txt is missing or still looks like the default template.",
                "operator_action": "Fill portfolio_input.txt with the real portfolio snapshot.",
            }
        )
    if gem_response_missing:
        rows.append(
            {
                "kind": "missing_data",
                "code": "GEM_RESPONSE_NOT_FILLED",
                "severity": "REVIEW",
                "detail": "gem_response.txt is missing or still looks like the default template.",
                "operator_action": "Paste the real GEM response into gem_response.txt.",
            }
        )
    for finding in forbidden_findings:
        rows.append(
            {
                "kind": "blocker",
                "code": finding,
                "severity": "BLOCKING",
                "detail": "Potential forbidden execution wording detected in input or GEM response.",
                "operator_action": "Review manually and remove any request for order, sizing, broker or Revolut X real access.",
            }
        )
    return rows


def _write_rows_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["kind", "code", "severity", "detail", "operator_action"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def _dashboard_md(
    status: str,
    p124_run_dir: Path | None,
    rows: list[dict[str, str]],
    portfolio_len: int,
    gem_len: int,
) -> str:
    if rows:
        findings_lines = [
            f"- `{row['severity']}` / `{row['kind']}` / `{row['code']}` - {row['operator_action']}"
            for row in rows
        ]
    else:
        findings_lines = ["- No blockers or missing data detected by P125."]

    lines = [
        "# P125 Operator Review Dashboard",
        "",
        f"- decision_status: `{status}`",
        f"- p124_run_dir: `{str(p124_run_dir) if p124_run_dir else 'NOT_FOUND'}`",
        f"- portfolio_text_chars: `{portfolio_len}`",
        f"- gem_response_chars: `{gem_len}`",
        f"- finding_count: `{len(rows)}`",
        "",
        "## Findings",
        "",
    ]
    lines.extend(findings_lines)
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "- HUMAN_REVIEW_ONLY",
            "- NO_AUTO_APPLY_GEM_RESPONSE",
            "- NO_SHEET_WRITE",
            "- NO_BROKER",
            "- NO_ORDER",
            "- NO_AUTO_SIZING",
            "- NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
            "",
        ]
    )
    return "\n".join(lines)


def _summary_md(status: str, rows: list[dict[str, str]]) -> str:
    blocker_count = len([row for row in rows if row["kind"] == "blocker"])
    missing_count = len([row for row in rows if row["kind"] == "missing_data"])
    return "\n".join(
        [
            "# P125 Real GEM Test Summary",
            "",
            f"- status: `{status}`",
            f"- missing_data_count: `{missing_count}`",
            f"- blocker_count: `{blocker_count}`",
            "- local_only: `true`",
            "- no_sheet_write: `true`",
            "- no_auto_apply_gem_response: `true`",
            "",
        ]
    )


def _next_actions_md(status: str) -> str:
    if status == "PENDING_PORTFOLIO_INPUT":
        actions = [
            "Fill `portfolio_input.txt` in the P124 folder.",
            "Then run P118 from `P124_OPERATOR_COMMANDS.md`.",
        ]
    elif status == "PENDING_GEM_RESPONSE":
        actions = [
            "Generate the prompt with P118.",
            "Paste the prompt manually into GEM.",
            "Paste GEM output into `gem_response.txt`.",
            "Then run P119/P120 commands.",
        ]
    elif status == "BLOCKED_REVIEW_REQUIRED":
        actions = [
            "Resolve blockers before continuing.",
            "Do not execute orders, sizing, broker calls, or Revolut X real access from MVP.",
        ]
    else:
        actions = [
            "Run P119 response capture if not already done.",
            "Run P120 local decision journal bridge.",
            "Review outputs manually before any further action.",
        ]
    return "\n".join(
        [
            "# P125 Next Actions",
            "",
            *[f"- {action}" for action in actions],
            "",
        ]
    )


def write_manual_test_review_pack(request: ManualTestReviewRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    p124_run_dir: Path | None
    if request.p124_run_dir:
        p124_run_dir = Path(request.p124_run_dir)
    elif request.exports_dir:
        p124_run_dir = discover_latest_p124_run_dir(request.exports_dir)
    else:
        p124_run_dir = None

    p124_dir_missing = p124_run_dir is None or not p124_run_dir.exists()

    portfolio_text = ""
    gem_response_text = ""
    if not p124_dir_missing and p124_run_dir is not None:
        portfolio_text = _read_text(p124_run_dir / "portfolio_input.txt")
        gem_response_text = _read_text(p124_run_dir / "gem_response.txt")

    portfolio_missing = not portfolio_text.strip() or _is_template_portfolio(portfolio_text)
    gem_response_missing = not gem_response_text.strip() or _is_template_gem_response(
        gem_response_text
    )
    forbidden_findings = _find_forbidden_terms("\n".join([portfolio_text, gem_response_text]))

    status = _status_from_findings(
        portfolio_missing=portfolio_missing,
        gem_response_missing=gem_response_missing,
        forbidden_findings=forbidden_findings,
    )
    rows = _build_rows(
        portfolio_missing=portfolio_missing,
        gem_response_missing=gem_response_missing,
        forbidden_findings=forbidden_findings,
        p124_dir_missing=p124_dir_missing,
    )

    dashboard_path = out / "P125_OPERATOR_REVIEW_DASHBOARD.md"
    summary_path = out / "P125_REAL_GEM_TEST_SUMMARY.md"
    findings_path = out / "P125_MISSING_DATA_AND_BLOCKERS.csv"
    next_actions_path = out / "P125_NEXT_ACTIONS.md"
    contract_path = out / "P125_REVIEW_CONTRACT.json"
    manifest_path = out / "P125_RUN_MANIFEST.json"

    _write(
        dashboard_path,
        _dashboard_md(
            status=status,
            p124_run_dir=p124_run_dir,
            rows=rows,
            portfolio_len=len(portfolio_text),
            gem_len=len(gem_response_text),
        ),
    )
    _write(summary_path, _summary_md(status, rows))
    _write(next_actions_path, _next_actions_md(status))
    _write_rows_csv(findings_path, rows)
    _write_json(contract_path, build_review_contract())

    manifest = {
        "status": status,
        "step": "P125_REAL_GEM_MANUAL_TEST_REVIEW_UX_PACK",
        "version": VERSION,
        "run_id": request.run_id,
        "output_dir": str(out),
        "generated_at_utc": request.generated_at_utc,
        "p124_run_dir": str(p124_run_dir) if p124_run_dir else None,
        "p124_dir_missing": p124_dir_missing,
        "portfolio_missing": portfolio_missing,
        "gem_response_missing": gem_response_missing,
        "finding_count": len(rows),
        "blocker_count": len([row for row in rows if row["kind"] == "blocker"]),
        "missing_data_count": len([row for row in rows if row["kind"] == "missing_data"]),
        "human_review_only": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "no_order_no_sizing": True,
        "safety_markers": list(SAFETY_MARKERS),
        "files": [
            str(dashboard_path),
            str(summary_path),
            str(findings_path),
            str(next_actions_path),
            str(contract_path),
        ],
        "next": "REAL_GEM_TEST_OR_P126_DAILY_RUN_REGISTRY",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_manual_test_review_pack",
        description="Create P125 operator review dashboard for a P124 real GEM manual test folder.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--p124-run-dir")
    parser.add_argument("--exports-dir")
    parser.add_argument("--run-id", default="P125-REVIEW")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_manual_test_review_pack(
        ManualTestReviewRequest(
            output_dir=args.output_dir,
            p124_run_dir=args.p124_run_dir,
            exports_dir=args.exports_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["finding_count"])
    print(result["blocker_count"])
    print(result["missing_data_count"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
