from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P133_GEM_MULTIMODAL_RESPONSE_CAPTURE_GATE_0_1_0_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "HUMAN_REVIEW_REQUIRED",
    "GEM_RESPONSE_CAPTURE_ONLY",
    "IMAGE_USAGE_EVIDENCE_REQUIRED",
    "REFERENCE_CURRENCY_USD",
    "JSON_KEYS_STABLE_ENGLISH",
    "FRENCH_HUMAN_READABLE_REPORT",
    "PRETTY_JSON_REQUIRED",
    "NO_MINIFIED_JSON_FOR_OPERATOR_REVIEW",
    "NO_BROKER",
    "NO_ORDER",
    "NO_CANCEL",
    "NO_SIZING",
    "NO_AUTO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    "NO_SHEET_WRITE",
)

REQUIRED_TOP_LEVEL_KEYS = (
    "status",
    "source_type",
    "reference_currency",
    "image_used",
    "copy_paste_text_used",
    "image_usage_evidence",
    "portfolio",
    "assets",
    "missing_data",
    "unclear_data",
    "human_review_required",
    "no_order_no_sizing",
)

REQUIRED_IMAGE_EVIDENCE_KEYS = (
    "status",
    "visual_evidence_summary",
    "visible_platform_or_context",
    "blockers",
)

REQUIRED_PORTFOLIO_KEYS = (
    "total_value_usd",
    "unrealized_pnl_usd",
    "unrealized_pnl_pct",
    "cash_usd_value",
    "cash_allocation_pct",
)

REQUIRED_ASSET_KEYS = (
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
)


@dataclass(frozen=True)
class GemMultimodalResponseGateRequest:
    response_text_path: Path
    output_dir: Path
    run_id: str = "P133-GEM-MULTIMODAL-RESPONSE-CAPTURE-GATE"
    generated_at_utc: str | None = None
    source_image_path: Path | None = None
    tolerance_value_usd: float = 0.02
    tolerance_allocation_pct: float = 0.02
    tolerance_pnl_usd: float = 0.02


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_response_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"GEM response file not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"GEM response file is empty: {path}")
    return text


def extract_json_text(response_text: str) -> tuple[str, list[str]]:
    """Extract JSON from raw GEM response.

    Accepts raw JSON, fenced json blocks, or text around a JSON object.
    """

    warnings: list[str] = []
    text = response_text.strip()

    if "```" in text:
        parts = text.split("```")
        candidates = []
        for part in parts:
            cleaned = part.strip()
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()
            if cleaned.startswith("{") and cleaned.endswith("}"):
                candidates.append(cleaned)
        if candidates:
            return candidates[0], warnings
        warnings.append("FENCED_BLOCK_PRESENT_BUT_JSON_NOT_ISOLATED")

    if text.startswith("{") and text.endswith("}"):
        return text, warnings

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        warnings.append("JSON_EXTRACTED_FROM_SURROUNDING_TEXT")
        return text[start : end + 1], warnings

    raise ValueError("No JSON object found in GEM response text")


def parse_gem_response(response_text: str) -> tuple[dict[str, Any], list[str], str]:
    json_text, warnings = extract_json_text(response_text)
    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid GEM JSON response: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("GEM JSON response must be an object")
    return payload, warnings, json_text


def _is_number(value: Any) -> bool:
    return (
        isinstance(value, int | float)
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    if _is_number(value):
        return float(value)
    return None


def _round2(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value + 0.0, 2)


def _compact_json_likely(json_text: str) -> bool:
    stripped = json_text.strip()
    if "\n" in stripped:
        return False
    return len(stripped) > 240 and stripped.startswith("{") and stripped.endswith("}")


def _json_keys_language_check(payload: dict[str, Any]) -> list[str]:
    forbidden = {
        "statut",
        "type_source",
        "devise_reference",
        "image_utilisee",
        "portefeuille",
        "actifs",
        "valeur_usd",
        "prix_usd",
        "allocation_pourcentage",
    }
    return sorted(key for key in payload if key in forbidden)


def _missing_keys(obj: dict[str, Any], required: tuple[str, ...], prefix: str) -> list[str]:
    return [f"{prefix}.{key}" for key in required if key not in obj]


def validate_payload(
    payload: dict[str, Any],
    json_text: str,
    *,
    tolerance_value_usd: float = 0.02,
    tolerance_allocation_pct: float = 0.02,
    tolerance_pnl_usd: float = 0.02,
) -> dict[str, Any]:
    failures: list[str] = []
    advisory: list[str] = []
    warnings: list[str] = []

    failures.extend(_missing_keys(payload, REQUIRED_TOP_LEVEL_KEYS, "root"))

    if payload.get("status") != "REVIEW_REQUIRED":
        failures.append("status_not_review_required")
    if payload.get("reference_currency") != "USD":
        failures.append("reference_currency_not_usd")
    if payload.get("source_type") != "image":
        failures.append("source_type_not_image")
    if payload.get("image_used") is not True:
        failures.append("image_used_not_true")
    if payload.get("human_review_required") is not True:
        failures.append("human_review_required_not_true")
    if payload.get("no_order_no_sizing") is not True:
        failures.append("no_order_no_sizing_not_true")

    image_evidence = payload.get("image_usage_evidence")
    if not isinstance(image_evidence, dict):
        failures.append("image_usage_evidence_missing_or_not_object")
        image_evidence = {}
    else:
        failures.extend(
            _missing_keys(image_evidence, REQUIRED_IMAGE_EVIDENCE_KEYS, "image_usage_evidence")
        )
        if image_evidence.get("status") != "IMAGE_USED":
            failures.append("image_usage_evidence_status_not_image_used")

    blockers = image_evidence.get("blockers") if isinstance(image_evidence, dict) else []
    if not isinstance(blockers, list):
        failures.append("image_usage_evidence_blockers_not_list")
        blockers = []

    required_blockers = {"HUMAN_REVIEW_REQUIRED", "NO_BROKER", "NO_ORDER", "NO_SIZING"}
    missing_blockers = sorted(required_blockers - {str(item) for item in blockers})
    if missing_blockers:
        failures.append("missing_required_safety_blockers:" + ",".join(missing_blockers))

    if "NO_AUTO_APPLY" not in {str(item) for item in blockers}:
        advisory.append("NO_AUTO_APPLY_missing_from_blockers")

    if "no_auto_apply" not in payload:
        advisory.append("no_auto_apply_root_field_missing_future_schema_recommendation")
    elif payload.get("no_auto_apply") is not True:
        failures.append("no_auto_apply_root_field_not_true")

    portfolio = payload.get("portfolio")
    if not isinstance(portfolio, dict):
        failures.append("portfolio_missing_or_not_object")
        portfolio = {}
    else:
        failures.extend(_missing_keys(portfolio, REQUIRED_PORTFOLIO_KEYS, "portfolio"))

    assets = payload.get("assets")
    if not isinstance(assets, list) or not assets:
        failures.append("assets_missing_empty_or_not_list")
        assets = []

    asset_rows: list[dict[str, Any]] = []
    for idx, asset in enumerate(assets):
        if not isinstance(asset, dict):
            failures.append(f"assets[{idx}]_not_object")
            continue
        failures.extend(_missing_keys(asset, REQUIRED_ASSET_KEYS, f"assets[{idx}]"))
        asset_rows.append(asset)

    total_value = _as_float(portfolio.get("total_value_usd"))
    total_pnl = _as_float(portfolio.get("unrealized_pnl_usd"))

    asset_value_sum = sum(_as_float(asset.get("value_usd")) or 0.0 for asset in asset_rows)
    allocation_sum = sum(_as_float(asset.get("allocation_pct")) or 0.0 for asset in asset_rows)
    pnl_sum = sum(
        _as_float(asset.get("unrealized_pnl_usd")) or 0.0
        for asset in asset_rows
        if _as_float(asset.get("unrealized_pnl_usd")) is not None
    )

    value_delta = None if total_value is None else round(asset_value_sum - total_value, 6)
    allocation_delta = round(allocation_sum - 100.0, 6)
    pnl_delta = None if total_pnl is None else round(pnl_sum - total_pnl, 6)

    if total_value is None:
        failures.append("portfolio.total_value_usd_not_numeric")
    elif abs(value_delta or 0.0) > tolerance_value_usd:
        failures.append("asset_value_sum_mismatch")

    if abs(allocation_delta) > tolerance_allocation_pct:
        failures.append("allocation_sum_not_100_pct")

    if total_pnl is None:
        advisory.append("portfolio.unrealized_pnl_usd_missing_or_null")
    elif abs(pnl_delta or 0.0) > tolerance_pnl_usd:
        failures.append("asset_pnl_sum_mismatch")

    forbidden_keys = _json_keys_language_check(payload)
    if forbidden_keys:
        failures.append("translated_json_keys_detected:" + ",".join(forbidden_keys))

    if _compact_json_likely(json_text):
        advisory.append("gem_response_json_minified_single_line_operator_unfriendly")

    if not isinstance(payload.get("missing_data"), list):
        failures.append("missing_data_not_list")
    if not isinstance(payload.get("unclear_data"), list):
        failures.append("unclear_data_not_list")

    final_status = "PASS_WITH_HUMAN_REVIEW" if not failures else "BLOCKED"

    return {
        "gate_status": final_status,
        "failures": failures,
        "advisory": advisory,
        "warnings": warnings,
        "arithmetic": {
            "asset_value_sum_usd": _round2(asset_value_sum),
            "portfolio_total_value_usd": _round2(total_value),
            "value_delta_usd": _round2(value_delta),
            "allocation_sum_pct": _round2(allocation_sum),
            "allocation_delta_pct": _round2(allocation_delta),
            "asset_pnl_sum_usd": _round2(pnl_sum),
            "portfolio_unrealized_pnl_usd": _round2(total_pnl),
            "pnl_delta_usd": _round2(pnl_delta),
        },
        "detected": {
            "response_language_expected": "fr",
            "json_keys_language_expected": "en_stable",
            "pretty_json_required": True,
            "minified_json_detected": _compact_json_likely(json_text),
            "source_type": payload.get("source_type"),
            "reference_currency": payload.get("reference_currency"),
            "image_used": payload.get("image_used"),
            "image_evidence_status": image_evidence.get("status"),
            "human_review_required": payload.get("human_review_required"),
            "no_order_no_sizing": payload.get("no_order_no_sizing"),
            "no_auto_apply_in_blockers": "NO_AUTO_APPLY" in {str(item) for item in blockers},
            "no_auto_apply_root": payload.get("no_auto_apply"),
        },
    }


def build_human_readable_markdown(payload: dict[str, Any], validation: dict[str, Any]) -> str:
    portfolio = payload.get("portfolio") if isinstance(payload.get("portfolio"), dict) else {}
    assets = payload.get("assets") if isinstance(payload.get("assets"), list) else []
    evidence = payload.get("image_usage_evidence")
    evidence = evidence if isinstance(evidence, dict) else {}

    lines = [
        "# P133 — Rapport lisible capture réponse GEM multimodale",
        "",
        "## Décision",
        "",
        f"- Statut gate : `{validation['gate_status']}`",
        f"- Statut GEM : `{payload.get('status')}`",
        f"- Devise : `{payload.get('reference_currency')}`",
        f"- Image utilisée : `{payload.get('image_used')}`",
        f"- Evidence image : `{evidence.get('status')}`",
        f"- Human review : `{payload.get('human_review_required')}`",
        f"- No order / no sizing : `{payload.get('no_order_no_sizing')}`",
        "",
        "## Résumé portefeuille",
        "",
        f"- Valeur totale : `{portfolio.get('total_value_usd')}` USD",
        f"- PnL latent : `{portfolio.get('unrealized_pnl_usd')}` USD / `{portfolio.get('unrealized_pnl_pct')}`%",
        f"- Cash : `{portfolio.get('cash_usd_value')}` USD / `{portfolio.get('cash_allocation_pct')}`%",
        "",
        "## Actifs détectés",
        "",
        "| Symbol | Nom | Quantité | Prix USD | Valeur USD | Allocation % | PnL USD | PnL % | Confiance |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]

    for asset in assets:
        if not isinstance(asset, dict):
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    str(asset.get("symbol")),
                    str(asset.get("asset_name")),
                    str(asset.get("quantity")),
                    str(asset.get("price_usd")),
                    str(asset.get("value_usd")),
                    str(asset.get("allocation_pct")),
                    str(asset.get("unrealized_pnl_usd")),
                    str(asset.get("unrealized_pnl_pct")),
                    str(asset.get("confidence")),
                ]
            )
            + " |"
        )

    arithmetic = validation["arithmetic"]
    lines.extend(
        [
            "",
            "## Contrôles arithmétiques",
            "",
            f"- Somme valeurs actifs : `{arithmetic['asset_value_sum_usd']}` USD",
            f"- Total portefeuille : `{arithmetic['portfolio_total_value_usd']}` USD",
            f"- Écart valeur : `{arithmetic['value_delta_usd']}` USD",
            f"- Somme allocations : `{arithmetic['allocation_sum_pct']}`%",
            f"- Écart allocation : `{arithmetic['allocation_delta_pct']}`%",
            f"- Somme PnL actifs : `{arithmetic['asset_pnl_sum_usd']}` USD",
            f"- PnL portefeuille : `{arithmetic['portfolio_unrealized_pnl_usd']}` USD",
            f"- Écart PnL : `{arithmetic['pnl_delta_usd']}` USD",
            "",
            "## Lisibilité / format",
            "",
            f"- JSON minifié détecté : `{validation['detected']['minified_json_detected']}`",
            "- Action P133 : produire un JSON pretty-printed pour revue opérateur.",
            "",
            "## Failures",
            "",
        ]
    )

    if validation["failures"]:
        lines.extend(f"- `{item}`" for item in validation["failures"])
    else:
        lines.append("- Aucune failure bloquante.")

    lines.extend(["", "## Advisory", ""])
    if validation["advisory"]:
        lines.extend(f"- `{item}`" for item in validation["advisory"])
    else:
        lines.append("- Aucun advisory.")

    lines.extend(
        [
            "",
            "## Sécurité",
            "",
            "- HUMAN_REVIEW_REQUIRED",
            "- NO_BROKER",
            "- NO_ORDER",
            "- NO_SIZING",
            "- NO_AUTO_APPLY_GEM_RESPONSE",
            "- NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
        ]
    )

    return "\n".join(lines) + "\n"


def write_csv_summary(path: Path, payload: dict[str, Any], validation: dict[str, Any]) -> None:
    rows = [
        ("version", VERSION),
        ("gate_status", validation["gate_status"]),
        ("status", payload.get("status")),
        ("reference_currency", payload.get("reference_currency")),
        ("image_used", payload.get("image_used")),
        ("image_usage_evidence_status", validation["detected"]["image_evidence_status"]),
        ("human_review_required", payload.get("human_review_required")),
        ("no_order_no_sizing", payload.get("no_order_no_sizing")),
        ("no_auto_apply_in_blockers", validation["detected"]["no_auto_apply_in_blockers"]),
        ("minified_json_detected", validation["detected"]["minified_json_detected"]),
        ("asset_value_sum_usd", validation["arithmetic"]["asset_value_sum_usd"]),
        ("portfolio_total_value_usd", validation["arithmetic"]["portfolio_total_value_usd"]),
        ("value_delta_usd", validation["arithmetic"]["value_delta_usd"]),
        ("allocation_sum_pct", validation["arithmetic"]["allocation_sum_pct"]),
        ("allocation_delta_pct", validation["arithmetic"]["allocation_delta_pct"]),
        ("asset_pnl_sum_usd", validation["arithmetic"]["asset_pnl_sum_usd"]),
        ("portfolio_unrealized_pnl_usd", validation["arithmetic"]["portfolio_unrealized_pnl_usd"]),
        ("pnl_delta_usd", validation["arithmetic"]["pnl_delta_usd"]),
        ("failure_count", len(validation["failures"])),
        ("advisory_count", len(validation["advisory"])),
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)


def write_response_capture_gate(request: GemMultimodalResponseGateRequest) -> dict[str, Any]:
    generated_at = request.generated_at_utc or _utc_now_iso()
    _ensure_dir(request.output_dir)

    response_text = _read_response_text(request.response_text_path)
    payload, parse_warnings, json_text = parse_gem_response(response_text)

    validation = validate_payload(
        payload,
        json_text,
        tolerance_value_usd=request.tolerance_value_usd,
        tolerance_allocation_pct=request.tolerance_allocation_pct,
        tolerance_pnl_usd=request.tolerance_pnl_usd,
    )
    validation["warnings"].extend(parse_warnings)

    pretty_json = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False)
    manifest = {
        "status": "GEM_MULTIMODAL_RESPONSE_CAPTURE_GATE_READY",
        "gate_status": validation["gate_status"],
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": generated_at,
        "response_text_path": str(request.response_text_path),
        "source_image_path": str(request.source_image_path) if request.source_image_path else None,
        "reference_currency": payload.get("reference_currency"),
        "response_language_expected": "fr",
        "json_keys_language": "en_stable",
        "human_readable_summary_required": True,
        "pretty_json_required": True,
        "no_minified_json_for_operator_review": True,
        "safety_markers": list(SAFETY_MARKERS),
        "validation": validation,
    }

    (request.output_dir / "P133_GEM_RESPONSE_PRETTY.json").write_text(
        pretty_json + "\n", encoding="utf-8"
    )
    (request.output_dir / "P133_GEM_RESPONSE_CAPTURE_GATE.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    (request.output_dir / "P133_GEM_RESPONSE_HUMAN_REVIEW.md").write_text(
        build_human_readable_markdown(payload, validation), encoding="utf-8"
    )
    write_csv_summary(request.output_dir / "P133_OPERATOR_SUMMARY.csv", payload, validation)
    (request.output_dir / "P133_README.md").write_text(
        "# P133 — GEM multimodal response capture gate\n\n"
        "Capture locale de la réponse GEM multimodale, validation image/USD/sécurité, "
        "contrôles arithmétiques et restitution lisible pour revue humaine.\n\n"
        "Sécurité : no broker, no order, no sizing, no auto apply, no Sheet write.\n",
        encoding="utf-8",
    )

    return manifest


SAMPLE_GEM_RESPONSE = {
    "status": "REVIEW_REQUIRED",
    "source_type": "image",
    "reference_currency": "USD",
    "image_used": True,
    "copy_paste_text_used": False,
    "image_usage_evidence": {
        "status": "IMAGE_USED",
        "visual_evidence_summary": "L’image montre une interface de portefeuille crypto en USD avec une valeur totale visible de 655,66 $, une variation de -117,63 $ et -15.21%, ainsi que les lignes US Dollar, Bitcoin et USDC.",
        "visible_platform_or_context": "Interface type Revolut X / portefeuille crypto en USD",
        "blockers": [
            "HUMAN_REVIEW_REQUIRED",
            "NO_BROKER",
            "NO_ORDER",
            "NO_SIZING",
            "NO_AUTO_APPLY",
        ],
    },
    "portfolio": {
        "total_value_usd": 655.66,
        "unrealized_pnl_usd": -117.63,
        "unrealized_pnl_pct": -15.21,
        "cash_usd_value": 39.99,
        "cash_allocation_pct": 6.10,
    },
    "assets": [
        {
            "symbol": "USD",
            "asset_name": "US Dollar",
            "quantity": 39.99,
            "price_usd": 1.0,
            "value_usd": 39.99,
            "allocation_pct": 6.10,
            "unrealized_pnl_usd": None,
            "unrealized_pnl_pct": None,
            "confidence": "HIGH",
            "notes": "Ligne Espèces visible. Le PnL affiche un tiret, donc aucune valeur PnL n’est déduite.",
        },
        {
            "symbol": "BTC",
            "asset_name": "Bitcoin",
            "quantity": 0.00644955,
            "price_usd": 64644.62,
            "value_usd": 416.92,
            "allocation_pct": 63.59,
            "unrealized_pnl_usd": -117.69,
            "unrealized_pnl_pct": -22.01,
            "confidence": "HIGH",
            "notes": "Ligne Bitcoin visible dans la section Crypto-monnaies.",
        },
        {
            "symbol": "USDC",
            "asset_name": "USDC",
            "quantity": 198.756267,
            "price_usd": 1.0,
            "value_usd": 198.75,
            "allocation_pct": 30.31,
            "unrealized_pnl_usd": 0.06,
            "unrealized_pnl_pct": 0.03,
            "confidence": "HIGH",
            "notes": "Ligne USDC visible dans la section Crypto-monnaies.",
        },
    ],
    "missing_data": [],
    "unclear_data": [
        "Le PnL de la ligne US Dollar est affiché comme un tiret.",
        "Les valeurs proviennent de la capture d’écran et doivent rester soumises à revue humaine.",
    ],
    "human_review_required": True,
    "no_order_no_sizing": True,
}


def _write_sample_response(path: Path, *, minified: bool = True) -> None:
    if minified:
        path.write_text(
            json.dumps(SAMPLE_GEM_RESPONSE, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
    else:
        path.write_text(
            json.dumps(SAMPLE_GEM_RESPONSE, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="P133 GEM multimodal response capture gate")
    parser.add_argument("--response-text", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", default="P133-GEM-MULTIMODAL-RESPONSE-CAPTURE-GATE")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--source-image", type=Path)
    parser.add_argument("--write-sample-response", action="store_true")
    args = parser.parse_args(argv)

    _ensure_dir(args.output_dir)

    response_text = args.response_text
    if args.write_sample_response:
        response_text = args.output_dir / "P133_SAMPLE_GEM_RESPONSE_INPUT_MINIFIED.json"
        _write_sample_response(response_text, minified=True)

    if response_text is None:
        raise SystemExit("--response-text is required unless --write-sample-response is used")

    manifest = write_response_capture_gate(
        GemMultimodalResponseGateRequest(
            response_text_path=response_text,
            output_dir=args.output_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            source_image_path=args.source_image,
        )
    )
    print(manifest["status"])
    print(manifest["gate_status"])
    print(manifest["reference_currency"])
    print(manifest["validation"]["detected"]["image_used"])
    print(manifest["validation"]["detected"]["image_evidence_status"])
    print(manifest["validation"]["detected"]["minified_json_detected"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
