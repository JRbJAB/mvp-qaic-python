# P133 — Rapport lisible capture réponse GEM multimodale

## Décision

- Statut gate : `PASS_WITH_HUMAN_REVIEW`
- Statut GEM : `REVIEW_REQUIRED`
- Devise : `USD`
- Image utilisée : `True`
- Evidence image : `IMAGE_USED`
- Human review : `True`
- No order / no sizing : `True`

## Résumé portefeuille

- Valeur totale : `655.66` USD
- PnL latent : `-117.63` USD / `-15.21`%
- Cash : `39.99` USD / `6.1`%

## Actifs détectés

| Symbol | Nom | Quantité | Prix USD | Valeur USD | Allocation % | PnL USD | PnL % | Confiance |
|---|---|---:|---:|---:|---:|---:|---:|---|
| USD | US Dollar | 39.99 | 1.0 | 39.99 | 6.1 | None | None | HIGH |
| BTC | Bitcoin | 0.00644955 | 64644.62 | 416.92 | 63.59 | -117.69 | -22.01 | HIGH |
| USDC | USDC | 198.756267 | 1.0 | 198.75 | 30.31 | 0.06 | 0.03 | HIGH |

## Contrôles arithmétiques

- Somme valeurs actifs : `655.66` USD
- Total portefeuille : `655.66` USD
- Écart valeur : `0.0` USD
- Somme allocations : `100.0`%
- Écart allocation : `0.0`%
- Somme PnL actifs : `-117.63` USD
- PnL portefeuille : `-117.63` USD
- Écart PnL : `0.0` USD

## Lisibilité / format

- JSON minifié détecté : `True`
- Action P133 : produire un JSON pretty-printed pour revue opérateur.

## Failures

- Aucune failure bloquante.

## Advisory

- `no_auto_apply_root_field_missing_future_schema_recommendation`
- `gem_response_json_minified_single_line_operator_unfriendly`

## Sécurité

- HUMAN_REVIEW_REQUIRED
- NO_BROKER
- NO_ORDER
- NO_SIZING
- NO_AUTO_APPLY_GEM_RESPONSE
- NO_REVOLUTX_REAL_ACCESS_FROM_MVP
