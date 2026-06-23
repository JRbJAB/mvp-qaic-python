from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P145_GEM_RESPONSE_IMPORT_E2E_1.0.0_SAFE"
STATUS_IMPORTED = "P145_GEM_RESPONSE_IMPORT_E2E_VALIDATED_LOCAL_REVIEW"

SAFETY_MARKERS = {
    "source": "LOCAL_GEM_RESPONSE_FILE_OR_FIXTURE",
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "human_review_required": True,
}


@dataclass(frozen=True)
class ImportRequest:
    p144_model_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str
    gem_response_file: Path | None
    use_fixture: bool


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_response(path: Path) -> tuple[str, dict[str, Any] | None]:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return text, json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if match:
            try:
                return text, json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return text, None


def build_fixture_response() -> dict[str, Any]:
    return {
        "status": "REVIEW_REQUIRED",
        "source_type": "fixture",
        "reference_currency": "USD",
        "image_used": True,
        "human_review_required": True,
        "no_order_no_sizing": True,
        "portfolio_total_value": 655.66,
        "assets": [
            {"symbol": "BTC", "value": 416.92, "allocation_pct": 63.59, "pnl": -117.69},
            {"symbol": "USDC", "value": 198.75, "allocation_pct": 30.31, "pnl": 0.06},
            {"symbol": "CASH", "value": 39.99, "allocation_pct": 6.10, "pnl": 0.0},
        ],
        "blockers": ["HUMAN_REVIEW_REQUIRED", "NO_AUTO_APPLY"],
        "notes_fr": "Fixture locale P145 pour valider le chemin import GEM sans ordre ni sizing.",
    }


def validate_response(payload: dict[str, Any] | None) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []

    if payload is None:
        return {
            "status": "BLOCKED",
            "blockers": ["NO_JSON_PAYLOAD_DETECTED"],
            "warnings": [],
            "human_review_required": True,
            "no_auto_apply": True,
            "no_order_no_sizing": True,
        }

    if payload.get("status") not in {"REVIEW_REQUIRED", "OK", "BLOCKED"}:
        blockers.append("INVALID_OR_MISSING_STATUS")
    if payload.get("human_review_required") is not True:
        blockers.append("HUMAN_REVIEW_REQUIRED_NOT_TRUE")
    if payload.get("no_order_no_sizing") is not True:
        blockers.append("NO_ORDER_NO_SIZING_NOT_TRUE")

    if payload.get("reference_currency") not in {"USD", "EUR", "USDC"}:
        warnings.append("REFERENCE_CURRENCY_REVIEW")

    if "NO_AUTO_APPLY" not in json.dumps(payload, ensure_ascii=False):
        warnings.append("NO_AUTO_APPLY_MARKER_NOT_EXPLICIT")

    status = "VALIDATED_FOR_HUMAN_REVIEW" if not blockers else "BLOCKED"
    return {
        "status": status,
        "blockers": blockers,
        "warnings": warnings,
        "human_review_required": True,
        "no_auto_apply": True,
        "no_order_no_sizing": True,
    }


def build_import_payload(
    p144_model: dict[str, Any],
    response_payload: dict[str, Any] | None,
    raw_text: str,
    *,
    source_path: str,
    fixture_used: bool,
) -> dict[str, Any]:
    if p144_model.get("status") != "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY":
        raise ValueError(f"Invalid P144 model status: {p144_model.get('status')}")

    validation = validate_response(response_payload)
    return {
        "status": STATUS_IMPORTED
        if validation["status"] != "BLOCKED"
        else "P145_GEM_RESPONSE_IMPORT_BLOCKED_REVIEW",
        "version": VERSION,
        "source_p144_status": p144_model.get("status"),
        "workflow_step_count": p144_model.get("workflow_step_count"),
        "gem_response_source_path": source_path,
        "fixture_used": fixture_used,
        "raw_text_length": len(raw_text or ""),
        "response_payload": response_payload,
        "validation": validation,
        "review_queue_item": {
            "review_id": "P145-GEM-RESPONSE-REVIEW-001",
            "status": "REVIEW_REQUIRED",
            "decision_required": "ACCEPT_FOR_ANALYSIS_OR_REJECT_AND_CORRECT_PROMPT",
            "allowed_actions": ["HUMAN_REVIEW", "PROMPT_CORRECTION", "SAVE_LOCAL_REPORT"],
            "blocked_actions": ["ORDER", "SIZING", "AUTO_APPLY", "SHEET_WRITE"],
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "P146_CORRECTION_QUEUE_UI",
    }


def render_review_app(import_payload: dict[str, Any]) -> str:
    payload_repr = repr(json.dumps(import_payload, ensure_ascii=False, indent=2, sort_keys=True))
    return "\n".join(
        [
            "from __future__ import annotations",
            "import json",
            "from nicegui import ui",
            "",
            f"PAYLOAD = json.loads({payload_repr})",
            "",
            "@ui.page('/')",
            "def index():",
            "    ui.label('MVP QAIC — GEM Response Review').classes('text-h4')",
            "    ui.label('Human review only — no order / no sizing / no auto apply').classes('text-caption')",
            "    with ui.row().classes('q-gutter-sm q-mt-md'):",
            "        ui.badge(PAYLOAD['status'])",
            "        ui.badge(PAYLOAD['validation']['status'])",
            "        ui.badge('fixture' if PAYLOAD['fixture_used'] else 'real file')",
            "    ui.separator().classes('q-my-md')",
            "    ui.label('Validation blockers').classes('text-subtitle1')",
            "    for blocker in PAYLOAD['validation'].get('blockers', []):",
            "        ui.label('BLOCKER: ' + blocker).classes('text-negative')",
            "    ui.label('Warnings').classes('text-subtitle1 q-mt-md')",
            "    for warning in PAYLOAD['validation'].get('warnings', []):",
            "        ui.label('WARNING: ' + warning)",
            "    ui.separator().classes('q-my-md')",
            "    ui.json_editor({'content': {'json': PAYLOAD.get('response_payload')}}).classes('w-full')",
            "",
            "if __name__ in {'__main__', '__mp_main__'}:",
            "    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)",
            "",
        ]
    )


def write_outputs(import_payload: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    import_path = output_dir / "P145_GEM_RESPONSE_IMPORT_PAYLOAD.json"
    validation_path = output_dir / "P145_GEM_RESPONSE_VALIDATION_REPORT.json"
    app_path = output_dir / "P145_NICEGUI_GEM_RESPONSE_REVIEW_APP.py"
    md_path = output_dir / "P145_GEM_RESPONSE_IMPORT_E2E.md"
    summary_path = output_dir / "P145_SUMMARY.json"

    import_path.write_text(
        json.dumps(import_payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    validation_path.write_text(
        json.dumps(import_payload["validation"], ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    app_path.write_text(render_review_app(import_payload), encoding="utf-8")

    md_path.write_text(
        "\n".join(
            [
                "# P145 — GEM Response Import E2E",
                "",
                f"- Status: `{import_payload['status']}`",
                f"- Validation: `{import_payload['validation']['status']}`",
                f"- Fixture used: `{import_payload['fixture_used']}`",
                "",
                "## Safety",
                "",
                "- Human review required",
                "- No auto apply GEM response",
                "- No Sheet write",
                "- No broker/order/sizing",
                "- No public deploy",
                "",
                f"Next: `{import_payload['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": import_payload["status"],
        "validation_status": import_payload["validation"]["status"],
        "blocker_count": len(import_payload["validation"]["blockers"]),
        "warning_count": len(import_payload["validation"]["warnings"]),
        "fixture_used": import_payload["fixture_used"],
        "human_review_required": True,
        "google_sheets_write": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "auto_apply_gem_response": False,
        "output_dir": str(output_dir),
        "next": import_payload["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    return {
        "import_payload_json": str(import_path),
        "validation_report_json": str(validation_path),
        "review_app_py": str(app_path),
        "markdown": str(md_path),
        "summary_json": str(summary_path),
    }


def run_import(request: ImportRequest) -> dict[str, Any]:
    p144_model = load_json(request.p144_model_path)

    fixture_used = False
    source_path = ""
    if request.gem_response_file:
        raw_text, response_payload = read_response(request.gem_response_file)
        source_path = str(request.gem_response_file)
    elif request.use_fixture:
        response_payload = build_fixture_response()
        raw_text = json.dumps(response_payload, ensure_ascii=False, indent=2)
        fixture_used = True
        source_path = "BUILTIN_P145_FIXTURE"
    else:
        raise ValueError("Provide --gem-response-file or --use-fixture")

    import_payload = build_import_payload(
        p144_model,
        response_payload,
        raw_text,
        source_path=source_path,
        fixture_used=fixture_used,
    )
    import_payload["run_id"] = request.run_id
    import_payload["generated_at_utc"] = request.generated_at_utc
    import_payload["source_p144_model_path"] = str(request.p144_model_path)
    outputs = write_outputs(import_payload, request.output_dir)
    import_payload["output_files"] = outputs
    (request.output_dir / "P145_GEM_RESPONSE_IMPORT_PAYLOAD.json").write_text(
        json.dumps(import_payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return import_payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P145 GEM response import E2E.")
    parser.add_argument("--p144-model", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--gem-response-file", default=None)
    parser.add_argument("--use-fixture", action="store_true")
    parser.add_argument("--run-id", default="P145-GEM-RESPONSE-IMPORT-E2E")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    payload = run_import(
        ImportRequest(
            p144_model_path=Path(args.p144_model),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            gem_response_file=Path(args.gem_response_file) if args.gem_response_file else None,
            use_fixture=bool(args.use_fixture),
        )
    )
    print(payload["status"])
    print(f"validation_status={payload['validation']['status']}")
    print(f"fixture_used={str(payload['fixture_used']).lower()}")
    print("human_review_required=true")
    print("google_sheets_write=false")
    print("broker=false")
    print("order=false")
    print("sizing=false")
    print("auto_apply_gem_response=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
