# P137 — GEM Prompt Corrections Overlay

Version: MVP_QAIC_P137_PROMPT_CORRECTIONS_APPLY_QUEUE_20260622
Generated at UTC: 2026-06-22T00:00:00Z
Gem actif: GEM_GENERAL_REVIEW
Prompt profile: P132_R2_MULTIMODAL_PORTFOLIO_USD
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
{
  "contract_id": "P137_GEM_OUTPUT_CONTRACT",
  "gem_id": "GEM_GENERAL_REVIEW",
  "prompt_profile": "P132_R2_MULTIMODAL_PORTFOLIO_USD",
  "language": "fr",
  "required_response_shape": {
    "human_summary_first": true,
    "json_fenced_block_required": true,
    "json_pretty_required": true,
    "technical_keys_keep_english": true
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
    "safety"
  ],
  "required_enums": {
    "status": [
      "OK",
      "REVIEW_REQUIRED",
      "BLOCKED"
    ],
    "image_used": [
      "IMAGE_USED",
      "IMAGE_NOT_USED",
      "REVIEW_REQUIRED"
    ],
    "risk_level": [
      "LOW",
      "MEDIUM",
      "HIGH",
      "REVIEW"
    ]
  },
  "hard_safety": {
    "human_review_required": true,
    "no_order_no_sizing": true,
    "no_broker_execution": true,
    "no_auto_apply": true,
    "no_invented_portfolio_data": true
  }
}
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
{
  "status": "REVIEW_REQUIRED",
  "gem_id": "GEM_GENERAL_REVIEW",
  "prompt_profile": "P132_R2_MULTIMODAL_PORTFOLIO_USD",
  "reference_currency": "USD",
  "image_used": "IMAGE_USED",
  "image_usage_evidence": "Décrire exactement les éléments visibles dans la capture utilisée.",
  "portfolio_extract": {
    "positions": [],
    "total_value_usd": null,
    "cash_usd": null
  },
  "missing_data": [],
  "blockers": [],
  "human_review_required": true,
  "no_order_no_sizing": true,
  "safety": {
    "no_broker_execution": true,
    "no_order": true,
    "no_sizing": true,
    "no_auto_apply": true,
    "no_invented_portfolio_data": true
  }
}
```
```

---

# Prompt source

# P136C — Prompt Corrections Queue

Selected GEM: `GEM_GENERAL_REVIEW`

| correction_id | priority | status | scope | issue | proposed_fix |
|---|---:|---|---|---|---|
| P136_PROMPT_001 | HIGH | TODO | GEM_SELECTION | Le cockpit doit permettre le choix contrôlé du Gem actif. | Utiliser uniquement gem_id depuis ACTIVE_GEM_PROFILES. |
| P136_PROMPT_002 | HIGH | TODO | P132_R2_OUTPUT_FORMAT | Renforcer la sortie résumé lisible + JSON pretty fenced. | Ajouter un garde-fou de format dans la prochaine correction de prompt. |
| P136_PROMPT_003 | MEDIUM | TODO | IMAGE_USAGE_EVIDENCE | Rendre la preuve d'utilisation image plus visible pour human review. | Exiger un court champ/texte d'évidence image_used avant JSON. |
| P136_PROMPT_004 | MEDIUM | TODO | STITCH_UI_LOGIC | Aligner les prompts avec la logique UI Stitch/NiceGUI. | Synchroniser les écrans prompt, import réponse, P133 gate et corrections dans une spec UI unique. |
| P136C_UI_001 | HIGH | DONE | NICEGUI_OPERATOR_UI | Le rendu P136-R1 était trop technique et dominé par des JSON dumps. | Remplacer la page par un cockpit avec workflow gauche, tabs centraux, décision droite et debug caché. |

Safety: local private only, no broker, no order, no sizing, no auto apply.
