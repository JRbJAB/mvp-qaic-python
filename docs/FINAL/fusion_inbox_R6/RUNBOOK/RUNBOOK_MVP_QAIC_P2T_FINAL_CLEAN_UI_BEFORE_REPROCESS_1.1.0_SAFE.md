# 🛠️ MVP QAIC — P2-T Final Clean UI Before Reprocess — 1.1.0

## Statut
`SAFE_READY_FOR_INSTALL`

## Scripts à remplacer
- `scripts/mvpqaic_11_p1_prompt_quality_core.gs`
- `scripts/mvpqaic_23_gpt_response_intake_core.gs`

## Objectif
Finaliser les trois onglets avant de relancer un nouveau cycle Gem depuis une base propre :

- `🧭 PROMPT_IMPROVEMENT_QUEUE`
  - ajoute `ai_runtime_name` entre `prompt_id` et `next_prompt_draft` ;
  - fige le bloc `backlog_id / prompt_id / ai_runtime_name` ;
  - conserve `next_prompt_draft` visible immédiatement après ;
  - force hauteurs compactes + CLIP.

- `🧾 DECISION_JOURNAL`
  - `test_datetime` en heure de Paris ;
  - `journal_id`, `payload_id`, `test_datetime` en colonnes compactes ;
  - `ai_runtime_name` placé entre `test_datetime` et `prompt_id` ;
  - forçage des hauteurs sur toutes les lignes de la grille ;
  - CLIP sur toutes les cellules.

- `📘 PROMPT_LIBRARY`
  - `ai_runtime_name` placé entre `contract_id` et `prompt_id` ;
  - ajout `cleanup_action` et `cleanup_reason` pour identifier les lignes à garder / archiver / revoir ;
  - conservation des prompts références verrouillés et des variantes ;
  - aucune suppression.

## Fonctions à lancer après remplacement

```javascript
MVPQAIC_JournalFormatUltimate()
MVPQAIC_PromptWorkflowSheetsOptimize()
```

## Garde-fous
- Aucune suppression.
- Aucun trigger/menu.
- Aucun broker/order/sizing.
- `PROMPT_LIBRARY` : nettoyage signalé par colonnes, pas appliqué automatiquement.
