from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

PROMPT_SOURCE_ID_CURRENT = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
STATUS_READY = "P164_HISTORICAL_PROMPTS_AUDITED_REFERENCE_CANDIDATE_READY_REVIEW_ONLY"
FINAL_STATUS = "OK_P164_HISTORICAL_PROMPT_AUDIT_REFERENCE_REBUILD_READY_REVIEW_ONLY"
NEXT_STEP = "P165_HUMAN_REVIEW_REFERENCE_PROMPT_SELECTION_OR_STOP"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
}
ALLOWED_SUFFIXES = {".py", ".md", ".txt", ".csv", ".json", ".html", ".yaml", ".yml"}

KEYWORDS = {
    "demande globale": 30,
    "plusieurs points": 28,
    "mission globale": 24,
    "prompt global": 22,
    "prompt de référence": 22,
    "prompt historique": 20,
    "gem": 14,
    "portfolio": 14,
    "capture": 12,
    "image": 12,
    "revolut": 12,
    "json": 10,
    "human_review": 12,
    "human review": 12,
    "review_required": 10,
    "risk": 8,
    "risque": 8,
    "decision": 8,
    "décision": 8,
    "hard rules": 7,
    "no broker": 8,
    "no order": 8,
    "no sizing": 8,
    "P132": -14,
    "P133": -14,
}


@dataclass(frozen=True)
class PromptCandidate:
    rel_path: str
    suffix: str
    size_bytes: int
    source_kind: str
    score: int
    keyword_hits: str
    excerpt: str


def _read(path: Path) -> str:
    if path.stat().st_size > 260_000:
        return ""
    for enc in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _files(repo_root: Path) -> Iterable[Path]:
    for p in repo_root.rglob("*"):
        if not p.is_file():
            continue
        parts = p.relative_to(repo_root).parts
        if any(part in EXCLUDED_DIR_NAMES for part in parts):
            continue
        if p.suffix.lower() in ALLOWED_SUFFIXES:
            yield p


def _is_current_runtime_contract(rel: str, lower: str) -> bool:
    r = rel.lower().replace("\\", "/")
    current_runtime_files = {
        "mvp_qaic_py/multimodal_gem_image_prompt_usd_contract.py",
    }
    if r in current_runtime_files:
        return True
    if "p132" in r or "p133" in r:
        return True
    if "p132" in lower or "p133" in lower:
        if "multimodal" in r or "gem_image_prompt" in r or "portfolio" in lower:
            return True
    return False


def _classify(rel: str, lower: str) -> str:
    r = rel.lower()
    if _is_current_runtime_contract(rel, lower):
        return "CURRENT_RUNTIME_CONTRACT_REFERENCE"
    if any(f"p{n}" in r for n in range(152, 164)):
        return "REAL_CASE_CORRECTION_CHAIN_REFERENCE"
    if "05_exports" in r:
        return "EXPORT_ARCHIVE_REFERENCE"
    if "prompt" in r and any(x in r for x in ("histor", "archive", "old", "ancien")):
        return "HISTORICAL_PROMPT_SOURCE_CANDIDATE"
    if "prompt" in lower and ("demande globale" in lower or "plusieurs points" in lower):
        return "HISTORICAL_PROMPT_SOURCE_CANDIDATE"
    if "prompt" in r:
        return "PROMPT_RELATED_SOURCE_CANDIDATE"
    return "SUPPORTING_PROMPT_CONTEXT"


def _score(rel: str, text: str) -> tuple[str, int]:
    hay = f"{rel}\n{text}".lower()
    hits, score = [], 0
    for k, v in KEYWORDS.items():
        if k.lower() in hay:
            hits.append(k)
            score += v
    r = rel.lower()
    if any(x in r for x in ("histor", "archive", "old", "ancien")):
        hits.append("path_historical_bonus")
        score += 20
    if "prompt" in r:
        hits.append("path_prompt_bonus")
        score += 12
    if "p132" in r or "p133" in r:
        hits.append("p132_p133_demote_runtime_contract_only")
        score -= 25
    return "|".join(hits[:40]), score


def _excerpt(text: str) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return ""
    lower = compact.lower()
    start = 0
    for anchor in (
        "demande globale",
        "plusieurs points",
        "mission globale",
        "prompt global",
        "input mode",
        "hard rules",
        "portfolio",
        "gem",
        "json",
    ):
        idx = lower.find(anchor)
        if idx >= 0:
            start = max(0, idx - 160)
            break
    return compact[start : start + 900].replace("\ufeff", "").strip()


def build_inventory(repo_root: Path, max_files: int = 900) -> list[PromptCandidate]:
    rows = []
    for i, path in enumerate(_files(repo_root)):
        if i >= max_files:
            break
        text = _read(path)
        if not text:
            continue
        rel = path.relative_to(repo_root).as_posix()
        hits, score = _score(rel, text)
        if score <= 0 and "prompt" not in rel.lower():
            continue
        rows.append(
            PromptCandidate(
                rel,
                path.suffix.lower(),
                path.stat().st_size,
                _classify(rel, text.lower()),
                score,
                hits,
                _excerpt(text),
            )
        )
    return sorted(rows, key=lambda r: (r.score, r.rel_path), reverse=True)


def _write_inventory(path: Path, rows: list[PromptCandidate]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(
            h,
            fieldnames=[
                "rank",
                "rel_path",
                "suffix",
                "size_bytes",
                "source_kind",
                "score",
                "keyword_hits",
                "excerpt",
            ],
        )
        w.writeheader()
        for rank, r in enumerate(rows, 1):
            w.writerow(
                {
                    "rank": rank,
                    "rel_path": r.rel_path,
                    "suffix": r.suffix,
                    "size_bytes": r.size_bytes,
                    "source_kind": r.source_kind,
                    "score": r.score,
                    "keyword_hits": r.keyword_hits,
                    "excerpt": r.excerpt,
                }
            )


def _audit_md(rows: list[PromptCandidate]) -> str:
    out = [
        "# P164 — Historical Prompt Audit & Reference Rebuild",
        "",
        "## Decision",
        "",
        f"- `{PROMPT_SOURCE_ID_CURRENT}` is demoted to `CURRENT_RUNTIME_CONTRACT_REFERENCE`.",
        "- The final reference prompt must be rebuilt from historical/global prompt material.",
        "- P164 is review-only and does not modify the runtime prompt.",
        "",
        "## Top candidates",
        "",
    ]
    for i, r in enumerate(rows[:15], 1):
        out += [
            f"### {i}. `{r.rel_path}`",
            "",
            f"- kind: `{r.source_kind}`",
            f"- score: `{r.score}`",
            f"- hits: `{r.keyword_hits}`",
            "",
            "> " + r.excerpt[:1000],
            "",
        ]
    out += ["## Next", "", f"`{NEXT_STEP}`", ""]
    return "\n".join(out)


def _candidate_md(rows: list[PromptCandidate]) -> str:
    src = (
        "\n".join(
            f"- `{r.rel_path}` — {r.source_kind}, score={r.score}"
            for r in rows
            if r.source_kind != "CURRENT_RUNTIME_CONTRACT_REFERENCE"
        )
        or "- No historical source found."
    )
    return f"""# P164 — Reference Prompt Candidate V1 — REVIEW ONLY

## Source policy

- Current source `{PROMPT_SOURCE_ID_CURRENT}` is kept only as runtime/smoke contract reference.
- Historical/global prompt sources are the intended reference base.
- This file is not applied to runtime.

## Sources selected for review

{src}

## Prompt candidate

Tu es un assistant QAIC spécialisé dans l'analyse d'un portefeuille crypto à partir d'une capture écran, d'un texte copié ou d'un JSON local.

### Objectif global en plusieurs points

1. Extraire les positions visibles sans inventer de quantité, PRU, P&L ou devise manquante.
2. Vérifier ticker, nom actif, quantité, valeur, devise, exposition.
3. Identifier données manquantes, ambiguës, illisibles ou incohérentes.
4. Produire une synthèse opérateur claire.
5. Signaler concentration, exposition excessive, actif inconnu, incohérence de devise.
6. Préparer une décision humaine uniquement.
7. Retourner un JSON exploitable par MVP QAIC.

### Règles dures

- HUMAN_REVIEW_ONLY
- NO_AUTO_ORDER
- NO_AUTO_SIZING
- NO_BROKER_EXECUTION
- NO_GOOGLE_SHEETS_WRITE
- NO_PUBLIC_DEPLOY
- NO_APPS_SCRIPT_EXECUTION
- NO_CLASP_PUSH
- Ne jamais recommander d'achat/vente automatique.
- Ne jamais calculer de sizing réel.
- Ne jamais supposer une donnée absente.
- Si l'image est insuffisante, répondre `INSUFFICIENT_DATA`.

### Format JSON minimal attendu

```json
{{
  "prompt_source_id": "P164_REFERENCE_PROMPT_CANDIDATE_V1_REVIEW_ONLY",
  "input_mode": "IMAGE_OR_TEXT_OR_JSON",
  "image_used": true,
  "reference_currency": "USD",
  "reference_currency_status": "OK",
  "analysis_level": "PORTFOLIO_REVIEW",
  "decision_status": "REVIEW_REQUIRED",
  "human_final_decision": "NO_ACTION",
  "safety_status": "HUMAN_REVIEW_ONLY",
  "broker_action_allowed": false,
  "auto_order_allowed": false,
  "auto_sizing_allowed": false,
  "positions": [],
  "missing_data": [],
  "risk_flags": [],
  "operator_summary": "",
  "next_human_review_steps": []
}}
```

### Si données insuffisantes

Retourner `INSUFFICIENT_DATA`, `REVIEW_REQUIRED`, `NO_ACTION`, positions vides, et lister les données manquantes.

## P165 required

Review the historical source selection before any runtime replacement.
"""


def build_and_write_export(repo_root: Path, max_files: int = 900) -> dict:
    repo_root = repo_root.resolve()
    rows = build_inventory(repo_root, max_files=max_files)
    blockers = 0 if rows else 1
    stamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    out = repo_root / "05_EXPORTS" / f"P164_HISTORICAL_PROMPT_AUDIT_REFERENCE_REBUILD_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    inventory = out / "P164_HISTORICAL_PROMPT_INVENTORY.csv"
    audit = out / "P164_HISTORICAL_PROMPT_AUDIT_REPORT.md"
    candidate = out / "P164_REFERENCE_PROMPT_CANDIDATE_V1.md"
    decision = out / "P164_REFERENCE_REBUILD_DECISION.md"
    summary_file = out / "P164_SUMMARY.json"

    _write_inventory(inventory, rows)
    audit.write_text(_audit_md(rows), encoding="utf-8")
    candidate.write_text(_candidate_md(rows[:10]), encoding="utf-8")
    summary = {
        "STATUS": FINAL_STATUS if not blockers else "BLOCKED_P164_NO_PROMPT_CANDIDATES",
        "P164_STATUS": STATUS_READY if not blockers else "P164_BLOCKED_NO_PROMPT_CANDIDATES",
        "PROMPT_SOURCE_ID_CURRENT": PROMPT_SOURCE_ID_CURRENT,
        "P132_P133_DEMOTED_TO_RUNTIME_CONTRACT_ONLY": True,
        "PROMPT_RELATED_CANDIDATE_COUNT": len(rows),
        "HISTORICAL_PROMPT_CANDIDATE_COUNT": sum(1 for r in rows if "HISTORICAL" in r.source_kind),
        "REFERENCE_PROMPT_CANDIDATE_CREATED": not blockers,
        "REFERENCE_PROMPT_CANDIDATE_REVIEW_ONLY": True,
        "RUNTIME_PROMPT_MODIFIED": False,
        "APPLY_ALLOWED": False,
        "GOOGLE_SHEETS_WRITE": False,
        "PUBLIC_DEPLOY": False,
        "NO_APPS_SCRIPT_EXECUTION": True,
        "NO_CLASP_PUSH": True,
        "NO_BROKER": True,
        "NO_ORDER": True,
        "NO_SIZING": True,
        "BLOCKER_COUNT": blockers,
        "INVENTORY_FILE": str(inventory),
        "AUDIT_REPORT_FILE": str(audit),
        "REFERENCE_PROMPT_CANDIDATE_FILE": str(candidate),
        "DECISION_FILE": str(decision),
        "EXPORT_DIR": str(out),
        "NEXT": NEXT_STEP if not blockers else "MANUAL_PROMPT_SOURCE_PROVIDE_OR_STOP",
        "created_at_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
    }
    decision.write_text(
        f"""# P164 — Reference Rebuild Decision

`{summary["P164_STATUS"]}`

P132/P133 is not accepted as final prompt content. It is demoted to runtime contract reference only.

- Inventory: `{inventory}`
- Audit: `{audit}`
- Candidate: `{candidate}`
- Apply allowed: `{summary["APPLY_ALLOWED"]}`
- Runtime modified: `{summary["RUNTIME_PROMPT_MODIFIED"]}`
- Next: `{summary["NEXT"]}`
""",
        encoding="utf-8",
    )
    summary_file.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(summary["P164_STATUS"])
    for k in (
        "P132_P133_DEMOTED_TO_RUNTIME_CONTRACT_ONLY",
        "HISTORICAL_PROMPT_CANDIDATE_COUNT",
        "PROMPT_RELATED_CANDIDATE_COUNT",
        "REFERENCE_PROMPT_CANDIDATE_CREATED",
        "RUNTIME_PROMPT_MODIFIED",
        "APPLY_ALLOWED",
        "BLOCKER_COUNT",
        "EXPORT_DIR",
        "NEXT",
    ):
        print(f"{k.lower()}={summary[k]}")
    if blockers:
        raise RuntimeError("P164_NO_PROMPT_CANDIDATES")
    return summary


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", default=".")
    p.add_argument("--max-files", type=int, default=900)
    a = p.parse_args(argv)
    build_and_write_export(Path(a.repo_root), max_files=a.max_files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
