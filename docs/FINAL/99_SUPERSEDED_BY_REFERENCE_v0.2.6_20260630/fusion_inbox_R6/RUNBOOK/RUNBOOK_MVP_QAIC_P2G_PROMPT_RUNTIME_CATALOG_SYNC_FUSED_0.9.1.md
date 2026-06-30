# 🧭 Runbook — P2-G Runtime Prompt Catalog Sync FUSED 0.9.1

## 1. Remplacer les scripts live

Remplacer entièrement :

```text
mvpqaic_11_p1_prompt_quality_core.gs
mvpqaic_23_gpt_response_intake_core.gs
```

Ne pas ajouter `mvpqaic_24_prompt_runtime_catalog_sync_core.gs` dans Apps Script live.

## 2. Contrôle version

Lancer :

```javascript
MVPQAIC_PromptQualityCoreStatus()
```

Attendu :

```text
MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.9.1_RUNTIME_CATALOG_SYNC_FUSED_SAFE
```

## 3. Audit catalogue prompts

Lancer :

```javascript
MVPQAIC_PromptRuntimeCatalogStatus()
```

Attendu : 5 prompts runtime depuis `GPT_PROMPT_RUNTIME_SPEC` :

```text
prompt_01_portfolio_analysis
prompt_02_market_analysis
prompt_03_buy_analysis_multi_horizon
prompt_04_volatile_leverage_analysis
prompt_05_full_trading_review
```

## 4. Synchroniser 📘 PROMPT_LIBRARY

Lancer :

```javascript
MVPQAIC_PromptRuntimeCatalogSyncToLibrarySafe()
```

Le script ajoute/met à jour les 5 `PROMPT_CONTRACT` métier et marque les faux prompts non-runtime comme `DEPRECATED_ARCHIVE_CANDIDATE`, sans suppression.

## 5. Préparer intake

Lancer :

```javascript
MVPQAIC_AiRuntimeReferenceInit()
MVPQAIC_GptResponseIntakeInit()
```

Puis dans `🧪 GPT_RESPONSE_INTAKE`, choisir :

```text
ai_runtime_id
prompt_id
```

Ensuite :

```javascript
MVPQAIC_IntakePrepareRefs()
MVPQAIC_IntakeAnalyzeRawResponse()
MVPQAIC_JournalAppendFromIntake()
```

## Boutons conseillés

```text
🔄 Préparer références  → MVPQAIC_IntakePrepareRefs
🧪 Analyser réponse     → MVPQAIC_IntakeAnalyzeRawResponse
🧾 Journaliser          → MVPQAIC_JournalAppendFromIntake
```
