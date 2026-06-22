
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

## Block if

- GEM did not mention evidence from the image.
- GEM used EUR without explicit conversion.
- GEM invented missing values.
- GEM suggests an order, broker action, or sizing.
