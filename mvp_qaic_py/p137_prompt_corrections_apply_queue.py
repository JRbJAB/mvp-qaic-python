from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p136_p133_real_response_file_import import (
    DEFAULT_GEM_ID,
    get_active_gem_ids,
    get_active_gem_profiles,
    validate_gem_id,
)


P137_VERSION = "MVP_QAIC_P137_PROMPT_CORRECTIONS_APPLY_QUEUE_20260622"
DEFAULT_RUN_ID = "P137-PROMPT-CORRECTIONS-APPLY-QUEUE"

SAFETY_MARKERS: tuple[str, ...] = (
    "LOCAL_PRIVATE_ONLY",
    "P137_PROMPT_CORRECTIONS_APPLY_QUEUE",
    "PROMPT_CORRECTIONS_LOCAL_DRAFT_ONLY",
    "NO_PROMPT_SOURCE_OVERWRITE",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_PUBLIC_DEPLOY",
    "NO_TUNNEL",
    "NO_REMOTE_ACCESS",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_SIZING",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    "NO_SHEET_WRITE",
    "NO_BIGQUERY_WRITE",
    "HUMAN_REVIEW_REQUIRED",
    "P133_COMPATIBLE",
)


@dataclass(frozen=True)
class P137Request:
    output_dir: Path = Path("05_EXPORTS/P137_PROMPT_CORRECTIONS_APPLY_QUEUE")
    exports_dir: Path = Path("05_EXPORTS")
    prompt_file: Path | None = None
    gem_id: str = DEFAULT_GEM_ID
    run_id: str = DEFAULT_RUN_ID
    generated_at_utc: str | None = None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _find_latest_prompt(exports_dir: Path) -> Path | None:
    if not exports_dir.exists():
        return None

    patterns = (
        "P134_LATEST_P132_PROMPT_COPY.md",
        "P132*PROMPT*.md",
        "*GEM*PROMPT*.md",
        "*PROMPT*.md",
    )
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(path for path in exports_dir.rglob(pattern) if path.is_file())

    if not candidates:
        return None

    return max(candidates, key=lambda path: path.stat().st_mtime)


def _fallback_prompt(gem_id: str) -> str:
    return f"""# MVP QAIC — GEM Portfolio Prompt Base

Gem cible: {gem_id}

Prompt source non trouvé automatiquement. Utiliser ce fichier comme base temporaire, puis remplacer par le dernier prompt P132/P134 validé.

Objectif: analyser une capture Revolut X / portefeuille crypto en mode éducatif, analytique, human review only.

Sécurité:
- no broker
- no order
- no sizing
- no auto apply
"""


def load_source_prompt(request: P137Request) -> tuple[str, Path | None]:
    selected = request.prompt_file or _find_latest_prompt(request.exports_dir)
    if selected and selected.exists():
        return _read_text(selected), selected
    return _fallback_prompt(request.gem_id), None


def build_prompt_corrections_queue(gem_profile: dict[str, Any]) -> list[dict[str, Any]]:
    gem_id = gem_profile["gem_id"]
    return [
        {
            "correction_id": "P137_GEM_001",
            "priority": "HIGH",
            "status": "APPLIED_TO_LOCAL_DRAFT",
            "scope": "OUTPUT_FORMAT",
            "issue": "La réponse GEM doit être lisible humainement puis fournir un JSON pretty fenced.",
            "applied_rule": "Imposer un résumé court puis un bloc ```json strict.",
            "gem_id": gem_id,
        },
        {
            "correction_id": "P137_GEM_002",
            "priority": "HIGH",
            "status": "APPLIED_TO_LOCAL_DRAFT",
            "scope": "IMAGE_USAGE_EVIDENCE",
            "issue": "La preuve d'utilisation de l'image doit être explicite.",
            "applied_rule": "Ajouter `image_used` et `image_usage_evidence` obligatoires.",
            "gem_id": gem_id,
        },
        {
            "correction_id": "P137_GEM_003",
            "priority": "HIGH",
            "status": "APPLIED_TO_LOCAL_DRAFT",
            "scope": "USD_REFERENCE",
            "issue": "La devise de référence doit rester verrouillée sur USD pour Revolut X.",
            "applied_rule": "Ajouter `reference_currency=USD` et champs `*_usd`.",
            "gem_id": gem_id,
        },
        {
            "correction_id": "P137_GEM_004",
            "priority": "HIGH",
            "status": "APPLIED_TO_LOCAL_DRAFT",
            "scope": "SAFETY_GUARDS",
            "issue": "Le GEM ne doit jamais produire d'ordre, sizing ou auto-apply.",
            "applied_rule": "Exiger `no_order_no_sizing=true`, `human_review_required=true`.",
            "gem_id": gem_id,
        },
        {
            "correction_id": "P137_GEM_005",
            "priority": "HIGH",
            "status": "APPLIED_TO_LOCAL_DRAFT",
            "scope": "MISSING_DATA",
            "issue": "Les données manquantes doivent bloquer ou passer en review, jamais être inventées.",
            "applied_rule": "Ajouter `missing_data`, `blockers`, `status=REVIEW_REQUIRED|BLOCKED`.",
            "gem_id": gem_id,
        },
        {
            "correction_id": "P137_GEM_006",
            "priority": "MEDIUM",
            "status": "APPLIED_TO_LOCAL_DRAFT",
            "scope": "P133_COMPATIBILITY",
            "issue": "La sortie GEM doit rester compatible avec la gate P133.",
            "applied_rule": "Ajouter marqueurs et clés attendus par capture gate.",
            "gem_id": gem_id,
        },
        {
            "correction_id": "P137_GEM_007",
            "priority": "MEDIUM",
            "status": "APPLIED_TO_LOCAL_DRAFT",
            "scope": "GEM_RUNTIME_PROFILE",
            "issue": "La correction doit tenir compte du GEM actif.",
            "applied_rule": "Injecter `gem_id`, `prompt_profile`, capacités et limites dans l'en-tête.",
            "gem_id": gem_id,
        },
    ]


def build_output_contract(gem_profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_id": "P137_GEM_OUTPUT_CONTRACT",
        "gem_id": gem_profile["gem_id"],
        "prompt_profile": gem_profile["prompt_profile"],
        "language": "fr",
        "required_response_shape": {
            "human_summary_first": True,
            "json_fenced_block_required": True,
            "json_pretty_required": True,
            "technical_keys_keep_english": True,
        },
        "required_json_keys": [
            "status",
            "gem_id",
            "prompt_profile",
            "reference_currency",
            "image_used",
            "image_usage_evidence",
            "portfolio_extract",
            "missing_data",
            "blockers",
            "human_review_required",
            "no_order_no_sizing",
            "safety",
        ],
        "required_enums": {
            "status": ["OK", "REVIEW_REQUIRED", "BLOCKED"],
            "image_used": ["IMAGE_USED", "IMAGE_NOT_USED", "REVIEW_REQUIRED"],
            "risk_level": ["LOW", "MEDIUM", "HIGH", "REVIEW"],
        },
        "hard_safety": {
            "human_review_required": True,
            "no_order_no_sizing": True,
            "no_broker_execution": True,
            "no_auto_apply": True,
            "no_invented_portfolio_data": True,
        },
    }


def build_corrected_prompt(
    source_prompt: str,
    gem_profile: dict[str, Any],
    generated_at_utc: str,
) -> str:
    contract = build_output_contract(gem_profile)
    correction_header = f"""# P137 — GEM Prompt Corrections Overlay

Version: {P137_VERSION}
Generated at UTC: {generated_at_utc}
Gem actif: {gem_profile["gem_id"]}
Prompt profile: {gem_profile["prompt_profile"]}
Mode: HUMAN_REVIEW_ONLY / LOCAL_PRIVATE_ONLY

## Corrections appliquées au brouillon local

1. Réponse en français, mais clés JSON/enums techniques en anglais.
2. Résumé humain court avant le JSON.
3. Bloc final obligatoire fenced `json`, pretty printed.
4. Preuve d'utilisation de l'image obligatoire: `image_used` + `image_usage_evidence`.
5. Devise de référence verrouillée: `reference_currency="USD"`.
6. Aucun ordre, aucun sizing, aucun auto-apply.
7. Données manquantes explicites: `missing_data`, `blockers`.
8. Si doute image/données/prix: `status="REVIEW_REQUIRED"` ou `status="BLOCKED"`.
9. Compatibilité P133: conserver `human_review_required=true` et `no_order_no_sizing=true`.

## Contrat de sortie obligatoire

```json
{json.dumps(contract, ensure_ascii=False, indent=2)}
```

## Réponse attendue

Structure obligatoire:

```text
## Résumé opérateur

<5 à 12 lignes en français, orientées human review.>

## Points de contrôle

- Image utilisée: <preuve courte>
- Devise: USD
- Données manquantes: <liste courte>
- Blockers: <liste courte>
- Sécurité: no order / no sizing / human review

```json
{{
  "status": "REVIEW_REQUIRED",
  "gem_id": "{gem_profile["gem_id"]}",
  "prompt_profile": "{gem_profile["prompt_profile"]}",
  "reference_currency": "USD",
  "image_used": "IMAGE_USED",
  "image_usage_evidence": "Décrire exactement les éléments visibles dans la capture utilisée.",
  "portfolio_extract": {{
    "positions": [],
    "total_value_usd": null,
    "cash_usd": null
  }},
  "missing_data": [],
  "blockers": [],
  "human_review_required": true,
  "no_order_no_sizing": true,
  "safety": {{
    "no_broker_execution": true,
    "no_order": true,
    "no_sizing": true,
    "no_auto_apply": true,
    "no_invented_portfolio_data": true
  }}
}}
```
```

---

# Prompt source

"""
    return correction_header.rstrip() + "\n\n" + source_prompt.strip() + "\n"


def build_p137_payload(request: P137Request) -> dict[str, Any]:
    generated_at = request.generated_at_utc or _utc_now_iso()
    gem_profile = validate_gem_id(request.gem_id)
    source_prompt, source_path = load_source_prompt(request)
    corrected_prompt = build_corrected_prompt(source_prompt, gem_profile, generated_at)
    queue = build_prompt_corrections_queue(gem_profile)
    contract = build_output_contract(gem_profile)

    return {
        "step": "P137_PROMPT_CORRECTIONS_APPLY_QUEUE",
        "version": P137_VERSION,
        "status": "P137_PROMPT_CORRECTIONS_READY_FOR_HUMAN_REVIEW",
        "generated_at_utc": generated_at,
        "run_id": request.run_id,
        "selected_gem": gem_profile,
        "active_gem_ids": get_active_gem_ids(),
        "active_gem_profiles": get_active_gem_profiles(),
        "source_prompt": {
            "path": str(source_path) if source_path else None,
            "found": source_path is not None,
            "sha256": _sha256_text(source_prompt),
            "char_count": len(source_prompt),
        },
        "corrected_prompt": {
            "output_file": str(request.output_dir / "P137_CORRECTED_GEM_PROMPT.md"),
            "sha256": _sha256_text(corrected_prompt),
            "char_count": len(corrected_prompt),
            "local_draft_only": True,
            "source_overwritten": False,
        },
        "prompt_corrections_queue": queue,
        "output_contract": contract,
        "safety_markers": list(SAFETY_MARKERS),
        "features": {
            "prompt_corrections_apply_queue": True,
            "corrected_prompt_local_draft": True,
            "source_prompt_copy_exported": True,
            "no_prompt_source_overwrite": True,
            "p133_compatible": True,
            "human_review_required": True,
            "no_broker_execution": True,
            "no_order": True,
            "no_sizing": True,
            "no_auto_apply": True,
        },
    }


def _write_queue_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# P137 — Prompt Corrections Apply Queue",
        "",
        f"Status: `{payload['status']}`",
        f"Selected GEM: `{payload['selected_gem']['gem_id']}`",
        "",
        "| correction_id | priority | status | scope | issue | applied_rule |",
        "|---|---:|---|---|---|---|",
    ]
    for row in payload["prompt_corrections_queue"]:
        lines.append(
            "| {correction_id} | {priority} | {status} | {scope} | {issue} | {applied_rule} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Sécurité",
            "",
            "- Brouillon local uniquement.",
            "- Aucune modification du prompt source.",
            "- Human review obligatoire avant usage stable.",
            "- Aucun broker, ordre, sizing, auto-apply.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_contract_md(path: Path, payload: dict[str, Any]) -> None:
    contract = payload["output_contract"]
    lines = [
        "# P137 — GEM Output Contract",
        "",
        f"Contract: `{contract['contract_id']}`",
        f"Gem: `{contract['gem_id']}`",
        f"Prompt profile: `{contract['prompt_profile']}`",
        "",
        "## Required JSON keys",
        "",
    ]
    lines.extend(f"- `{key}`" for key in contract["required_json_keys"])
    lines.extend(
        [
            "",
            "## Hard safety",
            "",
        ]
    )
    lines.extend(f"- `{key}`: `{value}`" for key, value in contract["hard_safety"].items())
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_runbook(path: Path, payload: dict[str, Any]) -> None:
    text = f"""# P137 — Prompt Corrections Apply Queue

## Objectif

Créer un prompt GEM corrigé localement, compatible P133, sans écraser le prompt source.

## Résultat

- Status: `{payload["status"]}`
- GEM: `{payload["selected_gem"]["gem_id"]}`
- Prompt source trouvé: `{payload["source_prompt"]["found"]}`
- Prompt corrigé: `{payload["corrected_prompt"]["output_file"]}`

## Fichiers

- `P137_CORRECTED_GEM_PROMPT.md`
- `P137_SOURCE_PROMPT_COPY.md`
- `P137_PROMPT_CORRECTIONS_QUEUE.json`
- `P137_PROMPT_CORRECTIONS_QUEUE.md`
- `P137_GEM_OUTPUT_CONTRACT.json`
- `P137_GEM_OUTPUT_CONTRACT.md`

## Garde-fous

- Local draft only.
- No prompt source overwrite.
- Human review required.
- No broker, no order, no sizing, no auto apply.
"""
    path.write_text(text, encoding="utf-8")


def write_p137_prompt_pack(request: P137Request) -> dict[str, Any]:
    _ensure_dir(request.output_dir)
    payload = build_p137_payload(request)

    source_prompt, _ = load_source_prompt(request)
    corrected_prompt = build_corrected_prompt(
        source_prompt,
        payload["selected_gem"],
        payload["generated_at_utc"],
    )

    (request.output_dir / "P137_REAL_RESPONSE_FILE_IMPORT_NOTE.md").write_text(
        "P137 corrige le prompt GEM. L'import réponse GEM réelle reste géré par P136/P133.\n",
        encoding="utf-8",
    )
    (request.output_dir / "P137_SOURCE_PROMPT_COPY.md").write_text(source_prompt, encoding="utf-8")
    (request.output_dir / "P137_CORRECTED_GEM_PROMPT.md").write_text(
        corrected_prompt, encoding="utf-8"
    )
    (request.output_dir / "P137_PROMPT_CORRECTIONS_APPLY_PAYLOAD.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    (request.output_dir / "P137_PROMPT_CORRECTIONS_QUEUE.json").write_text(
        json.dumps(payload["prompt_corrections_queue"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_queue_md(request.output_dir / "P137_PROMPT_CORRECTIONS_QUEUE.md", payload)
    (request.output_dir / "P137_GEM_OUTPUT_CONTRACT.json").write_text(
        json.dumps(payload["output_contract"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_contract_md(request.output_dir / "P137_GEM_OUTPUT_CONTRACT.md", payload)
    _write_runbook(request.output_dir / "P137_RUNBOOK.md", payload)

    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P137 GEM prompt corrections apply queue")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("05_EXPORTS/P137_PROMPT_CORRECTIONS_APPLY_QUEUE")
    )
    parser.add_argument("--exports-dir", type=Path, default=Path("05_EXPORTS"))
    parser.add_argument("--prompt-file", type=Path, default=None)
    parser.add_argument("--gem-id", choices=get_active_gem_ids(), default=DEFAULT_GEM_ID)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--generated-at-utc", default=None)
    parser.add_argument("--dry-run-export", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    request = P137Request(
        output_dir=args.output_dir,
        exports_dir=args.exports_dir,
        prompt_file=args.prompt_file,
        gem_id=args.gem_id,
        run_id=args.run_id,
        generated_at_utc=args.generated_at_utc,
    )
    payload = write_p137_prompt_pack(request)
    print(payload["status"])
    print(payload["selected_gem"]["gem_id"])
    print(payload["corrected_prompt"]["output_file"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
