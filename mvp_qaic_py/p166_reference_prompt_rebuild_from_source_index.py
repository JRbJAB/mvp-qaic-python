from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

STATUS = "P166_REFERENCE_PROMPT_REBUILD_READY_REVIEW_ONLY"
SAFETY = {
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "runtime_prompt_modified": False,
    "apply_allowed": False,
    "public_deploy": False,
}
KEYWORDS = (
    "prompt",
    "gpt",
    "gem",
    "portfolio",
    "image",
    "capture",
    "json",
    "review",
    "human",
    "decision",
    "risk",
    "risque",
    "revolut",
    "journal",
    "lexique",
)


@dataclass(frozen=True)
class SourceCandidate:
    source_file: str
    source_row: int
    source_kind: str
    name: str
    score: int
    matched_keywords: str
    summary: str


def _utc_stamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).strftime("%Y%m%d_%H%M%S")


def _read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    rows: list[dict[str, str]] = []
    for row in csv.DictReader(text.splitlines()):
        rows.append({str(k or "").strip(): str(v or "").strip() for k, v in row.items()})
    return rows


def _compact(row: dict[str, str], max_chars: int = 360) -> str:
    parts: list[str] = []
    for key, value in row.items():
        if value:
            parts.append(f"{key}={value}")
    text = " | ".join(parts)
    return text[:max_chars]


def _pick_name(row: dict[str, str]) -> str:
    for key in (
        "function_name",
        "name",
        "module_name",
        "file_name",
        "script_name",
        "title",
        "rel_path",
        "path",
    ):
        if row.get(key):
            return row[key]
    return "UNKNOWN_SOURCE"


def _classify_source(path: Path) -> str:
    upper = path.name.upper()
    if "PROMPT_ENGINE" in upper or "PROMPT" in upper:
        return "PROMPT_ENGINE_OR_PROMPT_SOURCE"
    if "FUNCTION_INDEX" in upper:
        return "APPS_SCRIPT_FUNCTION_INDEX"
    if "MIGRATION_MAP" in upper:
        return "FUNCTIONAL_MIGRATION_MAP"
    if "SOURCE_REGISTRY" in upper:
        return "SOURCE_REGISTRY"
    if "SHEETS" in upper:
        return "SHEETS_ACCESS_PLAN"
    return "P165_SOURCE_INDEX"


def score_row(row: dict[str, str], source_kind: str) -> tuple[int, list[str]]:
    blob = " ".join(row.values()).lower()
    matched = [kw for kw in KEYWORDS if kw in blob]
    score = len(matched) * 10
    if source_kind == "PROMPT_ENGINE_OR_PROMPT_SOURCE":
        score += 80
    if "prompt" in blob and ("gem" in blob or "gpt" in blob):
        score += 50
    if "portfolio" in blob and "json" in blob:
        score += 35
    if "human" in blob or "review" in blob:
        score += 20
    if "order" in blob or "broker" in blob or "sizing" in blob:
        score += 5  # keep as safety signal, not execution authorization
    return score, matched


def discover_latest_p165_export(repo: Path) -> Path:
    exports = repo / "05_EXPORTS"
    candidates = sorted(
        exports.glob("P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(
            "No P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_* export found"
        )
    return candidates[0]


def build_candidates(p165_dir: Path) -> list[SourceCandidate]:
    rows: list[SourceCandidate] = []
    for csv_path in sorted(p165_dir.glob("P165_R3_*.csv")):
        source_kind = _classify_source(csv_path)
        for idx, row in enumerate(_read_csv_dicts(csv_path), start=2):
            score, matched = score_row(row, source_kind)
            if score <= 0:
                continue
            rows.append(
                SourceCandidate(
                    source_file=csv_path.name,
                    source_row=idx,
                    source_kind=source_kind,
                    name=_pick_name(row),
                    score=score,
                    matched_keywords="|".join(matched),
                    summary=_compact(row),
                )
            )
    rows.sort(key=lambda r: (-r.score, r.source_kind, r.name))
    return rows


def _write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_reference_prompt(candidates: list[SourceCandidate]) -> str:
    top = candidates[:20]
    top_lines = "\n".join(
        f"- {c.name} â€” {c.source_kind} â€” score={c.score} â€” `{c.source_file}` row {c.source_row}"
        for c in top
    )
    return f"""# P166 â€” Reference Prompt Draft V1 â€” Review Only

## Status

`{STATUS}`

This is a candidate prompt rebuilt from the P165-R3 initial system source index. It is not applied to runtime.

## Source hierarchy

- `MVP_QAIC_PY` = MVP product layer: lexique, prompt cockpit, local/private operator workflow, future public webapp preparation.
- `QAIC_PY` = private technical trading backend and execution-capable infrastructure, kept separate.
- Google Sheets / Apps Script historical system = source to recover and migrate, read-only until explicitly reviewed.
- `P132/P133` = runtime contract / smoke reference only, not the final business reference prompt.

## Mission globale

Analyze a crypto portfolio screenshot or equivalent portfolio text, extract structured information, identify missing data, assess review needs, and return a safe human-review decision package.

## Hard rules

- French explanatory text is allowed, but technical JSON keys and enums must remain stable.
- Never invent balances, quantities, P&L, prices, PRU, risk exposure, or broker state.
- Never recommend or prepare a real order, automatic sizing, broker execution, or hidden live action.
- If data is missing, stale, ambiguous, unreadable, or inconsistent, return `REVIEW_REQUIRED` or `INSUFFICIENT_DATA`.
- Portfolio protection has priority over alpha signal.
- Human review remains mandatory.

## Expected input

1. Portfolio screenshot / image capture.
2. Optional copied portfolio text.
3. Optional context notes from the operator.

## Expected output blocks

1. `portfolio_extraction` â€” observed assets and values, with confidence and missing fields.
2. `data_quality_review` â€” freshness, ambiguity, OCR/image limitations, missing fields.
3. `risk_review` â€” concentration, exposure, liquidity, volatility, drawdown, unknowns.
4. `decision_review` â€” no automatic action, only human-review status.
5. `correction_backlog` â€” prompt/data/UI improvements found during the run.
6. `audit_metadata` â€” source mode, image usage, timestamp, schema version.

## Required JSON stance

The response must be structured, conservative, auditable, and safe for local private MVP usage.

## Source candidates used for review

{top_lines if top_lines else "- No scored source candidate found; stop and review P165-R3 source index."}

## Safety footer

`runtime_prompt_modified=false`  
`apply_allowed=false`  
`google_sheets_write=false`  
`apps_script_execution=false`  
`broker=false`  
`order=false`  
`sizing=false`
"""


def build_operator_quick_prompt() -> str:
    return """# P166 â€” Operator Quick Prompt â€” Draft

Use this with one portfolio screenshot/image and optional copied text.

Analyze this crypto portfolio screenshot in French. Keep JSON keys and technical enums in English. Do not invent missing data. Do not propose broker execution, real orders, or automatic sizing. If anything important is missing or unclear, return `REVIEW_REQUIRED` and explain exactly what is missing.

Return:
1. portfolio_extraction
2. data_quality_review
3. risk_review
4. decision_review
5. correction_backlog
6. audit_metadata
"""


def build_schema_draft() -> str:
    return """# P166 â€” JSON Output Schema Draft

```json
{
  "analysis_level": "IMAGE_USED | TEXT_USED | IMAGE_AND_TEXT_USED | INSUFFICIENT_DATA",
  "decision_status": "REVIEW_REQUIRED | NO_ACTION | WATCHLIST_REVIEW | BLOCKED",
  "human_final_decision": "NO_ACTION | REVIEW_LATER | MANUAL_ACTION_OUTSIDE_SYSTEM",
  "portfolio_extraction": [],
  "data_quality_review": [],
  "risk_review": [],
  "decision_review": [],
  "correction_backlog": [],
  "audit_metadata": {
    "schema_version": "p166_reference_prompt_draft.v1",
    "runtime_prompt_modified": false,
    "apply_allowed": false,
    "google_sheets_write": false,
    "apps_script_execution": false,
    "broker": false,
    "order": false,
    "sizing": false
  }
}
```
"""


def run(repo: Path, output_dir: Path | None = None) -> dict[str, object]:
    p165_dir = discover_latest_p165_export(repo)
    candidates = build_candidates(p165_dir)
    stamp = _utc_stamp()
    out = output_dir or (
        repo / "05_EXPORTS" / f"P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_{stamp}"
    )
    out.mkdir(parents=True, exist_ok=True)

    _write_csv(
        out / "P166_PROMPT_SOURCE_SELECTION.csv",
        (asdict(c) for c in candidates),
        [
            "source_file",
            "source_row",
            "source_kind",
            "name",
            "score",
            "matched_keywords",
            "summary",
        ],
    )
    (out / "P166_REFERENCE_PROMPT_DRAFT_V1.md").write_text(
        build_reference_prompt(candidates), encoding="utf-8"
    )
    (out / "P166_OPERATOR_QUICK_USE_PROMPT.md").write_text(
        build_operator_quick_prompt(), encoding="utf-8"
    )
    (out / "P166_JSON_OUTPUT_SCHEMA_DRAFT.md").write_text(build_schema_draft(), encoding="utf-8")
    report = f"""# P166 â€” Reference Prompt Rebuild From Source Index

## Decision

- Review-only candidate created from P165-R3 source index.
- `P132/P133` remains runtime contract only.
- Runtime prompt is not modified.

## Counts

- source_candidates: `{len(candidates)}`
- selected_top_for_draft: `{min(len(candidates), 20)}`

## Safety

{json.dumps(SAFETY, indent=2)}
"""
    (out / "P166_REBUILD_REPORT.md").write_text(report, encoding="utf-8")
    summary = {
        "status": STATUS,
        "p165_source_dir": str(p165_dir),
        "output_dir": str(out),
        "source_candidate_count": len(candidates),
        "reference_prompt_draft_created": True,
        "operator_quick_prompt_created": True,
        "json_schema_draft_created": True,
        "runtime_prompt_modified": False,
        "apply_allowed": False,
        "blocker_count": 0,
        "next": "P167_HUMAN_REVIEW_REFERENCE_PROMPT_OR_APPLY_GATE",
        **SAFETY,
    }
    (out / "P166_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()
    summary = run(
        Path(args.repo).resolve(), Path(args.output_dir).resolve() if args.output_dir else None
    )
    print(summary["status"])
    print(f"source_candidate_count={summary['source_candidate_count']}")
    print(f"reference_prompt_draft_created={summary['reference_prompt_draft_created']}")
    print(f"runtime_prompt_modified={summary['runtime_prompt_modified']}")
    print(f"apply_allowed={summary['apply_allowed']}")
    print(f"blocker_count={summary['blocker_count']}")
    print(f"output_dir={summary['output_dir']}")
    print(f"next={summary['next']}")
