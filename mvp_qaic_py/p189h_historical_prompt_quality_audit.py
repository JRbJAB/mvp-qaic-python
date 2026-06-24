from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SAFETY_FLAGS: dict[str, bool] = {
    "gem_call_executed": False,
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "source_prompt_modified": False,
}


AUDIT_COLUMNS = [
    "prompt_id",
    "source_path",
    "source_kind",
    "sha12",
    "dup_group",
    "char_count",
    "line_count",
    "has_gem",
    "has_portfolio",
    "has_image",
    "has_review_required",
    "has_usd_reference",
    "has_no_order",
    "has_no_sizing",
    "has_no_auto_apply",
    "has_missing_data",
    "has_blockers",
    "has_schema_rules",
    "has_json_contract",
    "quality_score",
    "risk_score",
    "migration_decision",
    "migration_reason",
    "candidate_extract",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _sha12_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:12]


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path, *, max_bytes: int = 400_000) -> str:
    data = path.read_bytes()[:max_bytes]
    return data.decode("utf-8", errors="replace")


def _normalise_text(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


def _candidate_roots(root: Path) -> list[Path]:
    return [
        root / "mvp_qaic_py",
        root / "05_EXPORTS",
        root / "01_DOCS",
        root / "docs",
        root / "prompts",
    ]


def _skip_path(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    blocked = {
        ".git",
        ".ruff_cache",
        ".pytest_cache",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        "dist",
        "build",
    }
    if parts & blocked:
        return True
    if path.name.lower() == "desktop.ini":
        return True
    if path.suffix.lower() not in {".py", ".md", ".txt", ".json"}:
        return True
    return False


def _looks_prompt_like(path: Path, text: str) -> bool:
    name = path.name.lower()
    lower = text.lower()
    name_hit = any(
        token in name
        for token in [
            "prompt",
            "gem",
            "portfolio",
            "multimodal",
            "review",
            "p132",
            "p133",
            "p158",
            "p167",
            "p182",
        ]
    )
    text_hit = any(
        token in lower
        for token in [
            "review_required",
            "image_used",
            "reference_currency",
            "missing_data",
            "blockers",
            "no_order",
            "no_sizing",
            "gem",
            "portfolio",
            "prompt",
        ]
    )
    return name_hit or text_hit


def _discover_prompt_files(root: Path, *, max_files: int = 2500) -> list[Path]:
    found: list[Path] = []
    for base in _candidate_roots(root):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if len(found) >= max_files:
                return found
            if not path.is_file() or _skip_path(path):
                continue
            if path.stat().st_size > 2_000_000:
                continue
            try:
                text = _read_text(path)
            except OSError:
                continue
            if _looks_prompt_like(path, text):
                found.append(path)
    return found


def _source_kind(path: Path, text: str) -> str:
    blob = f"{path.as_posix().lower()} {text[:8000].lower()}"
    if "active_prompt" in blob or "multimodal_gem_image_prompt_usd_contract" in blob:
        return "ACTIVE_RUNTIME_OR_SOURCE"
    if "reference" in blob or "audit" in blob or "p182" in blob:
        return "REFERENCE_AUDIT"
    if "p186_smoke" in blob:
        return "SMOKE_IGNORED_REFERENCE"
    return "HISTORICAL"


def _flag(lower: str, *patterns: str) -> bool:
    return any(pattern in lower for pattern in patterns)


def _quality_and_risk(lower: str, flags: dict[str, bool]) -> tuple[int, int]:
    quality = 0
    quality += 10 if flags["has_gem"] else 0
    quality += 10 if flags["has_portfolio"] else 0
    quality += 10 if flags["has_image"] else 0
    quality += 10 if flags["has_review_required"] else 0
    quality += 8 if flags["has_usd_reference"] else 0
    quality += 12 if flags["has_no_order"] else 0
    quality += 12 if flags["has_no_sizing"] else 0
    quality += 8 if flags["has_no_auto_apply"] else 0
    quality += 8 if flags["has_missing_data"] else 0
    quality += 8 if flags["has_blockers"] else 0
    quality += 8 if flags["has_schema_rules"] else 0
    quality += 4 if flags["has_json_contract"] else 0

    risky_terms = [
        "place_order",
        "post_order",
        "cancel_order",
        "buy ",
        "sell ",
        "market order",
        "limit order",
        "sizing",
        "position size",
        "leverage",
        "take profit",
        "stop loss",
        "tp ",
        "sl ",
    ]
    risk_hits = sum(1 for term in risky_terms if term in lower)
    risk = min(100, risk_hits * 15)

    if flags["has_no_order"]:
        risk = max(0, risk - 25)
    if flags["has_no_sizing"]:
        risk = max(0, risk - 25)
    if flags["has_no_auto_apply"]:
        risk = max(0, risk - 15)

    return min(100, quality), risk


def _candidate_extract(text: str, *, limit: int = 420) -> str:
    lines = []
    keywords = [
        "hard rule",
        "règle",
        "review_required",
        "image_used",
        "reference_currency",
        "missing_data",
        "blockers",
        "no_order",
        "no_sizing",
        "portfolio",
        "gem",
    ]
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lower = line.lower()
        if any(keyword in lower for keyword in keywords):
            lines.append(line)
        if len(" | ".join(lines)) >= limit:
            break
    extract = " | ".join(lines)
    if not extract:
        extract = text.strip().replace("\n", " ")[:limit]
    return extract[:limit]


def _decision(
    *,
    source_kind: str,
    quality_score: int,
    risk_score: int,
    flags: dict[str, bool],
) -> tuple[str, str]:
    missing_core = [
        name
        for name in [
            "has_review_required",
            "has_image",
            "has_usd_reference",
            "has_no_order",
            "has_no_sizing",
            "has_missing_data",
            "has_blockers",
        ]
        if not flags[name]
    ]

    if risk_score >= 55 and (not flags["has_no_order"] or not flags["has_no_sizing"]):
        return "REJECT_UNSAFE", "Risk markers without explicit no_order/no_sizing guards."

    if source_kind == "ACTIVE_RUNTIME_OR_SOURCE":
        if quality_score >= 70 and risk_score <= 30:
            return "ACTIVE_KEEP", "Active-like prompt with acceptable safety coverage."
        return "REVIEW_REQUIRED", "Active-like prompt missing important safety fields."

    if quality_score >= 75 and risk_score <= 30:
        return "MERGE_INTO_MASTER", "High value historical rules candidate for master prompt."

    if quality_score >= 50 and risk_score <= 45:
        return "REFERENCE_ONLY", "Useful reference but not strong enough for direct merge."

    if len(missing_core) >= 4:
        return "ARCHIVE_LEGACY", "Too many mandatory prompt contract fields are missing."

    return "REVIEW_REQUIRED", "Needs manual review before migration decision."


def audit_historical_prompts(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    files = _discover_prompt_files(root)
    rows: list[dict[str, Any]] = []

    for path in files:
        text = _read_text(path)
        lower = text.lower()
        normalised = _normalise_text(text)
        sha12 = _sha12_text(text)
        dup_group = _sha12_text(normalised[:2000])
        source_kind = _source_kind(path, text)

        flags = {
            "has_gem": _flag(lower, "gem", "gemini"),
            "has_portfolio": _flag(lower, "portfolio", "positions", "holdings"),
            "has_image": _flag(lower, "image_used", "screenshot", "capture", "image"),
            "has_review_required": _flag(lower, "review_required"),
            "has_usd_reference": _flag(lower, "reference_currency", "usd"),
            "has_no_order": _flag(lower, "no_order", "aucun ordre", '"order": false'),
            "has_no_sizing": _flag(lower, "no_sizing", "aucun sizing", '"sizing": false'),
            "has_no_auto_apply": _flag(lower, "auto_apply", "no_auto_apply"),
            "has_missing_data": _flag(lower, "missing_data", "données manquantes"),
            "has_blockers": _flag(lower, "blockers", "blocker_count"),
            "has_schema_rules": _flag(lower, "schema", "json schema", "contract"),
            "has_json_contract": _flag(lower, "{", "}", "json"),
        }
        quality_score, risk_score = _quality_and_risk(lower, flags)
        decision, reason = _decision(
            source_kind=source_kind,
            quality_score=quality_score,
            risk_score=risk_score,
            flags=flags,
        )

        rows.append(
            {
                "prompt_id": f"PROMPT-{sha12}",
                "source_path": _safe_rel(path, root),
                "source_kind": source_kind,
                "sha12": sha12,
                "dup_group": dup_group,
                "char_count": len(text),
                "line_count": len(text.splitlines()),
                **flags,
                "quality_score": quality_score,
                "risk_score": risk_score,
                "migration_decision": decision,
                "migration_reason": reason,
                "candidate_extract": _candidate_extract(text),
            }
        )

    rows.sort(
        key=lambda row: (
            str(row["migration_decision"]),
            -int(row["quality_score"]),
            int(row["risk_score"]),
            str(row["source_path"]),
        )
    )

    decision_counts = Counter(str(row["migration_decision"]) for row in rows)
    kind_counts = Counter(str(row["source_kind"]) for row in rows)

    return {
        "STATUS": "OK_P189H_HISTORICAL_PROMPT_QUALITY_AUDIT_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "audited_prompt_count": len(rows),
        "migration_matrix_ready": len(rows) > 0,
        "decision_counts": dict(sorted(decision_counts.items())),
        "source_kind_counts": dict(sorted(kind_counts.items())),
        "merge_candidate_count": decision_counts.get("MERGE_INTO_MASTER", 0),
        "active_keep_count": decision_counts.get("ACTIVE_KEEP", 0),
        "reference_only_count": decision_counts.get("REFERENCE_ONLY", 0),
        "archive_legacy_count": decision_counts.get("ARCHIVE_LEGACY", 0),
        "reject_unsafe_count": decision_counts.get("REJECT_UNSAFE", 0),
        "review_required_count": decision_counts.get("REVIEW_REQUIRED", 0),
        "rows": rows,
        "blocker_count": 0,
        "blockers": [],
        **SAFETY_FLAGS,
        "recommended_next": "P190H_PROMPT_MIGRATION_GROUPING_AND_MASTER_EXTRACT",
    }


def export_historical_prompt_quality_audit(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P189H_HISTORICAL_PROMPT_QUALITY_AUDIT_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = audit_historical_prompts(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P189H_HISTORICAL_PROMPT_QUALITY_AUDIT.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    csv_path = export_path / "P189H_PROMPT_MIGRATION_MATRIX.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=AUDIT_COLUMNS)
        writer.writeheader()
        for row in payload["rows"]:
            writer.writerow({key: row.get(key) for key in AUDIT_COLUMNS})

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "audited_prompt_count",
        "migration_matrix_ready",
        "decision_counts",
        "source_kind_counts",
        "merge_candidate_count",
        "active_keep_count",
        "reference_only_count",
        "archive_legacy_count",
        "reject_unsafe_count",
        "review_required_count",
        "blocker_count",
        "blockers",
        "gem_call_executed",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "auto_apply_gem_response",
        "source_prompt_modified",
        "recommended_next",
    ]
    summary = {key: payload.get(key) for key in summary_keys}
    (export_path / "P189H_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    top_merge = [
        row for row in payload["rows"] if row["migration_decision"] == "MERGE_INTO_MASTER"
    ][:20]
    lines = [
        "# P189H Historical Prompt Quality Audit",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- audited_prompt_count: {payload['audited_prompt_count']}",
        f"- merge_candidate_count: {payload['merge_candidate_count']}",
        f"- active_keep_count: {payload['active_keep_count']}",
        f"- reference_only_count: {payload['reference_only_count']}",
        f"- archive_legacy_count: {payload['archive_legacy_count']}",
        f"- reject_unsafe_count: {payload['reject_unsafe_count']}",
        f"- review_required_count: {payload['review_required_count']}",
        "",
        "## Top merge candidates",
    ]
    for row in top_merge:
        lines.append(
            f"- `{row['prompt_id']}` score={row['quality_score']} "
            f"risk={row['risk_score']} path={row['source_path']}"
        )
    lines.extend(
        [
            "",
            "## Safety",
            "- GEM_CALL_EXECUTED=False",
            "- AUTO_APPLY_GEM_RESPONSE=False",
            "- GOOGLE_SHEETS_WRITE=False",
            "- PUBLIC_SERVE=False",
            "- BROKER=False",
            "- ORDER=False",
            "- SIZING=False",
            "",
            "## Next",
            "- P190H_PROMPT_MIGRATION_GROUPING_AND_MASTER_EXTRACT",
        ]
    )
    (export_path / "P189H_REPORT.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P189H historical prompt quality audit.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_historical_prompt_quality_audit(
            args.project_root,
            export_dir=args.export_dir,
        )
        if args.write_export
        else audit_historical_prompts(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"AUDITED_PROMPT_COUNT={payload['audited_prompt_count']}")
        print(f"MERGE_CANDIDATE_COUNT={payload['merge_candidate_count']}")
        print(f"REJECT_UNSAFE_COUNT={payload['reject_unsafe_count']}")

    return 0 if payload["migration_matrix_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
