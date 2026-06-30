# 🧭 RUNBOOK — MVP QAIC P2-R 1.0.8

## 1. Installer les scripts actifs

Remplacer en live Apps Script :

```text
mvpqaic_11_p1_prompt_quality_core.gs
mvpqaic_23_gpt_response_intake_core.gs
```

Ne pas installer :

```text
archive_reference_only/mvpqaic_24_prompt_runtime_catalog_sync_core_DO_NOT_INSTALL_LIVE.gs
```

## 2. Restaurer les références originales

Lancer :

```javascript
MVPQAIC_PromptLibraryRestoreOriginalReferencesSafe()
```

Attendu :

```text
prompt_05_original_guaranteed = true
restored_prompt_ids contient prompt_05_full_trading_review
```

## 3. Réappliquer l'UX Prompt Library / Queue

Lancer :

```javascript
MVPQAIC_PromptWorkflowSheetsOptimize()
```

## 4. Vérifier dans 📘 PROMPT_LIBRARY

Pour `prompt_05_full_trading_review`, une ligne référence doit contenir :

```text
prompt_id = prompt_05_full_trading_review
base_prompt_id = prompt_05_full_trading_review
parent_prompt_id = vide
record_type = PROMPT_CONTRACT ou PROMPT_REFERENCE
prompt_version_role = ULTIMATE_REFERENCE_LOCKED
status = ULTIMATE_REFERENCE_LOCKED
is_reference_locked = YES
prompt_template_to_copy = prompt original restauré
original_prompt_template = prompt original restauré
ultimate_reference_prompt = prompt original restauré
```

Les corrections Gem doivent créer des variantes avec des IDs de type :

```text
prompt_05_full_trading_review__nomGEM_FULL_REVIEW_001__vYYYYMMDDHHMMSS
```
