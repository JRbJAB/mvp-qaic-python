from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

OPERATOR_REVIEW_PACK_VERSION = "mvp_qaic.operator_review_pack.v1"

OPERATOR_REVIEW_PACK_SAFETY_MARKERS: tuple[str, ...] = (
    "LOCAL_OPERATOR_REVIEW_ONLY",
    "HUMAN_REVIEW_ONLY",
    "NO_GOOGLE_LIVE_WRITE",
    "NO_SHEET_WRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_SECRET",
    "EXPLICIT_OUTPUT_DIR_REQUIRED_FOR_WRITE",
)


@dataclass(frozen=True)
class OperatorReviewPack:
    review_pack_version: str
    run_id: str
    generated_at: str
    status: str
    asset: str
    decision_status: str
    human_decision_only: bool
    no_order_no_sizing: bool
    current_price: float | None
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    required_human_actions: tuple[str, ...] = field(default_factory=tuple)
    pipeline_summary: Mapping[str, Any] = field(default_factory=dict)
    runtime_result: Mapping[str, Any] = field(default_factory=dict)
    journal_entry: Mapping[str, Any] = field(default_factory=dict)
    safety_markers: tuple[str, ...] = OPERATOR_REVIEW_PACK_SAFETY_MARKERS


@dataclass(frozen=True)
class OperatorReviewWriteResult:
    review_pack_version: str
    wrote_files: bool
    output_dir: str
    files: tuple[str, ...]
    sha256_by_file: Mapping[str, str]
    bytes_written: int
    file_count: int
    safety_markers: tuple[str, ...] = OPERATOR_REVIEW_PACK_SAFETY_MARKERS


def _now_utc_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _as_tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return tuple(str(item) for item in value if str(item).strip())
    return (str(value),)


def _as_bool(value: object, *, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _coerce_price(value: object) -> float | None:
    if value is None:
        return None
    try:
        price = float(value)
    except (TypeError, ValueError):
        return None
    if price <= 0:
        return None
    return price


def _unique(values: Sequence[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return tuple(ordered)


def _human_actions(
    decision_status: str, blockers: Sequence[str], missing_data: Sequence[str]
) -> tuple[str, ...]:
    actions: list[str] = ["Review the decision manually before any action."]

    if decision_status == "BLOCKED":
        actions.append("Do not execute: blocker present.")
    if missing_data:
        actions.append("Complete missing data before re-review.")
    if "FORBIDDEN_AUTO_ORDER_REQUEST" in blockers:
        actions.append("Remove any automatic order request.")
    if "FORBIDDEN_SIZING_REQUEST" in blockers:
        actions.append("Remove any sizing request.")
    if "NETWORK_DISABLED_BY_DEFAULT" in blockers:
        actions.append("Provider network remained disabled by default.")

    actions.append("Keep broker/order/sizing actions disabled.")
    return _unique(actions)


def build_operator_review_pack(
    pipeline_result: Mapping[str, Any],
    *,
    generated_at: str | None = None,
) -> OperatorReviewPack:
    if not isinstance(pipeline_result, Mapping):
        raise TypeError("pipeline_result must be a mapping")

    market_snapshot = pipeline_result.get("market_snapshot")
    if not isinstance(market_snapshot, Mapping):
        market_snapshot = {}

    runtime_result = pipeline_result.get("runtime_result")
    if not isinstance(runtime_result, Mapping):
        runtime_result = {}

    journal_entry = pipeline_result.get("journal_entry")
    if not isinstance(journal_entry, Mapping):
        journal_entry = {}

    run_id = str(pipeline_result.get("run_id") or journal_entry.get("run_id") or "").strip()
    asset = (
        str(
            pipeline_result.get("asset")
            or journal_entry.get("asset")
            or market_snapshot.get("asset")
            or ""
        )
        .strip()
        .upper()
    )
    decision_status = str(
        runtime_result.get("decision_status")
        or journal_entry.get("decision_status")
        or pipeline_result.get("status")
        or "REVIEW_REQUIRED"
    ).strip()

    missing_data = _unique(
        list(_as_tuple(pipeline_result.get("missing_data")))
        + list(_as_tuple(runtime_result.get("missing_data")))
        + list(_as_tuple(journal_entry.get("missing_data")))
    )
    blockers = _unique(
        list(_as_tuple(pipeline_result.get("blockers")))
        + list(_as_tuple(runtime_result.get("blockers")))
        + list(_as_tuple(journal_entry.get("blockers")))
    )

    current_price = _coerce_price(
        market_snapshot.get("current_price")
        or pipeline_result.get("current_price")
        or runtime_result.get("current_price")
    )
    human_decision_only = _as_bool(
        runtime_result.get("human_decision_only")
        if "human_decision_only" in runtime_result
        else journal_entry.get("human_decision_only"),
        default=True,
    )
    no_order_no_sizing = _as_bool(
        runtime_result.get("no_order_no_sizing")
        if "no_order_no_sizing" in runtime_result
        else journal_entry.get("no_order_no_sizing"),
        default=True,
    )

    status = "REVIEW_REQUIRED"
    if decision_status == "BLOCKED" or "FORBIDDEN_AUTO_ORDER_REQUEST" in blockers:
        status = "BLOCKED"

    return OperatorReviewPack(
        review_pack_version=OPERATOR_REVIEW_PACK_VERSION,
        run_id=run_id,
        generated_at=generated_at or _now_utc_iso(),
        status=status,
        asset=asset,
        decision_status=decision_status,
        human_decision_only=human_decision_only,
        no_order_no_sizing=no_order_no_sizing,
        current_price=current_price,
        missing_data=missing_data,
        blockers=blockers,
        required_human_actions=_human_actions(decision_status, blockers, missing_data),
        pipeline_summary={
            "pipeline_version": pipeline_result.get("pipeline_version", ""),
            "pipeline_status": pipeline_result.get("status", ""),
            "network_called": bool(pipeline_result.get("network_called", False)),
            "journal_written": bool(pipeline_result.get("journal_written", False)),
            "broker_called": bool(pipeline_result.get("broker_called", False)),
            "order_created": bool(pipeline_result.get("order_created", False)),
            "sizing_created": bool(pipeline_result.get("sizing_created", False)),
        },
        runtime_result=dict(runtime_result),
        journal_entry=dict(journal_entry),
    )


def operator_review_pack_to_dict(pack: OperatorReviewPack) -> dict[str, object]:
    return {
        "review_pack_version": pack.review_pack_version,
        "run_id": pack.run_id,
        "generated_at": pack.generated_at,
        "status": pack.status,
        "asset": pack.asset,
        "decision_status": pack.decision_status,
        "human_decision_only": pack.human_decision_only,
        "no_order_no_sizing": pack.no_order_no_sizing,
        "current_price": pack.current_price,
        "missing_data": list(pack.missing_data),
        "blockers": list(pack.blockers),
        "required_human_actions": list(pack.required_human_actions),
        "pipeline_summary": dict(pack.pipeline_summary),
        "runtime_result": dict(pack.runtime_result),
        "journal_entry": dict(pack.journal_entry),
        "safety_markers": list(pack.safety_markers),
    }


def render_operator_review_markdown(pack: OperatorReviewPack) -> str:
    payload = operator_review_pack_to_dict(pack)

    lines = [
        "# MVP QAIC - Operator Review Pack",
        "",
        f"- review_pack_version: {pack.review_pack_version}",
        f"- run_id: {pack.run_id}",
        f"- generated_at: {pack.generated_at}",
        f"- status: {pack.status}",
        f"- asset: {pack.asset}",
        f"- decision_status: {pack.decision_status}",
        f"- current_price: {pack.current_price}",
        f"- human_decision_only: {pack.human_decision_only}",
        f"- no_order_no_sizing: {pack.no_order_no_sizing}",
        "",
        "## Required human actions",
    ]
    lines.extend(f"- {action}" for action in pack.required_human_actions)
    lines.extend(
        [
            "",
            "## Missing data",
            *(f"- {item}" for item in pack.missing_data),
            "",
            "## Blockers",
            *(f"- {item}" for item in pack.blockers),
            "",
            "## Safety markers",
            *(f"- {marker}" for marker in pack.safety_markers),
            "",
            "## Machine-readable payload",
            "```json",
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def _json_dumps(payload: Mapping[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_operator_review_pack(
    pack: OperatorReviewPack,
    *,
    output_dir: str | Path,
) -> OperatorReviewWriteResult:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    pack_payload = operator_review_pack_to_dict(pack)
    markdown = render_operator_review_markdown(pack)
    json_payload = _json_dumps(pack_payload)

    manifest = {
        "review_pack_version": OPERATOR_REVIEW_PACK_VERSION,
        "run_id": pack.run_id,
        "file_count": 2,
        "files": ["operator_review.md", "operator_review.json"],
        "safety_markers": list(OPERATOR_REVIEW_PACK_SAFETY_MARKERS),
    }
    manifest_payload = _json_dumps(manifest)

    outputs = {
        "operator_review.md": markdown,
        "operator_review.json": json_payload,
        "operator_review_manifest.json": manifest_payload,
    }

    sha_by_file: dict[str, str] = {}
    bytes_written = 0
    for file_name, text in outputs.items():
        path = target_dir / file_name
        path.write_text(text, encoding="utf-8")
        sha_by_file[file_name] = _sha256_text(text)
        bytes_written += len(text.encode("utf-8"))

    return OperatorReviewWriteResult(
        review_pack_version=OPERATOR_REVIEW_PACK_VERSION,
        wrote_files=True,
        output_dir=str(target_dir),
        files=tuple(outputs),
        sha256_by_file=sha_by_file,
        bytes_written=bytes_written,
        file_count=len(outputs),
    )


def write_result_to_dict(result: OperatorReviewWriteResult) -> dict[str, object]:
    return {
        "review_pack_version": result.review_pack_version,
        "wrote_files": result.wrote_files,
        "output_dir": result.output_dir,
        "files": list(result.files),
        "sha256_by_file": dict(result.sha256_by_file),
        "bytes_written": result.bytes_written,
        "file_count": result.file_count,
        "safety_markers": list(result.safety_markers),
    }
