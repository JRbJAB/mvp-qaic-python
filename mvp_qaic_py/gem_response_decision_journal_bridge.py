from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE_0_1_0_SAFE"

SAFETY_MARKERS = (
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "LOCAL_ONLY",
    "DECISION_JOURNAL_BRIDGE_LOCAL_ONLY",
    "NO_AUTO_APPLY_GEM_RESPONSE",
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
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

JOURNAL_FIELDS = (
    "journal_entry_id",
    "journal_status",
    "decision_status",
    "source_step",
    "source_response_run_id",
    "source_prompt_run_id",
    "generated_at_utc",
    "missing_data_count",
    "blocker_count",
    "review_queue_rows",
    "summary",
    "missing_data",
    "blockers",
    "required_human_action",
    "human_review_only",
    "no_order_no_sizing",
    "no_sheet_write",
    "no_auto_apply_gem_response",
    "notes",
)


@dataclass(frozen=True)
class DecisionJournalBridgeRequest:
    output_dir: str | Path
    response_capture_json_file: str | Path
    journal_entry_id: str = "P120-JOURNAL-ENTRY"
    generated_at_utc: str | None = None
    notes: str | None = None


def load_response_capture(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("response_capture_json_file must contain a JSON object.")
    if payload.get("step") != "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE":
        raise ValueError("response_capture_json_file is not a P119 response capture.")
    return payload


def build_bridge_contract() -> dict[str, Any]:
    return {
        "contract": "P120_GEM_RESPONSE_TO_DECISION_JOURNAL_BRIDGE_LOCAL_ONLY",
        "version": VERSION,
        "status": "LOCAL_ONLY_HUMAN_REVIEW_READY",
        "purpose": "Convert P119 GEM response capture into a local decision journal entry candidate.",
        "input": "P119_RESPONSE_CAPTURE.json",
        "outputs": [
            "P120_DECISION_JOURNAL_ENTRY.json",
            "P120_DECISION_JOURNAL_ENTRY.csv",
            "P120_SOURCE_CAPTURE_SNAPSHOT.json",
            "P120_BRIDGE_CONTRACT.json",
            "P120_BRIDGE_MANIFEST.json",
            "P120_BRIDGE_REPORT.md",
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


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value]
    return [json.dumps(value, ensure_ascii=False, sort_keys=True)]


def _build_required_action(
    decision_status: str, missing_data: list[str], blockers: list[str]
) -> str:
    if blockers or decision_status == "BLOCKED":
        return "Resolve blockers manually before any journal acceptance or downstream bridge."
    if missing_data:
        return "Complete missing data manually or keep journal_status=REVIEW_REQUIRED."
    return "Manual verification required before accepting this journal entry candidate."


def build_decision_journal_entry(
    capture: Mapping[str, Any],
    *,
    journal_entry_id: str,
    generated_at_utc: str | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    missing_data = _as_list(capture.get("missing_data"))
    blockers = _as_list(capture.get("blockers"))
    review_queue_rows = capture.get("review_queue_rows") or []
    decision_status = str(
        capture.get("decision_status") or capture.get("status") or "REVIEW_REQUIRED"
    )

    if blockers or decision_status == "BLOCKED":
        journal_status = "BLOCKED"
    else:
        journal_status = "REVIEW_REQUIRED"

    structured_response = capture.get("structured_response")
    summary = ""
    if isinstance(structured_response, dict):
        summary = str(structured_response.get("summary") or "")
    if not summary:
        summary = "Local P120 journal entry candidate generated from P119 capture."

    entry = {
        "journal_entry_id": journal_entry_id,
        "journal_status": journal_status,
        "decision_status": decision_status,
        "source_step": capture.get("step"),
        "source_response_run_id": capture.get("response_run_id"),
        "source_prompt_run_id": capture.get("source_prompt_run_id"),
        "generated_at_utc": generated_at_utc or capture.get("generated_at_utc"),
        "missing_data_count": len(missing_data),
        "blocker_count": len(blockers),
        "review_queue_rows": len(review_queue_rows) if isinstance(review_queue_rows, list) else 0,
        "summary": summary,
        "missing_data": missing_data,
        "blockers": blockers,
        "required_human_action": _build_required_action(decision_status, missing_data, blockers),
        "human_review_only": True,
        "no_order_no_sizing": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "notes": notes,
        "safety_markers": list(SAFETY_MARKERS),
    }
    return entry


def _flatten_for_csv(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None:
        return ""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    return str(value)


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_journal_csv(path: Path, entry: Mapping[str, Any]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(JOURNAL_FIELDS))
        writer.writeheader()
        writer.writerow({field: _flatten_for_csv(entry.get(field)) for field in JOURNAL_FIELDS})


def _report_markdown(entry: Mapping[str, Any], output_dir: str) -> str:
    return "\n".join(
        [
            "# P120 GEM Response To Decision Journal Bridge Report",
            "",
            f"- journal_status: {entry['journal_status']}",
            f"- decision_status: {entry['decision_status']}",
            f"- version: {VERSION}",
            f"- output_dir: {output_dir}",
            f"- source_response_run_id: {entry['source_response_run_id']}",
            f"- source_prompt_run_id: {entry['source_prompt_run_id']}",
            f"- missing_data_count: {entry['missing_data_count']}",
            f"- blocker_count: {entry['blocker_count']}",
            f"- review_queue_rows: {entry['review_queue_rows']}",
            "- safety: LOCAL_ONLY / HUMAN_REVIEW_ONLY / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING",
            "",
            "## Required human action",
            "",
            str(entry["required_human_action"]),
            "",
            "## Next",
            "",
            "P121_DAILY_GEM_LOOP_END_TO_END_LOCAL_SMOKE",
            "",
        ]
    )


def write_decision_journal_bridge_pack(request: DecisionJournalBridgeRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    capture = load_response_capture(request.response_capture_json_file)
    entry = build_decision_journal_entry(
        capture,
        journal_entry_id=request.journal_entry_id,
        generated_at_utc=request.generated_at_utc,
        notes=request.notes,
    )

    entry_json_path = out / "P120_DECISION_JOURNAL_ENTRY.json"
    entry_csv_path = out / "P120_DECISION_JOURNAL_ENTRY.csv"
    capture_snapshot_path = out / "P120_SOURCE_CAPTURE_SNAPSHOT.json"
    contract_path = out / "P120_BRIDGE_CONTRACT.json"
    manifest_path = out / "P120_BRIDGE_MANIFEST.json"
    report_path = out / "P120_BRIDGE_REPORT.md"

    _write_json(entry_json_path, entry)
    _write_journal_csv(entry_csv_path, entry)
    _write_json(capture_snapshot_path, capture)
    _write_json(contract_path, build_bridge_contract())

    manifest = {
        "status": "EXPORTED",
        "step": "P120_GEM_RESPONSE_TO_DECISION_JOURNAL_BRIDGE_LOCAL_ONLY",
        "version": VERSION,
        "output_dir": str(out),
        "journal_entry_id": entry["journal_entry_id"],
        "journal_status": entry["journal_status"],
        "decision_status": entry["decision_status"],
        "files": [
            str(entry_json_path),
            str(entry_csv_path),
            str(capture_snapshot_path),
            str(contract_path),
            str(report_path),
        ],
        "safety_markers": list(SAFETY_MARKERS),
    }
    _write_json(manifest_path, manifest)
    report_path.write_text(_report_markdown(entry, str(out)), encoding="utf-8")
    manifest["files"].append(str(manifest_path))

    return {
        "status": "EXPORTED",
        "step": "P120_GEM_RESPONSE_TO_DECISION_JOURNAL_BRIDGE_LOCAL_ONLY",
        "output_dir": str(out),
        "journal_entry_id": entry["journal_entry_id"],
        "journal_status": entry["journal_status"],
        "decision_status": entry["decision_status"],
        "missing_data_count": entry["missing_data_count"],
        "blocker_count": entry["blocker_count"],
        "files": manifest["files"],
        "safety_markers": list(SAFETY_MARKERS),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_response_decision_journal_bridge",
        description="Bridge P119 response capture to a local decision journal entry candidate.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--response-capture-json-file", required=True)
    parser.add_argument("--journal-entry-id", default="P120-JOURNAL-ENTRY")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_decision_journal_bridge_pack(
        DecisionJournalBridgeRequest(
            output_dir=args.output_dir,
            response_capture_json_file=args.response_capture_json_file,
            journal_entry_id=args.journal_entry_id,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["journal_status"])
    print(result["decision_status"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
