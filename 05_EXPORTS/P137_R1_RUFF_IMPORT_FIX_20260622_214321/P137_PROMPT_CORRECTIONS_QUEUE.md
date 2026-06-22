# P137 — Prompt Corrections Apply Queue

Status: `P137_PROMPT_CORRECTIONS_READY_FOR_HUMAN_REVIEW`
Selected GEM: `GEM_GENERAL_REVIEW`

| correction_id | priority | status | scope | issue | applied_rule |
|---|---:|---|---|---|---|
| P137_GEM_001 | HIGH | APPLIED_TO_LOCAL_DRAFT | OUTPUT_FORMAT | La réponse GEM doit être lisible humainement puis fournir un JSON pretty fenced. | Imposer un résumé court puis un bloc ```json strict. |
| P137_GEM_002 | HIGH | APPLIED_TO_LOCAL_DRAFT | IMAGE_USAGE_EVIDENCE | La preuve d'utilisation de l'image doit être explicite. | Ajouter `image_used` et `image_usage_evidence` obligatoires. |
| P137_GEM_003 | HIGH | APPLIED_TO_LOCAL_DRAFT | USD_REFERENCE | La devise de référence doit rester verrouillée sur USD pour Revolut X. | Ajouter `reference_currency=USD` et champs `*_usd`. |
| P137_GEM_004 | HIGH | APPLIED_TO_LOCAL_DRAFT | SAFETY_GUARDS | Le GEM ne doit jamais produire d'ordre, sizing ou auto-apply. | Exiger `no_order_no_sizing=true`, `human_review_required=true`. |
| P137_GEM_005 | HIGH | APPLIED_TO_LOCAL_DRAFT | MISSING_DATA | Les données manquantes doivent bloquer ou passer en review, jamais être inventées. | Ajouter `missing_data`, `blockers`, `status=REVIEW_REQUIRED|BLOCKED`. |
| P137_GEM_006 | MEDIUM | APPLIED_TO_LOCAL_DRAFT | P133_COMPATIBILITY | La sortie GEM doit rester compatible avec la gate P133. | Ajouter marqueurs et clés attendus par capture gate. |
| P137_GEM_007 | MEDIUM | APPLIED_TO_LOCAL_DRAFT | GEM_RUNTIME_PROFILE | La correction doit tenir compte du GEM actif. | Injecter `gem_id`, `prompt_profile`, capacités et limites dans l'en-tête. |

## Sécurité

- Brouillon local uniquement.
- Aucune modification du prompt source.
- Human review obligatoire avant usage stable.
- Aucun broker, ordre, sizing, auto-apply.
