# 🛠️ MVP QAIC — P1-G Prompt Library / Contract Update — Runbook

**Version :** `MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.6.0_SAFE_FULL_FUSION_P1E_P1F_P1G`  
**Date :** 2026-06-11  
**Statut :** `READY_FOR_RUNTIME_VALIDATION`  

## Objectif

P1-G consolide P1-E + P1-F dans le même core durable et ajoute la génération de `PROMPT_LIBRARY`.

Le principe est volontairement simple : un seul onglet visible, mais avec lignes typées :

- `CORE_CONTRACT` : règles stables non négociables.
- `GEM_PROFILE` : capacités par Gem / runtime / futur QAIC readonly.
- `PROMPT_CONTRACT` : contrats de prompts issus de `PROMPT_IMPROVEMENT_QUEUE`.

## Sécurité

Lecture :

```text
DECISION_JOURNAL
GPT_QUALITY_DASHBOARD
PROMPT_IMPROVEMENT_QUEUE
```

Écriture :

```text
GPT_QUALITY_DASHBOARD
PROMPT_IMPROVEMENT_QUEUE
PROMPT_LIBRARY
```

Interdits :

```text
NO_BROKER
NO_ORDER
NO_SIZING
NO_SECRET
NO_TRADING_BOT
NO_AUTO_EXECUTION
```

## Installation

Remplacer dans Apps Script le fichier durable :

```text
mvpqaic_11_p1_prompt_quality_core.gs
```

par la version complète fournie dans `scripts/`.

Ne pas ajouter un nouveau script isolé P1-G.

## Validation runtime

Lancer dans cet ordre :

```javascript
MVPQAIC_PromptQualityCoreStatus()
MVPQAIC_PromptQualityDashboardStatus()
MVPQAIC_PromptImprovementQueueStatus()
MVPQAIC_PromptLibraryStatus()
MVPQAIC_PromptLibraryRefresh()
```

Résultat attendu pour P1-G :

```text
status = REFRESHED
target_sheet = PROMPT_LIBRARY
library_rows_written >= 1
core_contract_rows >= 2
gem_profile_rows >= 4
prompt_contract_rows >= 1
safety = HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET
```

## Règle métier importante

Un Gem peut expliquer plus qu’il ne peut scorer.
Un score est autorisé uniquement si :

```text
runtime_profile supports metric
metric data is present
source and as_of_date exist
quality_score/risk_guard are present
```

Sinon :

```text
score = NOT_AVAILABLE
ou decision_status = REVIEW_REQUIRED / BLOCKED
```

Jamais d’invention de prix, PRU, quantité, PnL, TP, SL, exposition ou score.
