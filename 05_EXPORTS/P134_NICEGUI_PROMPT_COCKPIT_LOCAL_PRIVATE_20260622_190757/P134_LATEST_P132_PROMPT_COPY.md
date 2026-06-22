
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
{
  "status": "REVIEW_REQUIRED",
  "source_type": "image",
  "reference_currency": "USD",
  "image_used": true
}
```
```

## Hard rules

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
{
  "properties": {
    "assets": {
      "items": {
        "properties": {
          "allocation_pct": {
            "type": [
              "number",
              "null"
            ]
          },
          "asset_name": {
            "type": [
              "string",
              "null"
            ]
          },
          "confidence": {
            "enum": [
              "HIGH",
              "MEDIUM",
              "LOW",
              "REVIEW"
            ]
          },
          "notes": {
            "type": [
              "string",
              "null"
            ]
          },
          "price_usd": {
            "type": [
              "number",
              "null"
            ]
          },
          "quantity": {
            "type": [
              "number",
              "string",
              "null"
            ]
          },
          "symbol": {
            "type": [
              "string",
              "null"
            ]
          },
          "unrealized_pnl_pct": {
            "type": [
              "number",
              "null"
            ]
          },
          "unrealized_pnl_usd": {
            "type": [
              "number",
              "null"
            ]
          },
          "value_usd": {
            "type": [
              "number",
              "null"
            ]
          }
        },
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
          "notes"
        ],
        "type": "object"
      },
      "type": "array"
    },
    "copy_paste_text_used": {
      "type": "boolean"
    },
    "human_review_required": {
      "const": true
    },
    "image_usage_evidence": {
      "properties": {
        "blockers": {
          "items": {
            "type": "string"