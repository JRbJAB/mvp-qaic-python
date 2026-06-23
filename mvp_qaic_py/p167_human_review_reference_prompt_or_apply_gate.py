from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

STATUS = "P167_REFERENCE_PROMPT_HUMAN_REVIEW_GATE_READY_REVIEW_ONLY"
NEXT = "P168_REFERENCE_PROMPT_MANUAL_APPLY_OR_STOP"
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
    "auto_apply": False,
}
REQUIRED_P166_FILES = (
    "P166_REFERENCE_PROMPT_DRAFT_V1.md",
    "P166_OPERATOR_QUICK_USE_PROMPT.md",
    "P166_JSON_OUTPUT_SCHEMA_DRAFT.md",
    "P166_PROMPT_SOURCE_SELECTION.csv",
    "P166_REBUILD_REPORT.md",
    "P166_SUMMARY.json",
)


@dataclass(frozen=True)
class ReviewItem:
    review_item_id: str
    source_file: str
    review_scope: str
    recommended_decision: str
    human_decision: str
    apply_now: str
    blocker_if_not_reviewed: str
    notes: str


def _utc_stamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).strftime("%Y%m%d_%H%M%S")


def discover_latest_p166_export(repo: Path) -> Path:
    exports = repo / "05_EXPORTS"
    candidates = sorted(
        exports.glob("P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_*"),
        key=lambda p: p.name,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError("No P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_* export found")
    return candidates[0]


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def validate_p166_export(p166_dir: Path) -> list[str]:
    blockers: list[str] = []
    for name in REQUIRED_P166_FILES:
        if not (p166_dir / name).exists():
            blockers.append(f"MISSING_{name}")
    summary = read_json(p166_dir / "P166_SUMMARY.json")
    if summary:
        if summary.get("runtime_prompt_modified") is not False:
            blockers.append("P166_RUNTIME_PROMPT_MODIFIED_NOT_FALSE")
        if summary.get("apply_allowed") is not False:
            blockers.append("P166_APPLY_ALLOWED_NOT_FALSE")
        if int(summary.get("blocker_count", 0)) != 0:
            blockers.append("P166_BLOCKER_COUNT_NON_ZERO")
    return blockers


def build_review_items(p166_dir: Path) -> list[ReviewItem]:
    source_count = count_csv_rows(p166_dir / "P166_PROMPT_SOURCE_SELECTION.csv")
    return [
        ReviewItem(
            review_item_id="P167-001",
            source_file="P166_REFERENCE_PROMPT_DRAFT_V1.md",
            review_scope="Valider la demande globale, les hard rules, les blocs attendus et la sÃ©paration MVP_QAIC_PY / QAIC_PY.",
            recommended_decision="REVIEW_REQUIRED",
            human_decision="PENDING",
            apply_now="NO",
            blocker_if_not_reviewed="Cannot promote rebuilt prompt without human review.",
            notes="Ne pas appliquer au runtime tant que la revue humaine n'est pas explicite.",
        ),
        ReviewItem(
            review_item_id="P167-002",
            source_file="P166_OPERATOR_QUICK_USE_PROMPT.md",
            review_scope="VÃ©rifier que le prompt opÃ©rateur rapide est utilisable pour GEM portfolio image/capture.",
            recommended_decision="REVIEW_REQUIRED",
            human_decision="PENDING",
            apply_now="NO",
            blocker_if_not_reviewed="Operator quick prompt remains draft only.",
            notes="Doit rester sans broker/order/sizing.",
        ),
        ReviewItem(
            review_item_id="P167-003",
            source_file="P166_JSON_OUTPUT_SCHEMA_DRAFT.md",
            review_scope="VÃ©rifier que le schÃ©ma JSON couvre extraction, data quality, risk review, decision review et audit metadata.",
            recommended_decision="REVIEW_REQUIRED",
            human_decision="PENDING",
            apply_now="NO",
            blocker_if_not_reviewed="Schema cannot be used as runtime contract without approval.",
            notes="Enums techniques Ã  garder stables.",
        ),
        ReviewItem(
            review_item_id="P167-004",
            source_file="P166_PROMPT_SOURCE_SELECTION.csv",
            review_scope=f"ContrÃ´ler les candidats source indexÃ©s par P166. source_candidate_count={source_count}.",
            recommended_decision="REVIEW_REQUIRED",
            human_decision="PENDING",
            apply_now="NO",
            blocker_if_not_reviewed="Source selection remains unapproved.",
            notes="P132/P133 reste runtime smoke contract only.",
        ),
        ReviewItem(
            review_item_id="P167-005",
            source_file="P166_REBUILD_REPORT.md",
            review_scope="Valider que le rebuild est cohÃ©rent avec la hiÃ©rarchie MVP_QAIC_PY, QAIC_PY, QAIT_PY.",
            recommended_decision="REVIEW_REQUIRED",
            human_decision="PENDING",
            apply_now="NO",
            blocker_if_not_reviewed="No apply gate can open.",
            notes="MVP_QAIC_PY ne doit pas absorber le backend trading QAIC_PY.",
        ),
    ]


def _write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_gate_report(p166_dir: Path, review_items: list[ReviewItem], blockers: list[str]) -> str:
    pending = sum(1 for item in review_items if item.human_decision == "PENDING")
    return f"""# P167 â€” Human Review Reference Prompt Gate

## Decision

`{STATUS}`

P167 creates a human-review workbench for the P166 rebuilt reference prompt. It does not modify the runtime prompt and it does not open apply.

## Source

- P166 export: `{p166_dir}`
- review_items: `{len(review_items)}`
- pending_review_items: `{pending}`
- validation_blockers: `{len(blockers)}`

## Hierarchy guard

- `MVP_QAIC_PY` = MVP product layer: prompt, lexique, webapp, operator workflow, source recovery.
- `QAIC_PY` = private trading backend / Revolut X / execution infrastructure.
- `QAIT_PY` = actions and commodities lane.

No cross-project absorption is authorized.

## Safety

```json
{json.dumps(SAFETY, indent=2)}
```

## Human instruction

Fill `P167_REFERENCE_PROMPT_REVIEW_WORKBENCH.csv` manually later. Keep `apply_now=NO` unless a separate explicit manual authorization is given.
"""


def run(repo: Path, output_dir: Path | None = None) -> dict[str, object]:
    p166_dir = discover_latest_p166_export(repo)
    blockers = validate_p166_export(p166_dir)
    review_items = build_review_items(p166_dir)
    pending_review_count = sum(1 for item in review_items if item.human_decision == "PENDING")
    apply_now_yes_count = sum(1 for item in review_items if item.apply_now == "YES")

    stamp = _utc_stamp()
    out = output_dir or (repo / "05_EXPORTS" / f"P167_HUMAN_REVIEW_REFERENCE_PROMPT_GATE_{stamp}")
    out.mkdir(parents=True, exist_ok=True)

    _write_csv(
        out / "P167_REFERENCE_PROMPT_REVIEW_WORKBENCH.csv",
        (asdict(item) for item in review_items),
        [
            "review_item_id",
            "source_file",
            "review_scope",
            "recommended_decision",
            "human_decision",
            "apply_now",
            "blocker_if_not_reviewed",
            "notes",
        ],
    )
    (out / "P167_GATE_REPORT.md").write_text(
        build_gate_report(p166_dir, review_items, blockers), encoding="utf-8"
    )
    (out / "P167_OPERATOR_REVIEW_INSTRUCTIONS.md").write_text(
        """# P167 â€” Operator Review Instructions

1. Open `P166_REFERENCE_PROMPT_DRAFT_V1.md`.
2. Compare with your intended MVP scope: prompt, lexique, webapp, operator workflow.
3. Confirm that QAIC_PY backend trading scope is not mixed into MVP_QAIC_PY.
4. Fill `P167_REFERENCE_PROMPT_REVIEW_WORKBENCH.csv` manually only when reviewed.
5. Keep `apply_now=NO` unless a separate explicit manual apply authorization is given.
""",
        encoding="utf-8",
    )
    summary = {
        "status": STATUS,
        "p166_source_dir": str(p166_dir),
        "output_dir": str(out),
        "review_item_count": len(review_items),
        "pending_review_count": pending_review_count,
        "apply_now_yes_count": apply_now_yes_count,
        "human_review_required": True,
        "reference_prompt_review_workbench_created": True,
        "operator_review_instructions_created": True,
        "runtime_prompt_modified": False,
        "apply_allowed": False,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "next": NEXT,
        **SAFETY,
    }
    (out / "P167_SUMMARY.json").write_text(
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
    print(f"review_item_count={summary['review_item_count']}")
    print(f"pending_review_count={summary['pending_review_count']}")
    print(f"apply_now_yes_count={summary['apply_now_yes_count']}")
    print(f"runtime_prompt_modified={summary['runtime_prompt_modified']}")
    print(f"apply_allowed={summary['apply_allowed']}")
    print(f"blocker_count={summary['blocker_count']}")
    print(f"output_dir={summary['output_dir']}")
    print(f"next={summary['next']}")
