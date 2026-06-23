from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = (
    "MVP_QAIC_P132_MULTIMODAL_GEM_IMAGE_PROMPT_USD_CONTRACT_0_1_1_FRENCH_RESPONSE_JSON_STABLE_SAFE"
)

REFERENCE_CURRENCY = "USD"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "GEM_MULTIMODAL_IMAGE_INPUT_ALLOWED",
    "IMAGE_INCLUDED_IN_MAIN_PROMPT",
    "NO_PRELIMINARY_IMAGE_EXTRACTION_STEP",
    "IMAGE_USAGE_EVIDENCE_REQUIRED",
    "USD_REFERENCE_CURRENCY",
    "FRENCH_RESPONSE_VALUES_ALLOWED",
    "JSON_KEYS_STABLE_ENGLISH",
    "P133_COMPATIBLE_RESPONSE_FORMAT",
    "NO_MINIFIED_JSON_FOR_OPERATOR_REVIEW",
    "PRETTY_JSON_REQUIRED",
    "HUMAN_READABLE_SUMMARY_REQUIRED",
    "HUMAN_REVIEW_REQUIRED",
    "NO_INVENTED_PORTFOLIO_DATA",
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
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

OUTPUT_FILES = (
    "P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md",
    "P132_EXPECTED_GEM_OUTPUT_SCHEMA.json",
    "P132_COPY_PASTE_TEXT_OPTIONAL_TEMPLATE.md",
    "P132_IMAGE_ATTACHMENT_GUIDE.md",
    "P132_RESPONSE_IMAGE_USAGE_GATE_CHECKLIST.csv",
    "P132_REFERENCE_PROMPTS_CORRECTION_PLAN.md",
    "P132_TODAY_FUNCTIONAL_RUNBOOK.md",
    "P132_CONTRACT.json",
    "P132_MANIFEST.json",
    "P132_README.md",
)

P131_EXPORT_PATTERN = "P131_REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST_*"


@dataclass(frozen=True)
class MultimodalGemImagePromptUsdContractRequest:
    output_dir: str | Path
    exports_dir: str | Path | None = None
    p131_dir: str | Path | None = None
    run_id: str = "P132-MULTIMODAL-GEM-IMAGE-PROMPT-USD-CONTRACT"
    generated_at_utc: str | None = None
    notes: str | None = None


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def discover_p131_dirs(exports_dir: str | Path) -> list[Path]:
    root = Path(exports_dir)
    if not root.exists():
        return []
    candidates = [path for path in root.glob(P131_EXPORT_PATTERN) if path.is_dir()]
    return sorted(
        candidates,
        key=lambda path: (path.stat().st_mtime_ns, str(path)),
        reverse=True,
    )


def discover_latest_p131_dir(exports_dir: str | Path) -> Path | None:
    dirs = discover_p131_dirs(exports_dir)
    return dirs[0] if dirs else None


def _resolve_p131_dir(p131_dir: str | Path | None, exports_dir: Path | None) -> Path | None:
    if p131_dir:
        return Path(p131_dir)
    if exports_dir:
        return discover_latest_p131_dir(exports_dir)
    return None


def build_expected_gem_output_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": [
            "status",
            "source_type",
            "reference_currency",
            "image_used",
            "image_usage_evidence",
            "portfolio",
            "assets",
            "missing_data",
            "unclear_data",
            "human_review_required",
            "no_order_no_sizing",
        ],
        "properties": {
            "status": {"enum": ["OK", "REVIEW_REQUIRED", "BLOCKED"]},
            "source_type": {"enum": ["image", "copy_paste_text", "image_plus_text"]},
            "reference_currency": {"const": "USD"},
            "image_used": {"type": "boolean"},
            "copy_paste_text_used": {"type": "boolean"},
            "image_usage_evidence": {
                "type": "object",
                "required": [
                    "status",
                    "visual_evidence_summary",
                    "visible_platform_or_context",
                    "blockers",
                ],
                "properties": {
                    "status": {
                        "enum": ["IMAGE_USED", "IMAGE_NOT_USED_OR_NOT_EVIDENCED", "REVIEW_REQUIRED"]
                    },
                    "visual_evidence_summary": {"type": ["string", "null"]},
                    "visible_platform_or_context": {"type": ["string", "null"]},
                    "blockers": {"type": "array", "items": {"type": "string"}},
                },
            },
            "portfolio": {
                "type": "object",
                "required": [
                    "total_value_usd",
                    "unrealized_pnl_usd",
                    "unrealized_pnl_pct",
                    "cash_usd_value",
                    "cash_allocation_pct",
                ],
                "properties": {
                    "total_value_usd": {"type": ["number", "null"]},
                    "unrealized_pnl_usd": {"type": ["number", "null"]},
                    "unrealized_pnl_pct": {"type": ["number", "null"]},
                    "cash_usd_value": {"type": ["number", "null"]},
                    "cash_allocation_pct": {"type": ["number", "null"]},
                },
            },
            "assets": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "symbol",
                        "asset_name",
                        "quantity",
                        "price_usd",
                        "value_usd",
                        "allocation_pct",
                        "unrealized_pnl_usd",
                        "unrealized_pnl_pct",
                        "confidence",
                        "notes",
                    ],
                    "properties": {
                        "symbol": {"type": ["string", "null"]},
                        "asset_name": {"type": ["string", "null"]},
                        "quantity": {"type": ["number", "string", "null"]},
                        "price_usd": {"type": ["number", "null"]},
                        "value_usd": {"type": ["number", "null"]},
                        "allocation_pct": {"type": ["number", "null"]},
                        "unrealized_pnl_usd": {"type": ["number", "null"]},
                        "unrealized_pnl_pct": {"type": ["number", "null"]},
                        "confidence": {"enum": ["HIGH", "MEDIUM", "LOW", "REVIEW"]},
                        "notes": {"type": ["string", "null"]},
                    },
                },
            },
            "missing_data": {"type": "array", "items": {"type": "string"}},
            "unclear_data": {"type": "array", "items": {"type": "string"}},
            "human_review_required": {"const": True},
            "no_order_no_sizing": {"const": True},
        },
    }


def build_contract() -> dict[str, Any]:
    return {
        "contract": "P132_MULTIMODAL_GEM_IMAGE_PROMPT_USD_CONTRACT",
        "version": VERSION,
        "status": "MULTIMODAL_PROMPT_CONTRACT_READY",
        "reference_currency": REFERENCE_CURRENCY,
        "response_language": "fr",
        "json_keys_language": "en_stable",
        "human_readable_summary_required": True,
        "pretty_json_required": True,
        "no_minified_json_for_operator_review": True,
        "p133_compatible_response_format": True,
        "architecture_decision": "The Revolut X image is attached directly to the main GEM portfolio prompt. There is no separate preliminary image-reading step.",
        "allowed": [
            "attach Revolut X image directly in GEM",
            "paste optional Revolut X copied text in the same prompt",
            "ask GEM for one final structured portfolio review",
            "require proof that the image was used",
            "require USD output schema",
            "require human review before any use",
        ],
        "forbidden": [
            "separate first-pass GEM extraction as mandatory workflow",
            "invented_portfolio_data",
            "auto_apply_gem_response",
            "broker_execution",
            "order_execution",
            "auto_sizing",
            "apps_script_execution",
            "sheet_write",
            "clasp_push",
            "public_deploy",
            "revolutx_real_access_from_mvp",
        ],
        "safety_markers": list(SAFETY_MARKERS),
        "outputs": list(OUTPUT_FILES),
    }


def _prompt_text() -> str:
    schema = json.dumps(
        build_expected_gem_output_schema(), ensure_ascii=False, indent=2, sort_keys=True
    )
    return f"""
# P132 GEM Multimodal Portfolio Prompt — Revolut X / USD

## Input mode

You will receive:
1. One attached image/screenshot from Revolut X or a similar crypto portfolio interface.
2. Optional copied text from the same interface.

The image is part of this main prompt. Do not ask for or create a separate preliminary step where you only read the image. Perform the portfolio extraction and review in this single response.

## Langue de réponse

- Réponds en français pour tous les textes rédigés, explications, résumés, commentaires et notes.
- Conserve exactement les noms de champs JSON, les statuts techniques, les enums, les booléens et les marqueurs de sécurité définis dans le schéma.
- Ne traduis pas les clés JSON.
- Si la réponse est en JSON, les valeurs textuelles peuvent être en français, mais la structure technique doit rester strictement conforme au schéma.
- Les valeurs des enums techniques doivent rester exactes, par exemple `IMAGE_USED`, `REVIEW_REQUIRED`, `OK`, `BLOCKED`, `HIGH`, `MEDIUM`, `LOW`, `REVIEW`.

## Format de sortie obligatoire

- Commence par un bloc `## Résumé lisible` rédigé en français pour l’opérateur.
- Ensuite, fournis un bloc `## JSON strict pretty-printed`.
- Le JSON strict doit être dans un bloc fenced `json`.
- Le JSON doit être indenté sur plusieurs lignes avec 2 espaces.
- Ne produis pas de JSON minifié sur une seule ligne.
- Le JSON doit rester parseable par P133 sans correction manuelle.
- Les clés JSON doivent rester exactement en anglais et conformes au schéma existant.
- Les valeurs textuelles libres, `notes`, `visual_evidence_summary`, `missing_data` et `unclear_data` peuvent être en français.
- Ne mets aucun ordre, sizing, recommandation d’exécution ou instruction broker.
- Si tu dois ajouter du texte hors JSON, il doit rester strictement dans le résumé lisible et ne doit pas modifier le JSON.

Format attendu :

```markdown
## Résumé lisible

- Statut : REVIEW_REQUIRED
- Image utilisée : oui
- Devise : USD
- Total portefeuille : <valeur> USD
- Sécurité : human review, no order, no sizing, no auto apply

## JSON strict pretty-printed

```json
{{
  "status": "REVIEW_REQUIRED",
  "source_type": "image",
  "reference_currency": "USD",
  "image_used": true
}}
```
```

## Hard rules

<!-- P158_R5_PROMPT_PATCH_APPLIED_20260623 -->
### P158-R5 Runtime clarification patch

- Set `image_used` explicitly in the output payload: `true` when the screenshot or image is used as evidence, `false` only when no image evidence is available.
- Set `reference_currency` explicitly: use `USD` for the Revolut X / USD runtime prompt unless the provided interface or copied text proves another currency.
- When a field is uncertain, missing, or not visible, mark the uncertainty explicitly instead of silently omitting the field.
- Preserve the human-review-only stance: do not convert prompt observations into execution instructions, allocation instructions, or broker actions.
- Keep JSON field names, enum values, safety markers, and technical statuses exactly as specified by the runtime schema.
<!-- /P158_R5_PROMPT_PATCH_APPLIED_20260623 -->


- Reference currency is USD.
- Use `value_usd`, `price_usd`, `portfolio_total_value_usd`, and `cash_usd_value`.
- Do not use EUR unless an explicit FX conversion is provided.
- You may use the attached image and optional copied text.
- Do not invent missing values.
- If a value is unclear, set it to null and explain it in `unclear_data`.
- If you did not use the image or cannot prove you used it, return `status="REVIEW_REQUIRED"` and `image_usage_evidence.status="IMAGE_NOT_USED_OR_NOT_EVIDENCED"`.
- Human review is always required.
- No broker action, no order, no sizing, no auto-apply.

## Optional copied text from Revolut X

Paste copied text here if available:

```text
<PASTE_REVOLUT_X_COPY_TEXT_HERE>
```

## Required final answer

Return only valid JSON matching this schema:

```json
{schema}
```

## Required image usage proof

The JSON must include:
- `image_used`
- `image_usage_evidence.status`
- `image_usage_evidence.visual_evidence_summary`
- `image_usage_evidence.visible_platform_or_context`

If the image is not visible, not attached, or not used, the response must be `REVIEW_REQUIRED`.

## Decision support boundaries

You may summarize risk and missing data.
You must not recommend execution.
You must not place or prepare an order.
You must not determine real sizing.
"""


def _copy_paste_template() -> str:
    return """
# P132 Optional Revolut X Copy-Paste Text Template

Use this only if Revolut X lets you copy visible portfolio text.

Paste raw interface text below. Do not edit numbers silently.

```text
<PASTE_RAW_REVOLUT_X_TEXT_HERE>
```

Reference currency: USD.

Human review remains required.
"""


def _image_attachment_guide() -> str:
    return """
# P132 Image Attachment Guide

Attach the Revolut X screenshot/image directly to GEM with the P132 prompt.

Do not run a separate preliminary OCR/extraction prompt.
The image is part of the main GEM portfolio prompt.

Expected control in final GEM response:
- image_used=true
- image_usage_evidence.status="IMAGE_USED"
- visual_evidence_summary is not empty
- reference_currency="USD"

If not, block or review.
"""


def _write_gate_checklist(path: Path) -> None:
    rows = [
        ("1", "GEM final answer is valid JSON", "REQUIRED", "JSON_VALIDATION", "BLOCK_IF_FAIL"),
        ("2", "reference_currency is USD", "REQUIRED", "USD_REFERENCE_CURRENCY", "BLOCK_IF_FAIL"),
        ("3", "image_used is true", "REQUIRED", "IMAGE_USAGE_EVIDENCE_REQUIRED", "BLOCK_IF_FAIL"),
        (
            "4",
            "image_usage_evidence.status is IMAGE_USED",
            "REQUIRED",
            "IMAGE_NOT_USED_OR_NOT_EVIDENCED",
            "BLOCK_IF_FAIL",
        ),
        (
            "5",
            "visual_evidence_summary is present",
            "REQUIRED",
            "IMAGE_USAGE_EVIDENCE_REQUIRED",
            "REVIEW_IF_MISSING",
        ),
        ("6", "assets use value_usd and price_usd", "REQUIRED", "USD_FIELDS", "BLOCK_IF_FAIL"),
        (
            "7",
            "human_review_required is true",
            "REQUIRED",
            "HUMAN_REVIEW_REQUIRED",
            "BLOCK_IF_FAIL",
        ),
        ("8", "no_order_no_sizing is true", "REQUIRED", "NO_BROKER_ORDER_SIZING", "BLOCK_IF_FAIL"),
        (
            "9",
            "missing/unclear values are explicit",
            "REQUIRED",
            "NO_INVENTED_PORTFOLIO_DATA",
            "REVIEW_IF_MISSING",
        ),
    ]
    fields = ["step", "check", "required", "safety_or_gate", "action_if_fail"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "step": row[0],
                    "check": row[1],
                    "required": row[2],
                    "safety_or_gate": row[3],
                    "action_if_fail": row[4],
                }
            )


def _reference_prompts_correction_plan() -> str:
    return """
# P132 Reference Prompts Correction Plan

## Question: when do we correct the current main GEM reference prompts?

We do it in two phases.

### Phase A — Today functional version

P132 is the functional layer for today's test:
- one multimodal GEM prompt,
- image attached directly to the main prompt,
- optional Revolut X copied text,
- USD as reference currency,
- output JSON schema,
- image usage evidence gate.

This avoids blocking today's test on a risky global refactor.

### Phase B — Controlled reference prompt sync

After P132/P133 are validated with one real GEM response, patch the existing reference prompts in a controlled batch:
- identify current GEM principal prompt files,
- replace EUR-centric fields with USD-centric fields,
- add image attachment language,
- add image_usage_evidence requirement,
- add no-order/no-sizing/no-auto-apply constraints,
- keep backward compatibility wrappers where needed,
- run tests and export a prompt diff report.

Recommended next:
- P133: GEM response capture and image usage gate.
- P134: Reference prompt inventory + patch plan read-only.
- P135: Apply reference prompt sync if P133 real response passes.
"""


def _today_runbook() -> str:
    return """
# P132 Today Functional Runbook

## Goal today

Get a functional real GEM test today without another pre-extraction step.

## Steps

1. Open `P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md`.
2. Attach the Revolut X screenshot/image directly in GEM.
3. Paste optional Revolut X copied text in the prompt.
4. Ask GEM to answer only with the required JSON.
5. Save GEM response for P133.
6. Check:
   - `image_used=true`
   - `image_usage_evidence.status="IMAGE_USED"`
   - `reference_currency="USD"`
   - assets contain `value_usd`
   - `human_review_required=true`
   - `no_order_no_sizing=true`
   - les valeurs textuelles rédigées sont en français
   - les clés JSON restent inchangées en anglais
   - le JSON strict est pretty-printed et non minifié
   - un résumé lisible en français précède le JSON strict

## Block if

- GEM did not mention evidence from the image.
- GEM used EUR without explicit conversion.
- GEM invented missing values.
- GEM suggests an order, broker action, or sizing.
"""


def _readme() -> str:
    return """
# P132 Multimodal GEM Image Prompt USD Contract

P132 delivers the functional prompt pack for today.

Architecture:
- Image attached directly to the main GEM prompt.
- Optional Revolut X copied text in same prompt.
- No separate preliminary image extraction step.
- USD reference currency.
- Final response must prove image usage.
- Human review required.
"""


def write_multimodal_gem_image_prompt_usd_contract(
    request: MultimodalGemImagePromptUsdContractRequest,
) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    exports_dir = Path(request.exports_dir) if request.exports_dir else None
    p131_dir = _resolve_p131_dir(request.p131_dir, exports_dir)

    prompt_path = out / "P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md"
    schema_path = out / "P132_EXPECTED_GEM_OUTPUT_SCHEMA.json"
    copy_template_path = out / "P132_COPY_PASTE_TEXT_OPTIONAL_TEMPLATE.md"
    image_guide_path = out / "P132_IMAGE_ATTACHMENT_GUIDE.md"
    checklist_path = out / "P132_RESPONSE_IMAGE_USAGE_GATE_CHECKLIST.csv"
    correction_plan_path = out / "P132_REFERENCE_PROMPTS_CORRECTION_PLAN.md"
    today_runbook_path = out / "P132_TODAY_FUNCTIONAL_RUNBOOK.md"
    contract_path = out / "P132_CONTRACT.json"
    manifest_path = out / "P132_MANIFEST.json"
    readme_path = out / "P132_README.md"

    _write(prompt_path, _prompt_text())
    _write_json(schema_path, build_expected_gem_output_schema())
    _write(copy_template_path, _copy_paste_template())
    _write(image_guide_path, _image_attachment_guide())
    _write_gate_checklist(checklist_path)
    _write(correction_plan_path, _reference_prompts_correction_plan())
    _write(today_runbook_path, _today_runbook())
    _write_json(contract_path, build_contract())
    _write(readme_path, _readme())

    manifest = {
        "status": "MULTIMODAL_GEM_IMAGE_PROMPT_USD_CONTRACT_READY",
        "step": "P132_MULTIMODAL_GEM_IMAGE_PROMPT_USD_CONTRACT",
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": request.generated_at_utc,
        "output_dir": str(out),
        "exports_dir": str(exports_dir) if exports_dir else None,
        "p131_dir": str(p131_dir) if p131_dir else None,
        "p131_dir_valid": bool(p131_dir and str(p131_dir) != "G" and p131_dir.exists()),
        "reference_currency": REFERENCE_CURRENCY,
        "response_language": "fr",
        "json_keys_language": "en_stable",
        "french_response_values_allowed": True,
        "json_keys_stable_english": True,
        "human_readable_summary_required": True,
        "pretty_json_required": True,
        "no_minified_json_for_operator_review": True,
        "p133_compatible_response_format": True,
        "gem_multimodal_image_input_allowed": True,
        "image_included_in_main_prompt": True,
        "no_preliminary_image_extraction_step": True,
        "image_usage_evidence_required": True,
        "functional_today": True,
        "reference_prompt_patch_strategy": "P132 functional pack now, then P134 inventory and P135 controlled sync after P133 real response gate.",
        "human_review_required": True,
        "no_invented_portfolio_data": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "no_order_no_sizing": True,
        "safety_markers": list(SAFETY_MARKERS),
        "files": [
            str(prompt_path),
            str(schema_path),
            str(copy_template_path),
            str(image_guide_path),
            str(checklist_path),
            str(correction_plan_path),
            str(today_runbook_path),
            str(contract_path),
            str(readme_path),
        ],
        "next": "P133_GEM_MULTIMODAL_RESPONSE_CAPTURE_AND_IMAGE_USAGE_GATE",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.multimodal_gem_image_prompt_usd_contract",
        description="Create P132 multimodal GEM image prompt USD contract pack.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--exports-dir")
    parser.add_argument("--p131-dir")
    parser.add_argument("--run-id", default="P132-MULTIMODAL-GEM-IMAGE-PROMPT-USD-CONTRACT")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(
            output_dir=args.output_dir,
            exports_dir=args.exports_dir,
            p131_dir=args.p131_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["functional_today"])
    print(result["image_included_in_main_prompt"])
    print(result["image_usage_evidence_required"])
    print(result["reference_currency"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
