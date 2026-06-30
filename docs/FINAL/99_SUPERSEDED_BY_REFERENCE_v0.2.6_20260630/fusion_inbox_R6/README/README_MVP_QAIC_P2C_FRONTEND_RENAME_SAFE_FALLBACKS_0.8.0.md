# 🛠️ MVP QAIC — P2-C Frontend Rename Safe Fallbacks — 0.8.0

## Version
`MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.8.0_FRONTEND_RENAME_SAFE_FALLBACKS`

## Objectif
Renommer proprement les onglets frontend prompt avec emoji, sans suppression ni écrasement, et avec compatibilité old/new names dans le core prompt.

## Renommages prévus
- `DECISION_JOURNAL` → `🧾 DECISION_JOURNAL`
- `GPT_QUALITY_DASHBOARD` → `📊 GPT_QUALITY_DASHBOARD`
- `PROMPT_IMPROVEMENT_QUEUE` → `🧭 PROMPT_IMPROVEMENT_QUEUE`
- `PROMPT_LIBRARY` → `📘 PROMPT_LIBRARY`

## Fonctions P2-C
```javascript
MVPQAIC_FrontendRenameStatus()
MVPQAIC_FrontendRenameDryRun()
MVPQAIC_FrontendRenameApplySafe()
```

## Garde-fous
- Dry-run disponible avant apply.
- Apply bloqué si old et new existent en même temps.
- Aucun delete.
- Aucun overwrite.
- Aucun trigger/menu mutation.
- Fallback old/new actif dans le core prompt.

## Ordre conseillé
```javascript
MVPQAIC_FrontendRenameStatus()
MVPQAIC_FrontendRenameDryRun()
MVPQAIC_FrontendRenameApplySafe()
MVPQAIC_PromptQualityCoreStatus()
MVPQAIC_PromptAdaptiveLoopStatus()
```
