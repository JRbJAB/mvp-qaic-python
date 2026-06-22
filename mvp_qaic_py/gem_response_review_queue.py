from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .gem_prompt_runner_pack import build_expected_gem_output_schema

VERSION = "MVP_QAIC_P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE_0_1_0_SAFE"

SAFETY_MARKERS = (
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "LOCAL_ONLY",
    "GEM_RESPONSE_CAPTURE_ONLY",
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

FORBIDDEN_ACTION_TERMS = (
    "place an order",
    "place order",
    "execute order",
    "broker execution",
    "auto sizing",
    "autosizing",
    "cancel order",
    "replace order",
    "trailing stop order",
    "revolutx real access",
    "revolut x real access",
)

EXPECTED_STATUS_VALUES = (
    "REVIEW_REQUIRED",
    "BLOCKED",
    "READY_FOR_HUMAN_DECISION",
    "ACCEPTED_WITH_WARNINGS",
)


@dataclass(frozen=True)
class GemResponseCaptureRequest:
    output_dir: str | Path
    raw_response: str | None = None
    response_text_file: str | None = None
    response_json_file: str | None = None
    source_prompt_run_id: str | None = None
    response_run_id: str = "GEM-RESPONSE-CAPTURE"
    generated_at_utc: str | None = None
    notes: str | None = None


def _read_text(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8-sig")


def _read_json(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("response_json_file must contain a JSON object.")
    return payload


def _strip_markdown_json_fence(text: str) -> str:
    cleaned = text.lstrip("\ufeff").strip()
    if not cleaned.startswith("```"):
        return cleaned

    lines = cleaned.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).lstrip("\ufeff").strip()


def _try_parse_json(raw_response: str | None) -> dict[str, Any] | None:
    if not raw_response:
        return None

    cleaned = _strip_markdown_json_fence(raw_response)

    candidates = [cleaned]
    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first >= 0 and last > first:
        candidates.append(cleaned[first : last + 1])

    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return None


def _list_from_payload(payload: Mapping[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value]
    return [json.dumps(value, ensure_ascii=False, sort_keys=True)]


def detect_forbidden_action_blockers(text: str) -> list[str]:
    lower = text.lower()
    blockers: list[str] = []
    for term in FORBIDDEN_ACTION_TERMS:
        if term in lower:
            blockers.append(f"FORBIDDEN_ACTION_TERM:{term}")
    return blockers


def build_capture_contract() -> dict[str, Any]:
    return {
        "contract": "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
        "version": VERSION,
        "status": "LOCAL_ONLY_CAPTURE_AND_REVIEW",
        "purpose": "Capture GEM response and convert it into a local human review queue.",
        "accepted_inputs": [
            "raw_response",
            "response_text_file",
            "response_json_file",
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


def build_review_queue_rows(capture: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for blocker in capture["blockers"]:
        rows.append(
            {
                "queue_id": f"BLOCKER-{len(rows) + 1:03d}",
                "priority": "P0",
                "review_status": "BLOCKED",
                "item_type": "blocker",
                "item_value": blocker,
                "required_action": "Resolve or reject before any downstream use.",
                "human_review_only": "TRUE",
                "no_order_no_sizing": "TRUE",
            }
        )

    for missing in capture["missing_data"]:
        rows.append(
            {
                "queue_id": f"MISSING-{len(rows) + 1:03d}",
                "priority": "P1",
                "review_status": "REVIEW_REQUIRED",
                "item_type": "missing_data",
                "item_value": missing,
                "required_action": "Provide missing data or keep decision_status=REVIEW_REQUIRED.",
                "human_review_only": "TRUE",
                "no_order_no_sizing": "TRUE",
            }
        )

    if not rows:
        rows.append(
            {
                "queue_id": "REVIEW-001",
                "priority": "P1",
                "review_status": "REVIEW_REQUIRED",
                "item_type": "response_review",
                "item_value": "Manual review of GEM response required before journal bridge.",
                "required_action": "Read response, verify facts, then decide whether to bridge to P120.",
                "human_review_only": "TRUE",
                "no_order_no_sizing": "TRUE",
            }
        )

    return rows


def build_response_capture(request: GemResponseCaptureRequest) -> dict[str, Any]:
    raw_from_file = _read_text(request.response_text_file)
    structured_from_file = _read_json(request.response_json_file)

    provided_inputs = [
        bool(request.raw_response),
        bool(raw_from_file),
        bool(structured_from_file),
    ]
    if sum(provided_inputs) == 0:
        raise ValueError("Provide raw_response, response_text_file, or response_json_file.")
    if sum(provided_inputs) > 1:
        raise ValueError("Use only one GEM response input source per capture.")

    raw_response = request.raw_response or raw_from_file
    structured_response = structured_from_file or _try_parse_json(raw_response)

    if raw_response is not None:
        response_text = raw_response
    else:
        response_text = json.dumps(
            structured_response, ensure_ascii=False, indent=2, sort_keys=True
        )

    forbidden_blockers = detect_forbidden_action_blockers(response_text)
    payload_missing = _list_from_payload(structured_response or {}, "missing_data")
    payload_blockers = _list_from_payload(structured_response or {}, "blockers")
    payload_decision_status = (structured_response or {}).get("decision_status")

    blockers = [*payload_blockers, *forbidden_blockers]
    decision_status = "BLOCKED" if blockers else "REVIEW_REQUIRED"
    if (
        isinstance(payload_decision_status, str)
        and payload_decision_status in EXPECTED_STATUS_VALUES
        and not blockers
    ):
        decision_status = payload_decision_status

    capture: dict[str, Any] = {
        "step": "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
        "version": VERSION,
        "status": decision_status,
        "source_prompt_run_id": request.source_prompt_run_id,
        "response_run_id": request.response_run_id,
        "generated_at_utc": request.generated_at_utc,
        "notes": request.notes,
        "raw_response_available": bool(raw_response),
        "structured_response_available": bool(structured_response),
        "structured_response": structured_response,
        "raw_response": response_text,
        "decision_status": decision_status,
        "missing_data": payload_missing,
        "blockers": blockers,
        "forbidden_action_blockers": forbidden_blockers,
        "review_queue_rows": [],
        "expected_gem_output_schema": build_expected_gem_output_schema(),
        "contract": build_capture_contract(),
        "safety_markers": list(SAFETY_MARKERS),
        "human_review_only": True,
        "no_order_no_sizing": True,
        "no_auto_apply_gem_response": True,
    }
    capture["review_queue_rows"] = build_review_queue_rows(capture)
    return capture


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_queue_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "queue_id",
        "priority",
        "review_status",
        "item_type",
        "item_value",
        "required_action",
        "human_review_only",
        "no_order_no_sizing",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def _report_markdown(capture: Mapping[str, Any], output_dir: str) -> str:
    return "\n".join(
        [
            "# P119 GEM Response Capture Review Queue Report",
            "",
            f"- status: {capture['status']}",
            f"- version: {capture['version']}",
            f"- output_dir: {output_dir}",
            f"- response_run_id: {capture['response_run_id']}",
            f"- source_prompt_run_id: {capture['source_prompt_run_id']}",
            f"- missing_data_count: {len(capture['missing_data'])}",
            f"- blocker_count: {len(capture['blockers'])}",
            f"- queue_rows: {len(capture['review_queue_rows'])}",
            "- safety: HUMAN_REVIEW_ONLY / NO_AUTO_APPLY_GEM_RESPONSE / NO_BROKER / NO_ORDER / NO_SIZING",
            "",
            "## Next",
            "",
            "P120_PROMPT_GEM_RESPONSE_TO_DECISION_JOURNAL_BRIDGE_LOCAL_ONLY",
            "",
        ]
    )


def write_response_review_pack(request: GemResponseCaptureRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    capture = build_response_capture(request)

    raw_path = out / "P119_GEM_RESPONSE_RAW.md"
    capture_path = out / "P119_RESPONSE_CAPTURE.json"
    queue_path = out / "P119_REVIEW_QUEUE.csv"
    contract_path = out / "P119_CAPTURE_CONTRACT.json"
    schema_path = out / "P119_EXPECTED_GEM_OUTPUT_SCHEMA.json"
    report_path = out / "P119_REVIEW_REPORT.md"

    raw_path.write_text(capture["raw_response"].rstrip() + "\n", encoding="utf-8")
    _write_json(capture_path, capture)
    _write_queue_csv(queue_path, capture["review_queue_rows"])
    _write_json(contract_path, build_capture_contract())
    _write_json(schema_path, build_expected_gem_output_schema())
    report_path.write_text(_report_markdown(capture, str(out)), encoding="utf-8")

    return {
        "status": "EXPORTED",
        "step": "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
        "output_dir": str(out),
        "decision_status": capture["decision_status"],
        "missing_data_count": len(capture["missing_data"]),
        "blocker_count": len(capture["blockers"]),
        "queue_rows": len(capture["review_queue_rows"]),
        "files": [
            str(raw_path),
            str(capture_path),
            str(queue_path),
            str(contract_path),
            str(schema_path),
            str(report_path),
        ],
        "safety_markers": list(SAFETY_MARKERS),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_response_review_queue",
        description="Capture a GEM response and create a local human review queue.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--raw-response")
    parser.add_argument("--response-text-file")
    parser.add_argument("--response-json-file")
    parser.add_argument("--source-prompt-run-id")
    parser.add_argument("--response-run-id", default="GEM-RESPONSE-CAPTURE")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_response_review_pack(
        GemResponseCaptureRequest(
            output_dir=args.output_dir,
            raw_response=args.raw_response,
            response_text_file=args.response_text_file,
            response_json_file=args.response_json_file,
            source_prompt_run_id=args.source_prompt_run_id,
            response_run_id=args.response_run_id,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["decision_status"])
    print(result["queue_rows"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
