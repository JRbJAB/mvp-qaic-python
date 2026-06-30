# 🧭 Runbook — MVP QAIC P2-H Prompt Template To Copy 0.9.2

## 1. Remplacer les scripts

Remplacer dans Apps Script :

```text
mvpqaic_11_p1_prompt_quality_core.gs
mvpqaic_23_gpt_response_intake_core.gs
```

Ne pas ajouter de nouveau script. Ne pas utiliser `mvpqaic_24`.

## 2. Synchroniser la library

```javascript
MVPQAIC_PromptRuntimeCatalogSyncToLibrarySafe()
```

Résultat attendu : `📘 PROMPT_LIBRARY` contient les 5 `PROMPT_CONTRACT` runtime avec une colonne :

```text
prompt_template_to_copy
```

C’est le champ à copier/coller dans le Gem.

## 3. Initialiser / préparer l’intake

```javascript
MVPQAIC_GptResponseIntakeInit()
MVPQAIC_IntakePrepareRefs()
```

Dans `🧪 GPT_RESPONSE_INTAKE`, sélectionner :

```text
ai_runtime_id
prompt_id
```

Puis copier la valeur `prompt_template_to_copy` dans le Gem.

## 4. Coller la réponse Gem

La réponse du Gem se colle dans :

```text
raw_response
```

Puis lancer :

```javascript
MVPQAIC_IntakeAnalyzeRawResponse()
```

## 5. Journaliser

Après contrôle humain :

```text
ready_to_journal = YES
```

Puis :

```javascript
MVPQAIC_JournalAppendFromIntake()
```

## 6. Repartir vierge

```javascript
MVPQAIC_IntakeNewBlank()
```

Conserve `ai_runtime_id`, `prompt_id` et `prompt_template_to_copy`, vide `raw_response` et les champs de parsing.
