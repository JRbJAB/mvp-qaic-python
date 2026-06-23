# P154 — P132/P133 Patch Plan

- Status: `P154_PROMPT_CORRECTION_APPLY_PLAN_READY_REVIEW_ONLY`
- Prompt source: `P132_P133_PORTFOLIO_MULTIMODAL_REVIEW`
- Plan rows: `4`
- Apply allowed: `False`

## Plan proposé

Ce batch ne modifie pas le prompt. Il prépare seulement les corrections candidates.

### Correction candidate principale

- Renforcer P132/P133 sur la preuve d'utilisation image.
- Renforcer la devise de référence.
- Renforcer la réconciliation arithmétique.
- Maintenir `human_review_required=true`.
- Maintenir `no_order_no_sizing=true`.
- Maintenir `NO_AUTO_APPLY=true`.

## Interdits

- Pas d'apply automatique.
- Pas d'écriture Sheets.
- Pas de public deploy.
- Pas de broker/order/sizing.
