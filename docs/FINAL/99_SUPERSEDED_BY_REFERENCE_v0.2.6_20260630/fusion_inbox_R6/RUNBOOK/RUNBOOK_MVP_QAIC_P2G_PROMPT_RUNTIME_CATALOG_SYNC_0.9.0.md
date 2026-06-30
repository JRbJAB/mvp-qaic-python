# 🛠️ MVP QAIC — P2-G Runtime Prompt Catalog Sync — Runbook 0.9.0

## Objectif

Corriger le modèle prompt autour des 5 prompts métier validés dans `GPT_PROMPT_RUNTIME_SPEC` :

1. `prompt_01_portfolio_analysis` — Portfolio / positions / exposition / Revolut X si disponible
2. `prompt_02_market_analysis` — Marché / régime / momentum / liquidité
3. `prompt_03_buy_analysis_multi_horizon` — Reco achat / entrée / TP / SL / multi-horizon
4. `prompt_04_volatile_leverage_analysis` — Volatile / leverage / futures / funding / OI / liquidations
5. `prompt_05_full_trading_review` — Revue complète portfolio + marché + signal + décision

## Scripts inclus

- `scripts/mvpqaic_24_prompt_runtime_catalog_sync_core.gs`
- `scripts/mvpqaic_23_gpt_response_intake_core.gs`

## Sécurité

- `HUMAN_REVIEW_ONLY`
- `NO_BROKER`
- `NO_ORDER`
- `NO_SIZING`
- `NO_SECRET`
- `NO_DELETE`
- `NO_TRIGGER`
- `NO_MENU_MUTATION`

## Ordre de lancement

### 1. Charger les scripts

Remplacer/ajouter dans Apps Script :

- remplacer `mvpqaic_23_gpt_response_intake_core.gs` par la version `0.8.1_PROMPT_SELECTOR_SAFE`
- ajouter `mvpqaic_24_prompt_runtime_catalog_sync_core.gs`

### 2. Vérifier le catalogue runtime

```javascript
MVPQAIC_PromptRuntimeCatalogStatus()
```

Attendu :

```text
source_runtime_prompts_count = 5
source_runtime_prompt_ids contient prompt_01 à prompt_05
```

### 3. Synchroniser `📘 PROMPT_LIBRARY`

```javascript
MVPQAIC_PromptRuntimeCatalogSyncToLibrarySafe()
```

Attendu :

```text
status = OK
prompt_rows_inserted / updated > 0
runtime_prompt_ids = prompt_01...prompt_05
non_runtime_prompt_rows_marked_archive_candidate >= 0
```

Aucune suppression n’est faite. Les lignes parasites hors catalogue sont seulement marquées `DEPRECATED` / `NON_RUNTIME_PROMPT_ARCHIVE_CANDIDATE`.

### 4. Réinitialiser l’intake avec prompt_id éditable

```javascript
MVPQAIC_AiRuntimeReferenceInit()
MVPQAIC_GptResponseIntakeInit()
```

Dans `🧪 GPT_RESPONSE_INTAKE`, les champs éditables deviennent :

```text
ai_runtime_id
prompt_id
raw_response
ready_to_journal
human_review_note
```

### 5. Préparer les références avant test Gem/GPT

Choisir :

```text
ai_runtime_id = nomGEM_FULL_REVIEW_001
prompt_id = un des 5 prompts métier
```

Puis lancer :

```javascript
MVPQAIC_IntakePrepareRefs()
```

Ce bouton pré-remplit :

```text
ai_runtime_name
platform
runtime_type
gem_profile
prompt_contract_id
```

### 6. Après réponse du Gem/GPT

Coller la réponse complète dans :

```text
raw_response
```

Puis lancer :

```javascript
MVPQAIC_IntakeAnalyzeRawResponse()
```

Vérifier les champs extraits, puis passer :

```text
ready_to_journal = YES
```

Puis journaliser :

```javascript
MVPQAIC_JournalAppendFromIntake()
```

## Boutons recommandés dans `🧪 GPT_RESPONSE_INTAKE`

Créer 3 dessins ou boutons :

1. `🔄 Préparer références` → `MVPQAIC_IntakePrepareRefs`
2. `🧪 Analyser réponse` → `MVPQAIC_IntakeAnalyzeRawResponse`
3. `🧾 Journaliser` → `MVPQAIC_JournalAppendFromIntake`
