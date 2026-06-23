from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P152_REAL_GEM_RESPONSE_IMPORT_OR_STOP_1.0.0_SAFE"
STATUS_IMPORTED = "P152_REAL_GEM_RESPONSE_IMPORTED_LOCAL_REVIEW"
STATUS_STOP = "P152_STOP_WAIT_REAL_GEM_RESPONSE_FILE_READY"

SAFETY_MARKERS = {
    "real_file_import_only": True,
    "fixture_allowed": False,
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
class RealImportRequest:
    p151_summary_path: Path
    gem_response_file: Path | None
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_json_payload(text: str) -> dict[str, Any] | None:
    try:
        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.S)
    if match:
        try:
            payload = json.loads(match.group(0))
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            return None
    return None


def read_real_response(path: Path) -> tuple[str, dict[str, Any] | None]:
    text = path.read_text(encoding="utf-8-sig")
    return text, extract_json_payload(text)


def validate_p151(summary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if summary.get("status") != "P151_RELEASE_PACK_VERIFY_LAUNCH_SMOKE_READY":
        blockers.append("P151_STATUS_NOT_READY")
    if summary.get("launch_smoke_ready") is not True:
        blockers.append("P151_LAUNCH_SMOKE_NOT_READY")
    if summary.get("google_sheets_write") is not False:
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    if summary.get("public_deploy") is not False:
        blockers.append("PUBLIC_DEPLOY_NOT_FALSE")
    if summary.get("server_launch_executed") is not False:
        blockers.append("SERVER_LAUNCH_WAS_EXECUTED")
    return blockers


def validate_real_payload(payload: dict[str, Any] | None, raw_text: str) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []

    if not raw_text.strip():
        blockers.append("EMPTY_GEM_RESPONSE_FILE")
    if payload is None:
        blockers.append("NO_JSON_PAYLOAD_DETECTED")
        return {
            "status": "BLOCKED",
            "blockers": blockers,
            "warnings": warnings,
            "human_review_required": True,
            "no_auto_apply": True,
            "no_order_no_sizing": True,
        }

    if payload.get("human_review_required") is not True:
        blockers.append("HUMAN_REVIEW_REQUIRED_NOT_TRUE")
    if payload.get("no_order_no_sizing") is not True:
        blockers.append("NO_ORDER_NO_SIZING_NOT_TRUE")
    if "NO_AUTO_APPLY" not in json.dumps(payload, ensure_ascii=False):
        warnings.append("NO_AUTO_APPLY_MARKER_NOT_EXPLICIT")
    if payload.get("status") not in {"REVIEW_REQUIRED", "OK", "BLOCKED"}:
        warnings.append("STATUS_ENUM_REVIEW")
    if payload.get("image_used") is not True and payload.get("source_type") == "image":
        warnings.append("IMAGE_SOURCE_WITHOUT_IMAGE_USED_TRUE")

    return {
        "status": "VALIDATED_FOR_HUMAN_REVIEW" if not blockers else "BLOCKED",
        "blockers": blockers,
        "warnings": warnings,
        "human_review_required": True,
        "no_auto_apply": True,
        "no_order_no_sizing": True,
    }


def build_stop_report(p151_summary: dict[str, Any], p151_blockers: list[str]) -> dict[str, Any]:
    blockers = list(p151_blockers)
    return {
        "status": "P152_STOP_BLOCKED_BY_P151" if blockers else STATUS_STOP,
        "version": VERSION,
        "mode": "STOP_WAIT_REAL_GEM_RESPONSE_FILE",
        "source_p151_status": p151_summary.get("status"),
        "real_gem_file_provided": False,
        "validation_status": "NOT_RUN_WAIT_REAL_FILE",
        "blocker_count": len(blockers),
        "warning_count": 0,
        "blockers": blockers,
        "warnings": [],
        "operator_instruction": "Définir $env:MVP_QAIC_GEM_RESPONSE_FILE vers un fichier JSON/TXT de réponse GEM réelle puis relancer P152.",
        "safety": dict(SAFETY_MARKERS),
        "next": "WAIT_REAL_GEM_RESPONSE_FILE_OR_STOP",
    }


def build_import_report(
    p151_summary: dict[str, Any],
    p151_blockers: list[str],
    gem_response_file: Path,
    raw_text: str,
    payload: dict[str, Any] | None,
) -> dict[str, Any]:
    validation = validate_real_payload(payload, raw_text)
    blockers = list(p151_blockers) + list(validation["blockers"])
    status = STATUS_IMPORTED if not blockers else "P152_REAL_GEM_RESPONSE_IMPORT_BLOCKED_REVIEW"

    return {
        "status": status,
        "version": VERSION,
        "mode": "REAL_GEM_RESPONSE_FILE_IMPORT",
        "source_p151_status": p151_summary.get("status"),
        "real_gem_file_provided": True,
        "gem_response_file": str(gem_response_file),
        "raw_text_length": len(raw_text),
        "json_payload_detected": payload is not None,
        "response_payload": payload,
        "validation": validation,
        "validation_status": validation["status"],
        "blocker_count": len(blockers),
        "warning_count": len(validation["warnings"]),
        "blockers": blockers,
        "warnings": validation["warnings"],
        "review_queue_item": {
            "review_id": "P152-REAL-GEM-REVIEW-001",
            "status": "REVIEW_REQUIRED",
            "allowed_actions": ["HUMAN_REVIEW", "PROMPT_CORRECTION", "SAVE_LOCAL_REPORT"],
            "blocked_actions": ["ORDER", "SIZING", "AUTO_APPLY", "SHEET_WRITE", "PUBLIC_DEPLOY"],
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "P153_CORRECTION_LOOP_REAL_CASE_OR_STOP",
    }


def write_outputs(report: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "P152_REAL_GEM_RESPONSE_IMPORT_REPORT.json"
    payload_path = output_dir / "P152_REAL_GEM_RESPONSE_PAYLOAD.json"
    md_path = output_dir / "P152_REAL_GEM_RESPONSE_IMPORT_OR_STOP.md"
    instruction_path = output_dir / "P152_REAL_GEM_RESPONSE_IMPORT_COMMANDS.md"
    summary_path = output_dir / "P152_SUMMARY.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    payload_path.write_text(
        json.dumps(report.get("response_payload"), ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    md_path.write_text(
        "\n".join(
            [
                "# P152 — Real GEM Response Import or Stop",
                "",
                f"- Status: `{report['status']}`",
                f"- Mode: `{report['mode']}`",
                f"- Real file provided: `{report['real_gem_file_provided']}`",
                f"- Validation: `{report['validation_status']}`",
                f"- Blockers: `{report['blocker_count']}`",
                f"- Warnings: `{report['warning_count']}`",
                "",
                "## Safety",
                "",
                "- No fixture in P152",
                "- No Sheet write",
                "- No public deploy",
                "- No broker/order/sizing",
                "- No auto apply GEM response",
                "",
                f"Next: `{report['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    instruction_path.write_text(
        "\n".join(
            [
                "# P152 — Commandes fichier GEM réel",
                "",
                "Avant relance avec un vrai fichier :",
                "",
                "```powershell",
                '$env:MVP_QAIC_GEM_RESPONSE_FILE = "C:\\chemin\\vers\\gem_response.json"',
                "```",
                "",
                "Le fichier peut être JSON pur ou texte contenant un bloc JSON.",
                "",
                "Garde-fous : aucun write Sheets, aucun public deploy, aucun ordre/sizing.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": report["status"],
        "mode": report["mode"],
        "real_gem_file_provided": report["real_gem_file_provided"],
        "validation_status": report["validation_status"],
        "json_payload_detected": report.get("json_payload_detected", False),
        "blocker_count": report["blocker_count"],
        "warning_count": report["warning_count"],
        "human_review_required": True,
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "auto_apply_gem_response": False,
        "output_dir": str(output_dir),
        "next": report["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "report_json": str(report_path),
        "payload_json": str(payload_path),
        "markdown": str(md_path),
        "commands_md": str(instruction_path),
        "summary_json": str(summary_path),
    }


def run_import_or_stop(request: RealImportRequest) -> dict[str, Any]:
    p151_summary = load_json(request.p151_summary_path)
    p151_blockers = validate_p151(p151_summary)

    if request.gem_response_file is None:
        report = build_stop_report(p151_summary, p151_blockers)
    else:
        if not request.gem_response_file.exists():
            report = build_stop_report(
                p151_summary, p151_blockers + ["REAL_GEM_RESPONSE_FILE_NOT_FOUND"]
            )
            report["operator_instruction"] = f"Fichier introuvable : {request.gem_response_file}"
        else:
            raw_text, payload = read_real_response(request.gem_response_file)
            report = build_import_report(
                p151_summary, p151_blockers, request.gem_response_file, raw_text, payload
            )

    report["run_id"] = request.run_id
    report["generated_at_utc"] = request.generated_at_utc
    report["source_p151_summary_path"] = str(request.p151_summary_path)
    outputs = write_outputs(report, request.output_dir)
    report["output_files"] = outputs
    (request.output_dir / "P152_REAL_GEM_RESPONSE_IMPORT_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P152 real GEM response import or stop.")
    parser.add_argument("--p151-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--gem-response-file", default=None)
    parser.add_argument("--run-id", default="P152-REAL-GEM-RESPONSE-IMPORT-OR-STOP")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_import_or_stop(
        RealImportRequest(
            p151_summary_path=Path(args.p151_summary),
            gem_response_file=Path(args.gem_response_file) if args.gem_response_file else None,
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(report["status"])
    print(f"mode={report['mode']}")
    print(f"real_gem_file_provided={str(report['real_gem_file_provided']).lower()}")
    print(f"validation_status={report['validation_status']}")
    print(f"blocker_count={report['blocker_count']}")
    print(f"warning_count={report['warning_count']}")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print("auto_apply_gem_response=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
