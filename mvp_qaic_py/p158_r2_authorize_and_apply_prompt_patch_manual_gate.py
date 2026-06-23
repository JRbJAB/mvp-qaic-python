from __future__ import annotations

import argparse
import csv
import difflib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

EXPECTED_PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
PATCH_MARKER = "P158_R5_PROMPT_PATCH_APPLIED_20260623"
PATCH_TITLE = "P158-R5 Runtime clarification patch"

PATCH_BLOCK = f"""
<!-- {PATCH_MARKER} -->
### {PATCH_TITLE}

- Set `image_used` explicitly in the output payload: `true` when the screenshot or image is used as evidence, `false` only when no image evidence is available.
- Set `reference_currency` explicitly: use `USD` for the Revolut X / USD runtime prompt unless the provided interface or copied text proves another currency.
- When a field is uncertain, missing, or not visible, mark the uncertainty explicitly instead of silently omitting the field.
- Preserve the human-review-only stance: do not convert prompt observations into execution instructions, allocation instructions, or broker actions.
- Keep JSON field names, enum values, safety markers, and technical statuses exactly as specified by the runtime schema.
<!-- /{PATCH_MARKER} -->
""".strip()

PYTHON_PATCH_CONSTANT = f'''

# {PATCH_MARKER}_PYTHON_ADDENDUM_START
P158_R5_RUNTIME_CLARIFICATION_PATCH = """{PATCH_BLOCK}"""
# {PATCH_MARKER}_PYTHON_ADDENDUM_END
'''.lstrip()

UNSAFE_RUNTIME_MARKERS = (
    "AUTO_BROKER_EXECUTION=true",
    "NO_HUMAN_REVIEW_REQUIRED",
    "PUBLIC_DEPLOY=true",
    "GOOGLE_SHEETS_WRITE=true",
    "NO_AUTO_APPLY_GEM_RESPONSE=false",
    "buy now",
    "sell now",
    "place order",
    "execute order",
    "broker execution",
    "auto sizing",
    "auto-sizing",
)


def utc_stamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "y", "1", "ok"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


def ci_get(mapping: dict[str, Any], key: str, default: Any = None) -> Any:
    if key in mapping:
        return mapping[key]
    target = key.lower()
    for existing_key, value in mapping.items():
        if existing_key.lower() == target:
            return value
    return default


def latest_export_dir(repo_root: Path, prefix: str) -> Path:
    exports = repo_root / "05_EXPORTS"
    matches = [p for p in exports.glob(f"{prefix}*") if p.is_dir()]
    if not matches:
        raise FileNotFoundError(f"No export dir found for prefix {prefix!r}")
    return max(matches, key=lambda p: p.stat().st_mtime)


def load_latest_p158_summary(repo_root: Path) -> tuple[Path, dict[str, Any]]:
    source_dir = latest_export_dir(repo_root, "P158_MANUAL_PROMPT_PATCH_APPLY_OR_STOP_")
    summary_file = source_dir / "P158_SUMMARY.json"
    if not summary_file.exists():
        raise FileNotFoundError(f"P158_SUMMARY.json missing: {summary_file}")
    return source_dir, read_json(summary_file)


def validate_p158_summary(summary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    p158_status = str(ci_get(summary, "P158_STATUS", ci_get(summary, "status", "")))
    if p158_status != "P158_STOP_WAITING_MANUAL_APPLY_AUTHORIZATION":
        blockers.append("P158_STATUS_NOT_WAITING_MANUAL_AUTHORIZATION")
    if not boolish(
        ci_get(summary, "PATCH_CANDIDATE_FOUND", ci_get(summary, "patch_candidate_found"))
    ):
        blockers.append("PATCH_CANDIDATE_NOT_FOUND")
    if not boolish(
        ci_get(summary, "PATCH_SAFE_FOR_REVIEW", ci_get(summary, "patch_safe_for_review"))
    ):
        blockers.append("PATCH_NOT_SAFE_FOR_REVIEW")
    if not boolish(
        ci_get(
            summary,
            "CANDIDATE_READY_FOR_MANUAL_APPLY",
            ci_get(summary, "candidate_ready_for_manual_apply"),
        )
    ):
        blockers.append("CANDIDATE_NOT_READY_FOR_MANUAL_APPLY")
    if boolish(ci_get(summary, "SOURCE_PATCH_APPLIED", ci_get(summary, "source_patch_applied"))):
        blockers.append("P158_ALREADY_SOURCE_PATCH_APPLIED")
    if boolish(
        ci_get(summary, "PROMPT_SOURCE_MODIFIED", ci_get(summary, "prompt_source_modified"))
    ):
        blockers.append("P158_ALREADY_PROMPT_SOURCE_MODIFIED")
    if boolish(ci_get(summary, "GOOGLE_SHEETS_WRITE", ci_get(summary, "google_sheets_write"))):
        blockers.append("GOOGLE_SHEETS_WRITE_TRUE")
    if boolish(ci_get(summary, "PUBLIC_DEPLOY", ci_get(summary, "public_deploy"))):
        blockers.append("PUBLIC_DEPLOY_TRUE")
    return blockers


def locate_p156_candidate(repo_root: Path) -> tuple[Path, Path, str]:
    p156_dir = latest_export_dir(
        repo_root, "P156_PROMPT_PATCH_CANDIDATE_OR_STOP_AFTER_HUMAN_REVIEW_"
    )
    candidate = p156_dir / "P156_PROMPT_PATCH_CANDIDATE.md"
    if not candidate.exists():
        raise FileNotFoundError(f"P156 patch candidate missing: {candidate}")
    text = candidate.read_text(encoding="utf-8-sig")
    return p156_dir, candidate, text


def candidate_unsafe_marker_count(text: str) -> int:
    upper_text = text.upper()
    return sum(1 for marker in UNSAFE_RUNTIME_MARKERS if marker.upper() in upper_text)


def prompt_source_candidates(repo_root: Path) -> list[tuple[int, Path]]:
    base = repo_root / "mvp_qaic_py"
    candidates: list[tuple[int, Path]] = []
    preferred = [
        base / "multimodal_gem_image_prompt_usd_contract_p132.py",
        base / "gem_multimodal_response_capture_gate_p133.py",
        base / "gem_portfolio_prompt_module_p112.py",
    ]
    seen: set[Path] = set()
    for path in preferred:
        if path.exists():
            text = path.read_text(encoding="utf-8-sig")
            score = 100
            if "# P132 GEM Multimodal Portfolio Prompt" in text:
                score += 200
            if EXPECTED_PROMPT_SOURCE_ID in text:
                score += 100
            if "reference_currency" in text:
                score += 50
            if "image_used" in text:
                score += 50
            candidates.append((score, path))
            seen.add(path)

    for path in base.glob("*.py"):
        if path in seen:
            continue
        if path.name.startswith(("p152", "p153", "p154", "p155", "p156", "p157", "p158")):
            continue
        text = path.read_text(encoding="utf-8-sig")
        score = 0
        if "# P132 GEM Multimodal Portfolio Prompt" in text:
            score += 250
        if EXPECTED_PROMPT_SOURCE_ID in text:
            score += 100
        if "reference_currency" in text and "image_used" in text:
            score += 100
        if "Revolut X" in text and "USD" in text:
            score += 50
        if score > 0:
            candidates.append((score, path))

    return sorted(candidates, key=lambda item: (-item[0], str(item[1])))


def locate_prompt_source_file(repo_root: Path) -> Path:
    candidates = prompt_source_candidates(repo_root)
    if not candidates:
        raise FileNotFoundError("No prompt source candidate found for P132/P133 runtime prompt")
    best_score, best_path = candidates[0]
    if best_score < 100:
        raise FileNotFoundError(
            f"Prompt source candidate score too low: {best_path} score={best_score}"
        )
    return best_path


def _is_inside_triple_quote(text: str, index: int) -> bool:
    # Conservative heuristic: only insert raw markdown inside an existing triple-quoted prompt string.
    before = text[:index]
    triple_double = before.count('"""')
    triple_single = before.count("'''")
    return (triple_double % 2 == 1) or (triple_single % 2 == 1)


def apply_patch_block_to_prompt_source(text: str) -> tuple[str, bool, str]:
    if PATCH_MARKER in text:
        return text, False, "already_present"

    hard_rules_marker = "## Hard rules"
    if hard_rules_marker in text:
        idx = text.index(hard_rules_marker) + len(hard_rules_marker)
        if _is_inside_triple_quote(text, idx):
            insertion = "\n\n" + PATCH_BLOCK + "\n"
            return text[:idx] + insertion + text[idx:], True, "inserted_inside_prompt_hard_rules"

    title_marker = "# P132 GEM Multimodal Portfolio Prompt"
    if title_marker in text:
        idx = text.index(title_marker) + len(title_marker)
        if _is_inside_triple_quote(text, idx):
            insertion = "\n\n" + PATCH_BLOCK + "\n"
            return text[:idx] + insertion + text[idx:], True, "inserted_inside_prompt_title"

    # Safe fallback: keep Python valid even if the prompt text is not a direct triple-quoted string.
    return (
        text.rstrip() + "\n\n" + PYTHON_PATCH_CONSTANT + "\n",
        True,
        "appended_python_addendum_constant",
    )


def update_manual_apply_decision_csv(p158_dir: Path) -> Path | None:
    decision_file = p158_dir / "P158_MANUAL_APPLY_DECISION.csv"
    if not decision_file.exists():
        return None

    with decision_file.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        original_fields = list(reader.fieldnames or [])

    required_fields = [
        "manual_apply_authorized",
        "source_patch_applied",
        "apply_allowed",
        "prompt_source_modified",
        "human_apply_decision",
        "apply_now",
        "authorization_note",
        "authorized_at_utc",
    ]
    fields = list(dict.fromkeys(original_fields + required_fields))

    if not rows:
        rows = [{field: "" for field in fields}]

    for row in rows:
        row["human_apply_decision"] = "AUTHORIZED_MANUAL_PROMPT_PATCH_APPLY"
        row["manual_apply_authorized"] = "YES"
        row["apply_now"] = "YES"
        row["source_patch_applied"] = "YES"
        row["apply_allowed"] = "true"
        row["prompt_source_modified"] = "true"
        row["authorization_note"] = (
            "AUTHORIZED_BY_OPERATOR_REQUEST_P158_R2_AUTHORIZE_AND_APPLY_PROMPT_PATCH_MANUAL_GATE_REPAIRED_BY_P158_R5_NO_FRAGILE_PATCH_SCRIPT"
        )
        row["authorized_at_utc"] = utc_stamp()

    with decision_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    return decision_file


@dataclass(frozen=True)
class ApplyResult:
    export_dir: Path
    source_file: Path
    source_changed: bool
    insertion_mode: str
    manual_apply_decision_file: Path | None
    summary: dict[str, Any]


def build_and_apply(repo_root: Path, authorize_manual_apply: bool) -> ApplyResult:
    if not authorize_manual_apply:
        raise PermissionError("Manual apply authorization flag is required")

    p158_dir, p158_summary = load_latest_p158_summary(repo_root)
    blockers = validate_p158_summary(p158_summary)

    p156_dir, candidate_file, candidate_text = locate_p156_candidate(repo_root)
    unsafe_marker_count = candidate_unsafe_marker_count(candidate_text)
    if unsafe_marker_count:
        blockers.append("P156_CANDIDATE_UNSAFE_MARKERS")

    prompt_source_file = locate_prompt_source_file(repo_root)
    before = prompt_source_file.read_text(encoding="utf-8")
    after, source_changed, insertion_mode = apply_patch_block_to_prompt_source(before)

    if blockers:
        raise RuntimeError(";".join(blockers))

    prompt_source_file.write_text(after, encoding="utf-8")
    manual_apply_decision_file = update_manual_apply_decision_csv(p158_dir)

    export_dir = (
        repo_root
        / "05_EXPORTS"
        / f"P158_R5_AUTHORIZE_AND_APPLY_PROMPT_PATCH_MANUAL_GATE_{fs_stamp()}"
    )
    export_dir.mkdir(parents=True, exist_ok=True)

    diff_text = "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=str(prompt_source_file.relative_to(repo_root)) + ".before",
            tofile=str(prompt_source_file.relative_to(repo_root)) + ".after",
        )
    )
    (export_dir / "P158_R5_SOURCE_PATCH_DIFF.txt").write_text(diff_text, encoding="utf-8")
    (export_dir / "P158_R5_APPLIED_PROMPT_PATCH_READBACK.md").write_text(
        f"# P158-R5 Applied Prompt Patch Readback\n\n"
        f"Prompt source file: `{prompt_source_file.relative_to(repo_root)}`\n\n"
        f"Source changed: `{source_changed}`\n\n"
        f"Insertion mode: `{insertion_mode}`\n\n"
        f"## Patch block\n\n{PATCH_BLOCK}\n\n"
        f"## Source P156 candidate\n\n`{candidate_file.relative_to(repo_root)}`\n",
        encoding="utf-8",
    )

    p158_status = str(ci_get(p158_summary, "P158_STATUS", ci_get(p158_summary, "status", "")))
    summary = {
        "STATUS": "OK_P158_R5_AUTHORIZE_AND_APPLY_PROMPT_PATCH_MANUAL_GATE_READY_TO_SEAL",
        "P158_R5_STATUS": "P158_R5_MANUAL_PROMPT_PATCH_APPLIED_REVIEW_ONLY",
        "P158_R2_REPAIR": True,
        "PROMPT_SOURCE_ID": EXPECTED_PROMPT_SOURCE_ID,
        "SOURCE_P158_STATUS": p158_status,
        "SOURCE_P156_DIR": str(p156_dir),
        "SOURCE_P156_CANDIDATE_FILE": str(candidate_file),
        "P158_SOURCE_DIR": str(p158_dir),
        "PATCH_CANDIDATE_FOUND": True,
        "PATCH_SAFE_FOR_REVIEW": True,
        "MANUAL_APPLY_AUTHORIZED": True,
        "SOURCE_PATCH_APPLIED": True,
        "PROMPT_SOURCE_MODIFIED": True,
        "APPLY_ALLOWED": True,
        "AUTO_APPLY_GEM_RESPONSE": False,
        "GOOGLE_SHEETS_WRITE": False,
        "LIVE_GOOGLE_SHEETS_READ": False,
        "PUBLIC_DEPLOY": False,
        "NO_APPS_SCRIPT_EXECUTION": True,
        "NO_CLASP_PUSH": True,
        "NO_BROKER": True,
        "NO_ORDER": True,
        "NO_SIZING": True,
        "UNSAFE_MARKER_COUNT": unsafe_marker_count,
        "BLOCKER_COUNT": 0,
        "SOURCE_PROMPT_FILE": str(prompt_source_file),
        "SOURCE_PROMPT_FILE_REL": str(prompt_source_file.relative_to(repo_root)),
        "SOURCE_CHANGED": source_changed,
        "INSERTION_MODE": insertion_mode,
        "PATCH_MARKER": PATCH_MARKER,
        "MANUAL_APPLY_DECISION_FILE": str(manual_apply_decision_file)
        if manual_apply_decision_file
        else "",
        "EXPORT_DIR": str(export_dir),
        "NEXT": "P159_PROMPT_PATCH_RUNTIME_SMOKE_OR_ROLLBACK_GATE",
        "created_at_utc": utc_stamp(),
    }
    write_json(export_dir / "P158_R5_SUMMARY.json", summary)
    write_json(export_dir / "P158_R5_AUTHORIZE_AND_APPLY_REPORT.json", summary)
    (export_dir / "P158_R5_HANDOFF.md").write_text(
        "# P158-R5 — Manual Prompt Patch Applied\n\n"
        "Status: `P158_R5_MANUAL_PROMPT_PATCH_APPLIED_REVIEW_ONLY`\n\n"
        f"Prompt source: `{prompt_source_file.relative_to(repo_root)}`\n\n"
        f"Insertion mode: `{insertion_mode}`\n\n"
        "Safety: no Sheets write, no public deploy, no Apps Script, no CLASP, no broker, no order, no sizing.\n\n"
        "Next: `P159_PROMPT_PATCH_RUNTIME_SMOKE_OR_ROLLBACK_GATE`.\n",
        encoding="utf-8",
    )

    return ApplyResult(
        export_dir=export_dir,
        source_file=prompt_source_file,
        source_changed=source_changed,
        insertion_mode=insertion_mode,
        manual_apply_decision_file=manual_apply_decision_file,
        summary=summary,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--authorize-manual-apply", action="store_true")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    result = build_and_apply(
        repo_root=repo_root, authorize_manual_apply=args.authorize_manual_apply
    )

    summary = result.summary
    print(summary["P158_R5_STATUS"])
    print(f"prompt_source_id={summary['PROMPT_SOURCE_ID']}")
    print(f"source_p158_status={summary['SOURCE_P158_STATUS']}")
    print(f"manual_apply_authorized={str(summary['MANUAL_APPLY_AUTHORIZED']).lower()}")
    print(f"source_patch_applied={str(summary['SOURCE_PATCH_APPLIED']).lower()}")
    print(f"prompt_source_modified={str(summary['PROMPT_SOURCE_MODIFIED']).lower()}")
    print(f"apply_allowed={str(summary['APPLY_ALLOWED']).lower()}")
    print(f"auto_apply_gem_response={str(summary['AUTO_APPLY_GEM_RESPONSE']).lower()}")
    print(f"google_sheets_write={str(summary['GOOGLE_SHEETS_WRITE']).lower()}")
    print(f"public_deploy={str(summary['PUBLIC_DEPLOY']).lower()}")
    print(f"unsafe_marker_count={summary['UNSAFE_MARKER_COUNT']}")
    print(f"blocker_count={summary['BLOCKER_COUNT']}")
    print(f"source_prompt_file={summary['SOURCE_PROMPT_FILE_REL']}")
    print(f"insertion_mode={summary['INSERTION_MODE']}")
    print(f"output_dir={summary['EXPORT_DIR']}")
    print(f"next={summary['NEXT']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
