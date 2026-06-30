# 🛠️ MVP QAIC — P2-B GEM Adaptive Prompt Loop — 0.7.0

Version: `MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.7.0_GEM_ADAPTIVE_LOOP_SAFE`
Date: 2026-06-12
Status: SAFE_DRAFT_ONLY

## Objectif

Fusionner P2-B dans `mvpqaic_11_p1_prompt_quality_core.gs` sans créer de nouveau script ni nouvel onglet.

Le module lit le dernier test GPT réel depuis `DECISION_JOURNAL`, lit `GPT_QUALITY_DASHBOARD`, `PROMPT_IMPROVEMENT_QUEUE` et `PROMPT_LIBRARY`, puis écrit un brouillon `next_prompt_draft` dans `PROMPT_IMPROVEMENT_QUEUE`.

## Garde-fous

- `PROMPT_LIBRARY` est lu en read-only par P2-B.
- Aucun overwrite de prompt idéal.
- Aucune promotion automatique en ACTIVE.
- Écriture P2-B limitée à `PROMPT_IMPROVEMENT_QUEUE`.
- `promotion_allowed = NO`.
- `human_review_status = TO_REVIEW`.

## Fonctions

```javascript
MVPQAIC_PromptAdaptiveLoopStatus()
MVPQAIC_PromptAdaptiveNextDraftBuild()
MVPQAIC_PromptAdaptiveRunAllFast()
```

## Run conseillé

```javascript
MVPQAIC_PromptAdaptiveLoopStatus()
MVPQAIC_PromptAdaptiveNextDraftBuild()
```

## Sortie

Dans `PROMPT_IMPROVEMENT_QUEUE`, ligne `queue_type = ADAPTIVE_NEXT_PROMPT_DRAFT`, avec colonnes :

- `gem_profile`
- `base_prompt_version`
- `source_journal_id`
- `source_payload_id`
- `adaptive_issue_summary`
- `mandatory_fields_patch`
- `missing_data_patch`
- `blocker_patch`
- `next_prompt_draft`
- `draft_status`
- `human_review_status`
- `promotion_allowed`
- `base_prompt_readonly`
- `prompt_library_write_allowed`
