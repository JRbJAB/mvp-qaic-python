# 🛠️ MVP QAIC — P3-E Risk Playbook Position Action Simple Apply — 1.4.5 SAFE

## Objectif

Résoudre le blocage `BLOCKED_TARGET_HEADER_NOT_FOUND` sur les 10 lignes approuvées `RISK_PLAYBOOK!position_action`.

## Cause

`🧪 LEXIQUE_GAP_AUDIT` pointe vers `RISK_PLAYBOOK.position_action`, mais la colonne `position_action` n’existe pas encore dans la table source `RISK_PLAYBOOK`.

## Solution simple

- créer uniquement la colonne source manquante `position_action` dans `RISK_PLAYBOOK` si elle n’existe pas ;
- appliquer uniquement les lignes déjà marquées `review_decision = APPROVE_APPLY` ;
- écrire uniquement dans les cellules vides ;
- ne jamais écrire directement dans `📚 LEXIQUE_MASTER` ;
- reconstruire `📚 LEXIQUE_MASTER` et `🔎 SEARCH_COCKPIT` seulement si au moins une ligne est appliquée.

## Fonctions

```javascript
MVPQAIC_P3E_RiskPlaybookPositionActionStatus()
MVPQAIC_P3E_RiskPlaybookPositionActionDryRun()
MVPQAIC_P3E_RiskPlaybookPositionActionApplySafe()
```

## Séquence recommandée

```javascript
MVPQAIC_P3E_RiskPlaybookPositionActionStatus()
MVPQAIC_P3E_RiskPlaybookPositionActionDryRun()
MVPQAIC_P3E_RiskPlaybookPositionActionApplySafe()
```

Puis relancer l’audit :

```javascript
MVPQAIC_P3A_LexiqueExistingGapAuditRun()
```

## Sécurité

- HUMAN_REVIEW_ONLY
- NO broker / order / sizing
- NO secret
- NO delete / hide / menu / trigger mutation
- NO generated master direct apply
- no overwrite
- applies only `APPROVE_APPLY`
