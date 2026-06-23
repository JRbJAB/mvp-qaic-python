"""P158 manual prompt patch apply or stop gate.

Creates a manual apply authorization pack from the reviewed P157 patch candidate.
This module deliberately does not modify the prompt source and does not apply patches.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

P157_READY_STATUS = "P157_PROMPT_PATCH_CANDIDATE_REVIEW_READY_ONLY"
P158_WAITING_STATUS = "P158_STOP_WAITING_MANUAL_APPLY_AUTHORIZATION"
P158_BLOCKED_STATUS = "P158_STOP_PATCH_CANDIDATE_NOT_READY_FOR_MANUAL_APPLY"
PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"

FORBIDDEN_PHRASES = (
    "buy now",
    "sell now",
    "place order",
    "post order",
    "execute order",
    "execute trade",
    "send order",
    "market order",
    "limit order",
    "auto apply enabled",
    "auto-apply enabled",
    "automatic apply",
    "auto sizing",
    "auto-sizing enabled",
    "broker execution",
)


@dataclass(frozen=True)
class P157Source:
    source_dir: str
    summary_path: str
    candidate_readback_path: str
    summary: dict[str, Any]
    candidate_text: str


@dataclass(frozen=True)
class P158Summary:
    status: str
    prompt_source_id: str
    source_p157_status: str
    source_p157_dir: str
    patch_candidate_found: bool
    patch_candidate_created: bool
    patch_safe_for_review: bool
    candidate_ready_for_manual_apply: bool
    manual_apply_authorized: bool
    source_patch_applied: bool
    apply_allowed: bool
    apply_now_yes_count: int
    prompt_source_modified: bool
    google_sheets_write: bool
    live_google_sheets_read: bool
    public_deploy: bool
    no_apps_script_execution: bool
    no_clasp_push: bool
    no_broker: bool
    no_order: bool
    no_sizing: bool
    no_auto_apply_gem_response: bool
    human_review_required: bool
    unsafe_marker_count: int
    unsafe_markers: list[str]
    blocker_count: int
    blockers: list[str]
    output_dir: str
    next: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _int(value: Any) -> int:
    if value is None or value == "":
        return 0
    return int(str(value).strip())


def _ci_get(mapping: dict[str, Any], key: str, default: Any = None) -> Any:
    if key in mapping:
        return mapping[key]
    target = key.lower()
    for existing_key, value in mapping.items():
        if existing_key.lower() == target:
            return value
    return default


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def find_latest_p157_export(repo_root: Path) -> Path:
    exports_root = repo_root / "05_EXPORTS"
    candidates: list[Path] = []
    if exports_root.exists():
        for directory in exports_root.glob("P157_PROMPT_PATCH_CANDIDATE_REVIEW_OR_APPLY_GATE_*"):
            if directory.is_dir() and (directory / "P157_SUMMARY.json").exists():
                candidates.append(directory)
    if not candidates:
        raise FileNotFoundError("No P157 patch candidate review export found.")
    return sorted(candidates, key=lambda item: item.stat().st_mtime, reverse=True)[0]


def load_p157_source(repo_root: Path, source_dir: Path | None = None) -> P157Source:
    resolved_source_dir = source_dir or find_latest_p157_export(repo_root)
    summary_path = resolved_source_dir / "P157_SUMMARY.json"
    candidate_readback_path = resolved_source_dir / "P157_PROMPT_PATCH_CANDIDATE_READBACK.md"
    if not summary_path.exists():
        raise FileNotFoundError(f"P157 summary not found: {summary_path}")
    if not candidate_readback_path.exists():
        raise FileNotFoundError(f"P157 candidate readback not found: {candidate_readback_path}")
    return P157Source(
        source_dir=str(resolved_source_dir),
        summary_path=str(summary_path),
        candidate_readback_path=str(candidate_readback_path),
        summary=read_json(summary_path),
        candidate_text=candidate_readback_path.read_text(encoding="utf-8-sig"),
    )


def detect_unsafe_markers(candidate_text: str, summary: dict[str, Any]) -> list[str]:
    lowered = candidate_text.lower()
    unsafe: list[str] = []
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lowered:
            unsafe.append(phrase)
    if _bool(_ci_get(summary, "APPLY_ALLOWED")):
        unsafe.append("summary.APPLY_ALLOWED=true")
    if _bool(_ci_get(summary, "PROMPT_SOURCE_MODIFIED")):
        unsafe.append("summary.PROMPT_SOURCE_MODIFIED=true")
    if _bool(_ci_get(summary, "GOOGLE_SHEETS_WRITE")):
        unsafe.append("summary.GOOGLE_SHEETS_WRITE=true")
    if _bool(_ci_get(summary, "PUBLIC_DEPLOY")):
        unsafe.append("summary.PUBLIC_DEPLOY=true")
    if _int(_ci_get(summary, "UNSAFE_MARKER_COUNT")) != 0:
        unsafe.append("summary.UNSAFE_MARKER_COUNT!=0")
    return sorted(set(unsafe))


def review_manual_apply_gate(repo_root: Path, source_dir: Path | None = None) -> P158Summary:
    source = load_p157_source(repo_root=repo_root, source_dir=source_dir)
    summary = source.summary
    source_status = str(_ci_get(summary, "P157_STATUS", _ci_get(summary, "status", "")))
    prompt_source_id = str(_ci_get(summary, "PROMPT_SOURCE_ID", PROMPT_SOURCE_ID))
    patch_candidate_found = _bool(_ci_get(summary, "PATCH_CANDIDATE_FOUND"))
    patch_candidate_created = _bool(_ci_get(summary, "PATCH_CANDIDATE_CREATED"))
    patch_safe_for_review = _bool(_ci_get(summary, "PATCH_SAFE_FOR_REVIEW"))
    source_blocker_count = _int(_ci_get(summary, "BLOCKER_COUNT"))
    source_apply_allowed = _bool(_ci_get(summary, "APPLY_ALLOWED"))
    source_prompt_modified = _bool(_ci_get(summary, "PROMPT_SOURCE_MODIFIED"))
    candidate_text = source.candidate_text.strip()
    unsafe_markers = detect_unsafe_markers(candidate_text, summary)

    blockers: list[str] = []
    if source_status != P157_READY_STATUS:
        blockers.append("P157_STATUS_NOT_READY")
    if prompt_source_id != PROMPT_SOURCE_ID:
        blockers.append("PROMPT_SOURCE_ID_MISMATCH")
    if not patch_candidate_found:
        blockers.append("PATCH_CANDIDATE_NOT_FOUND")
    if not patch_candidate_created:
        blockers.append("PATCH_CANDIDATE_NOT_CREATED")
    if not patch_safe_for_review:
        blockers.append("PATCH_NOT_SAFE_FOR_REVIEW")
    if source_blocker_count != 0:
        blockers.append("P157_BLOCKER_COUNT_NOT_ZERO")
    if source_apply_allowed:
        blockers.append("P157_APPLY_ALLOWED_TRUE")
    if source_prompt_modified:
        blockers.append("P157_PROMPT_SOURCE_MODIFIED_TRUE")
    if not candidate_text:
        blockers.append("PATCH_CANDIDATE_READBACK_EMPTY")
    if unsafe_markers:
        blockers.append("UNSAFE_MARKERS_FOUND")

    candidate_ready = not blockers
    waiting_manual_auth = (
        "WAITING_MANUAL_APPLY_AUTHORIZATION" if candidate_ready else "PATCH_CANDIDATE_NOT_READY"
    )
    all_blockers = list(blockers)
    if candidate_ready:
        all_blockers.append(waiting_manual_auth)

    status = P158_WAITING_STATUS if candidate_ready else P158_BLOCKED_STATUS
    next_step = (
        "AUTHORIZE_P158_MANUAL_APPLY_THEN_RETRY_OR_STOP"
        if candidate_ready
        else "REVIEW_P157_AND_P156_THEN_RETRY_P158"
    )
    output_dir = (
        repo_root
        / "05_EXPORTS"
        / f"P158_MANUAL_PROMPT_PATCH_APPLY_OR_STOP_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    )

    return P158Summary(
        status=status,
        prompt_source_id=prompt_source_id,
        source_p157_status=source_status,
        source_p157_dir=source.source_dir,
        patch_candidate_found=patch_candidate_found,
        patch_candidate_created=patch_candidate_created,
        patch_safe_for_review=patch_safe_for_review,
        candidate_ready_for_manual_apply=candidate_ready,
        manual_apply_authorized=False,
        source_patch_applied=False,
        apply_allowed=False,
        apply_now_yes_count=0,
        prompt_source_modified=False,
        google_sheets_write=False,
        live_google_sheets_read=False,
        public_deploy=False,
        no_apps_script_execution=True,
        no_clasp_push=True,
        no_broker=True,
        no_order=True,
        no_sizing=True,
        no_auto_apply_gem_response=True,
        human_review_required=True,
        unsafe_marker_count=len(unsafe_markers),
        unsafe_markers=unsafe_markers,
        blocker_count=len(all_blockers),
        blockers=all_blockers,
        output_dir=str(output_dir),
        next=next_step,
        generated_at_utc=utc_now_iso(),
    )


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_decision_csv(path: Path, summary: P158Summary) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "decision_id",
                "prompt_source_id",
                "source_p157_status",
                "patch_candidate_found",
                "patch_safe_for_review",
                "candidate_ready_for_manual_apply",
                "human_apply_decision",
                "manual_apply_authorized",
                "apply_now",
                "apply_allowed",
                "source_patch_applied",
                "prompt_source_modified",
                "safety_status",
                "manual_note",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "decision_id": "P158-APPLY-001",
                "prompt_source_id": summary.prompt_source_id,
                "source_p157_status": summary.source_p157_status,
                "patch_candidate_found": summary.patch_candidate_found,
                "patch_safe_for_review": summary.patch_safe_for_review,
                "candidate_ready_for_manual_apply": summary.candidate_ready_for_manual_apply,
                "human_apply_decision": "PENDING_MANUAL_APPLY_AUTHORIZATION",
                "manual_apply_authorized": "false",
                "apply_now": "NO",
                "apply_allowed": "false",
                "source_patch_applied": "false",
                "prompt_source_modified": "false",
                "safety_status": "HUMAN_REVIEW_ONLY_NO_APPLY",
                "manual_note": "Review P157 candidate and explicitly authorize manual source patch only in a later controlled batch.",
            }
        )


def _write_report_csv(path: Path, summary: P158Summary) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for key, value in asdict(summary).items():
            writer.writerow(
                {
                    "metric": key,
                    "value": json.dumps(value, ensure_ascii=False)
                    if isinstance(value, list)
                    else value,
                }
            )


def _write_markdown_files(output_dir: Path, summary: P158Summary, source: P157Source) -> None:
    stop_reason = "Manual apply authorization is required before any prompt source modification."
    (output_dir / "P158_MANUAL_APPLY_GATE.md").write_text(
        "# P158 Manual Prompt Patch Apply Gate\n\n"
        f"- status: `{summary.status}`\n"
        f"- candidate_ready_for_manual_apply: `{summary.candidate_ready_for_manual_apply}`\n"
        f"- manual_apply_authorized: `{summary.manual_apply_authorized}`\n"
        f"- source_patch_applied: `{summary.source_patch_applied}`\n"
        f"- apply_allowed: `{summary.apply_allowed}`\n"
        f"- prompt_source_modified: `{summary.prompt_source_modified}`\n\n"
        f"## Stop reason\n\n{stop_reason}\n",
        encoding="utf-8",
    )
    (output_dir / "P158_PROMPT_PATCH_CANDIDATE_READBACK.md").write_text(
        source.candidate_text, encoding="utf-8"
    )
    (output_dir / "P158_HANDOFF.md").write_text(
        "# P158 Handoff\n\n"
        "P158 did not apply the patch and did not modify the prompt source.\n\n"
        "Next: `AUTHORIZE_P158_MANUAL_APPLY_THEN_RETRY_OR_STOP`.\n\n"
        "Required explicit future decision values:\n"
        "- `AUTHORIZE_MANUAL_APPLY` to allow a later controlled source patch candidate batch.\n"
        "- `STOP_NO_APPLY` to close without source modification.\n",
        encoding="utf-8",
    )


def build_and_write_export(repo_root: Path, source_dir: Path | None = None) -> P158Summary:
    source = load_p157_source(repo_root=repo_root, source_dir=source_dir)
    summary = review_manual_apply_gate(repo_root=repo_root, source_dir=Path(source.source_dir))
    output_dir = Path(summary.output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    _write_json(output_dir / "P158_SUMMARY.json", asdict(summary))
    _write_json(output_dir / "P158_MANUAL_PROMPT_PATCH_APPLY_OR_STOP_REPORT.json", asdict(summary))
    _write_report_csv(output_dir / "P158_MANUAL_PROMPT_PATCH_APPLY_OR_STOP_REPORT.csv", summary)
    _write_decision_csv(output_dir / "P158_MANUAL_APPLY_DECISION.csv", summary)
    _write_markdown_files(output_dir, summary, source)
    return summary


def main(argv: list[str] | None = None) -> int:
    repo_root = Path.cwd()
    if not (repo_root / "pyproject.toml").exists():
        raise SystemExit("Run from repository root.")
    summary = build_and_write_export(repo_root=repo_root)
    print(summary.status)
    print(f"prompt_source_id={summary.prompt_source_id}")
    print(f"source_p157_status={summary.source_p157_status}")
    print(f"patch_candidate_found={str(summary.patch_candidate_found).lower()}")
    print(f"patch_safe_for_review={str(summary.patch_safe_for_review).lower()}")
    print(
        f"candidate_ready_for_manual_apply={str(summary.candidate_ready_for_manual_apply).lower()}"
    )
    print(f"manual_apply_authorized={str(summary.manual_apply_authorized).lower()}")
    print(f"source_patch_applied={str(summary.source_patch_applied).lower()}")
    print(f"apply_allowed={str(summary.apply_allowed).lower()}")
    print(f"prompt_source_modified={str(summary.prompt_source_modified).lower()}")
    print(f"unsafe_marker_count={summary.unsafe_marker_count}")
    print(f"blocker_count={summary.blocker_count}")
    print(f"output_dir={summary.output_dir}")
    print(f"next={summary.next}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
