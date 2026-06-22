# P113 — Portfolio Input Normalizer + Image Review Workflow

## Mode

`IMAGE_REVIEW_REQUIRED`

## Asset candidates

`NONE`

## Human review

human_review_required=`True`

## Missing data

- `portfolio_image_visual_extraction`

## Review required reasons

- `IMAGE_CAPTURE_REQUIRES_HUMAN_VISUAL_CONFIRMATION`

## Image review checklist

- Confirm that the image/capture reference is correct: portfolio_capture_example.png.
- List every visible asset symbol exactly as displayed.
- Confirm visible quantity/amount for each asset.
- Confirm visible fiat value for each asset if present.
- Confirm average entry price/cost basis only if it is explicitly visible.
- Confirm current price only if explicitly visible or provided as separate market context.
- Do not infer hidden rows or missing assets from the capture.
- Do not generate an order, sizing, stop-loss, take-profit, or trailing action.

## Draft rows from pasted text

- No text draft rows.

## Safety

- NO_OCR_CLAIM
- NO_IMAGE_VISUAL_EXTRACTION_WITHOUT_HUMAN
- NO_INVENTED_POSITION
- NO_INVENTED_PRICE
- NO_INVENTED_VALUE
- NO_BROKER
- NO_ORDER
- NO_SIZING
