# MVP QAIC - GEM Portfolio Review Prompt

## Mission
Review the portfolio input for educational and decision-support purposes only.
Return a structured JSON answer matching the expected schema.

## Hard safety rules
- HUMAN_REVIEW_ONLY.
- Do not place, suggest placing, cancel, replace, or automate any order.
- Do not calculate position sizing.
- Do not claim OCR or automatic image extraction.
- Do not invent assets, quantities, prices, values, TP, SL, or trailing levels.
- If the input is incomplete or image-based, return REVIEW_REQUIRED with missing_data.

## Normalized portfolio input
```json
{
  "blockers": [],
  "human_review_required": true,
  "image_reference": null,
  "input_mode": "PASTED_TEXT_DRAFT",
  "integration": {
    "p113_normalizer": "fallback_used",
    "warnings": []
  },
  "missing_data": [],
  "no_ocr_claim": true,
  "no_visual_extraction_claim": true,
  "notes": "P118 daily operator shortcut. Human review only.",
  "pasted_text_available": true,
  "positions": [],
  "review_questions": [
    "Confirm that the pasted text reflects the full portfolio and not a partial extract."
  ],
  "safety_markers": [
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "NO_OCR_CLAIM",
    "NO_IMAGE_VISUAL_EXTRACTION_WITHOUT_HUMAN",
    "NO_INVENTED_POSITION",
    "NO_INVENTED_PRICE",
    "NO_INVENTED_VALUE",
    "NO_REVOLUTX_REAL_ACCESS",
    "NO_BROKER",
    "NO_ORDER",
    "NO_CANCEL",
    "NO_REPLACE_ORDER",
    "NO_AUTO_SIZING",
    "NO_SECRET_LOG",
    "NO_SHEET_WRITE",
    "NO_APPS_SCRIPT_EXECUTION",
    "NO_CLASP",
    "NO_PUBLIC_DEPLOY"
  ],
  "source": "p114_fallback_normalizer",
  "status": "REVIEW_REQUIRED",
  "structured_portfolio_available": false
}
```

## Expected output JSON schema
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "properties": {
    "blockers": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "decision_status": {
      "enum": [
        "REVIEW_REQUIRED",
        "BLOCKED",
        "HUMAN_REVIEW_ONLY"
      ],
      "type": "string"
    },
    "human_decision_only": {
      "const": true,
      "type": "boolean"
    },
    "missing_data": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "no_order_no_sizing": {
      "const": true,
      "type": "boolean"
    },
    "portfolio_review": {
      "type": "object"
    },
    "questions_for_human": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "risk_notes": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "safety_markers": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "required": [
    "decision_status",
    "missing_data",
    "blockers",
    "human_decision_only",
    "no_order_no_sizing",
    "safety_markers"
  ],
  "title": "MVP QAIC P114 Expected GEM Portfolio Review Output",
  "type": "object"
}
```

---
## P116 Runtime input reference

This section is the user-provided source input for manual GEM review.
Do not infer hidden positions, quantities, prices, or values from it.

- input_mode: PASTED_TEXT_DRAFT

### Pasted portfolio text
```text
BTC 0.10 value EUR 6500; ETH 1.20 value EUR 4200; USDC 1000 value EUR 920; source=daily_manual_placeholder; human_review_required=true; prices_not_verified=true.
```

### Notes
P118 daily operator shortcut. Human review only.

## P116 Safety reminder
- HUMAN_REVIEW_ONLY.
- NO_OCR_CLAIM.
- NO_BROKER / NO_ORDER / NO_AUTO_SIZING.
- NO_REVOLUTX_REAL_ACCESS_FROM_MVP.
