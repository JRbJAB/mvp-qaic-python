"""P157 prompt patch candidate review gate.

Review-only gate for the P156 prompt patch candidate.
No prompt source modification, no apply, no Sheet write, no public deploy.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

P156_READY_STATUS = "P156_PROMPT_PATCH_CANDIDATE_READY_REVIEW_ONLY"
P157_READY_STATUS = "P157_PROMPT_PATCH_CANDIDATE_REVIEW_READY_ONLY"
P157_BLOCKED_STATUS = "P157_STOP_PATCH_CANDIDATE_REVIEW_BLOCKED"
PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"

FORBIDDEN_EXACT_MARKERS = (
    "apply_allowed=true",
    "apply_now=yes",
    "prompt_source_modified=true",
    "google_sheets_write=true",
    "public_deploy=true",
    "no_auto_apply_gem_response=false",
)

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

REQUIRED_SAFE_HINTS = (
    "sans apply automatique",
    "review-only",
    "human review",
    "no apply",
    "apply_allowed=false",
)


@dataclass(frozen=True)
class P156Source:
    source_dir: str
    summary_path: str
    candidate_path: str
    summary: dict[str, Any]
    candidate_text: str


@dataclass(frozen=True)
class P157Summary:
    status: str
    prompt_source_id: str
    source_p156_status: str
    source_p156_dir: str
    patch_candidate_found: bool
    patch_candidate_created: bool
    patch_candidate_text_length: int
    patch_candidate_line_count: int
    patch_safe_for_review: bool
    unsafe_marker_count: int
    unsafe_markers: list[str]
    required_safe_hint_count: int
    apply_allowed: bool
    apply_now_yes_count: int
    prompt_source_modified: bool
    google_sheets_write: bool
    public_deploy: bool
    human_review_required: bool
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


def find_latest_p156_candidate_export(repo_root: Path) -> Path:
    exports_root = repo_root / "05_EXPORTS"
    candidates: list[Path] = []
    if exports_root.exists():
        for directory in exports_root.glob(
            "P156_PROMPT_PATCH_CANDIDATE_OR_STOP_AFTER_HUMAN_REVIEW_*"
        ):
            if directory.is_dir() and (directory / "P156_PROMPT_PATCH_CANDIDATE.md").exists():
                candidates.append(directory)
    if not candidates:
        raise FileNotFoundError("No P156 prompt patch candidate export found.")
    return sorted(candidates, key=lambda item: item.stat().st_mtime, reverse=True)[0]


def load_p156_source(repo_root: Path, source_dir: Path | None = None) -> P156Source:
    resolved_source_dir = source_dir or find_latest_p156_candidate_export(repo_root)
    summary_path = resolved_source_dir / "P156_SUMMARY.json"
    candidate_path = resolved_source_dir / "P156_PROMPT_PATCH_CANDIDATE.md"
    if not summary_path.exists():
        raise FileNotFoundError(f"P156 summary not found: {summary_path}")
    if not candidate_path.exists():
        raise FileNotFoundError(f"P156 candidate not found: {candidate_path}")
    return P156Source(
        source_dir=str(resolved_source_dir),
        summary_path=str(summary_path),
        candidate_path=str(candidate_path),
        summary=read_json(summary_path),
        candidate_text=candidate_path.read_text(encoding="utf-8-sig"),
    )


def detect_unsafe_markers(candidate_text: str, summary: dict[str, Any]) -> list[str]:
    lowered = candidate_text.lower()
    unsafe: list[str] = []
    for marker in FORBIDDEN_EXACT_MARKERS:
        if marker in lowered:
            unsafe.append(marker)
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lowered:
            unsafe.append(phrase)
    if _bool(_ci_get(summary, "APPLY_ALLOWED")):
        unsafe.append("summary.APPLY_ALLOWED=true")
    if _int(_ci_get(summary, "APPLY_NOW_YES_COUNT")) != 0:
        unsafe.append("summary.APPLY_NOW_YES_COUNT!=0")
    if _bool(_ci_get(summary, "PROMPT_SOURCE_MODIFIED")):
        unsafe.append("summary.PROMPT_SOURCE_MODIFIED=true")
    if _bool(_ci_get(summary, "GOOGLE_SHEETS_WRITE")):
        unsafe.append("summary.GOOGLE_SHEETS_WRITE=true")
    if _bool(_ci_get(summary, "PUBLIC_DEPLOY")):
        unsafe.append("summary.PUBLIC_DEPLOY=true")
    return sorted(set(unsafe))


def count_safe_hints(candidate_text: str) -> int:
    lowered = candidate_text.lower()
    return sum(1 for hint in REQUIRED_SAFE_HINTS if hint in lowered)


def review_patch_candidate(repo_root: Path, source_dir: Path | None = None) -> P157Summary:
    source = load_p156_source(repo_root=repo_root, source_dir=source_dir)
    summary = source.summary
    source_status = str(_ci_get(summary, "P156_STATUS", ""))
    prompt_source_id = str(_ci_get(summary, "PROMPT_SOURCE_ID", PROMPT_SOURCE_ID))
    patch_candidate_created = _bool(_ci_get(summary, "PATCH_CANDIDATE_CREATED"))
    pending_count = _int(_ci_get(summary, "PENDING_HUMAN_REVIEW_COUNT"))
    accepted_count = _int(_ci_get(summary, "ACCEPTED_FOR_PATCH_CANDIDATE_COUNT"))
    candidate_text = source.candidate_text.strip()
    unsafe_markers = detect_unsafe_markers(candidate_text, summary)
    safe_hint_count = count_safe_hints(candidate_text)
    blockers: list[str] = []

    if source_status != P156_READY_STATUS:
        blockers.append("P156_STATUS_NOT_READY")
    if prompt_source_id != PROMPT_SOURCE_ID:
        blockers.append("PROMPT_SOURCE_ID_MISMATCH")
    if not patch_candidate_created:
        blockers.append("PATCH_CANDIDATE_NOT_CREATED")
    if pending_count != 0:
        blockers.append("PENDING_HUMAN_REVIEW_NOT_ZERO")
    if accepted_count < 1:
        blockers.append("NO_ACCEPTED_PATCH_CANDIDATE")
    if not candidate_text:
        blockers.append("PATCH_CANDIDATE_EMPTY")
    if unsafe_markers:
        blockers.append("UNSAFE_PATCH_CANDIDATE_MARKERS")

    line_count = 0 if not candidate_text else candidate_text.count("\n") + 1
    patch_safe_for_review = not blockers
    status = P157_READY_STATUS if patch_safe_for_review else P157_BLOCKED_STATUS
    next_step = (
        "P158_MANUAL_PROMPT_PATCH_APPLY_OR_STOP"
        if patch_safe_for_review
        else "REVIEW_P156_PATCH_CANDIDATE_THEN_RETRY_P157"
    )
    output_dir = (
        repo_root
        / "05_EXPORTS"
        / f"P157_PROMPT_PATCH_CANDIDATE_REVIEW_OR_APPLY_GATE_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    )

    return P157Summary(
        status=status,
        prompt_source_id=prompt_source_id,
        source_p156_status=source_status,
        source_p156_dir=source.source_dir,
        patch_candidate_found=bool(candidate_text),
        patch_candidate_created=patch_candidate_created,
        patch_candidate_text_length=len(candidate_text),
        patch_candidate_line_count=line_count,
        patch_safe_for_review=patch_safe_for_review,
        unsafe_marker_count=len(unsafe_markers),
        unsafe_markers=unsafe_markers,
        required_safe_hint_count=safe_hint_count,
        apply_allowed=False,
        apply_now_yes_count=0,
        prompt_source_modified=False,
        google_sheets_write=False,
        public_deploy=False,
        human_review_required=True,
        blocker_count=len(blockers),
        blockers=blockers,
        output_dir=str(output_dir),
        next=next_step,
        generated_at_utc=utc_now_iso(),
    )


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_report_csv(path: Path, summary: P157Summary) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "status",
                "patch_candidate_found",
                "patch_safe_for_review",
                "unsafe_marker_count",
                "blocker_count",
                "apply_allowed",
                "prompt_source_modified",
                "next",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "status": summary.status,
                "patch_candidate_found": str(summary.patch_candidate_found),
                "patch_safe_for_review": str(summary.patch_safe_for_review),
                "unsafe_marker_count": str(summary.unsafe_marker_count),
                "blocker_count": str(summary.blocker_count),
                "apply_allowed": str(summary.apply_allowed),
                "prompt_source_modified": str(summary.prompt_source_modified),
                "next": summary.next,
            }
        )


def build_review_markdown(summary: P157Summary) -> str:
    verdict = "READY FOR MANUAL APPLY GATE" if summary.patch_safe_for_review else "BLOCKED"
    blockers = "\n".join(f"- {item}" for item in summary.blockers) or "- none"
    unsafe = "\n".join(f"- {item}" for item in summary.unsafe_markers) or "- none"
    return f"""# P157 Prompt Patch Candidate Review Gate

## Verdict

{verdict}

## Source

- prompt_source_id: `{summary.prompt_source_id}`
- source_p156_status: `{summary.source_p156_status}`
- source_p156_dir: `{summary.source_p156_dir}`

## Review result

- patch_candidate_found: `{summary.patch_candidate_found}`
- patch_candidate_created: `{summary.patch_candidate_created}`
- patch_safe_for_review: `{summary.patch_safe_for_review}`
- patch_candidate_line_count: `{summary.patch_candidate_line_count}`
- patch_candidate_text_length: `{summary.patch_candidate_text_length}`
- required_safe_hint_count: `{summary.required_safe_hint_count}`

## Safety gates

- apply_allowed: `{summary.apply_allowed}`
- apply_now_yes_count: `{summary.apply_now_yes_count}`
- prompt_source_modified: `{summary.prompt_source_modified}`
- google_sheets_write: `{summary.google_sheets_write}`
- public_deploy: `{summary.public_deploy}`
- human_review_required: `{summary.human_review_required}`

## Unsafe markers

{unsafe}

## Blockers

{blockers}

## Next

`{summary.next}`
"""


def build_handoff(summary: P157Summary) -> str:
    return f"""# P157 handoff

P157 reviewed the P156 prompt patch candidate without applying it.

Status: `{summary.status}`

Next: `{summary.next}`

Hard rule: P158 may prepare a manual apply gate, but it must not silently modify the prompt source.
"""


def build_and_write_export(repo_root: Path, source_dir: Path | None = None) -> P157Summary:
    summary = review_patch_candidate(repo_root=repo_root, source_dir=source_dir)
    output_dir = Path(summary.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source = load_p156_source(repo_root=repo_root, source_dir=source_dir)

    _write_json(output_dir / "P157_SUMMARY.json", asdict(summary))
    _write_json(output_dir / "P157_PROMPT_PATCH_CANDIDATE_REVIEW_REPORT.json", asdict(summary))
    _write_report_csv(output_dir / "P157_PROMPT_PATCH_CANDIDATE_REVIEW_REPORT.csv", summary)
    (output_dir / "P157_REVIEW_GATE_DECISION.md").write_text(
        build_review_markdown(summary), encoding="utf-8"
    )
    (output_dir / "P157_PROMPT_PATCH_CANDIDATE_READBACK.md").write_text(
        source.candidate_text, encoding="utf-8"
    )
    (output_dir / "P157_HANDOFF.md").write_text(build_handoff(summary), encoding="utf-8")
    return summary


def main(argv: list[str] | None = None) -> int:
    del argv
    repo_root = Path.cwd()
    summary = build_and_write_export(repo_root=repo_root)
    print(summary.status)
    print(f"prompt_source_id={summary.prompt_source_id}")
    print(f"source_p156_status={summary.source_p156_status}")
    print(f"patch_candidate_found={str(summary.patch_candidate_found).lower()}")
    print(f"patch_candidate_created={str(summary.patch_candidate_created).lower()}")
    print(f"patch_safe_for_review={str(summary.patch_safe_for_review).lower()}")
    print(f"unsafe_marker_count={summary.unsafe_marker_count}")
    print(f"blocker_count={summary.blocker_count}")
    print(f"apply_allowed={str(summary.apply_allowed).lower()}")
    print(f"prompt_source_modified={str(summary.prompt_source_modified).lower()}")
    print(f"output_dir={summary.output_dir}")
    print(f"next={summary.next}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
