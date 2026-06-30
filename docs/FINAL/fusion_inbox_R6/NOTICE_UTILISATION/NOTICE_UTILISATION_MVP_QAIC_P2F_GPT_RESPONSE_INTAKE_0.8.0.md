# 🧪 Notice d’utilisation — MVP QAIC P2-F GPT Response Intake — 0.8.0

## 🎯 Objectif

Créer une passerelle simple et contrôlée entre une réponse GPT/Gem/IA et le journal officiel `🧾 DECISION_JOURNAL`.

La règle est volontairement simple : le parsing est automatique, mais la journalisation reste validée humainement.

## 🧩 Onglets créés

### 🤖 AI_RUNTIME_REFERENCE

Base courte des GPT/Gem/IA utilisables.

L’entrée par défaut est :

```text
ai_runtime_id = nomGEM_FULL_REVIEW_001
prompt_id = prompt_05_full_trading_review
prompt_contract_id = P2D-PROMPT-BASELINE-001-PROMPT_05_FULL_TRADING_REVIEW
gem_profile = GEM_GENERAL_REVIEW
```

### 🧪 GPT_RESPONSE_INTAKE

Zone de saisie et d’analyse de la réponse GPT/Gem.

Champs éditables minimum :

| Champ | Mode | Description |
|---|---|---|
| `ai_runtime_id` | éditable | Sélection du GPT/Gem/IA utilisé. |
| `raw_response` | éditable | Réponse complète collée depuis le GPT/Gem. |
| `ready_to_journal` | éditable | `NO` par défaut, passer à `YES` après contrôle humain. |
| `human_review_note` | éditable optionnel | Note courte de validation humaine. |

`prompt_id`, `gem_profile`, `prompt_contract_id`, `platform` et `ai_runtime_name` sont auto-remplis depuis `🤖 AI_RUNTIME_REFERENCE`.

## ▶️ Workflow quotidien

1. Lancer une fois :

```javascript
MVPQAIC_AiRuntimeReferenceInit()
```

2. Lancer une fois :

```javascript
MVPQAIC_GptResponseIntakeInit()
```

3. Dans `🧪 GPT_RESPONSE_INTAKE`, choisir :

```text
ai_runtime_id = nomGEM_FULL_REVIEW_001
```

4. Coller la réponse complète dans :

```text
raw_response
```

5. Lancer :

```javascript
MVPQAIC_IntakeAnalyzeRawResponse()
```

6. Vérifier les champs extraits :

```text
analysis_level
decision_status
human_final_decision
validation_status
signal_id
score_id
risk_guard
missing_data
blockers
confidence_score
quality_score
```

7. Si c’est correct, passer :

```text
ready_to_journal = YES
```

8. Lancer :

```javascript
MVPQAIC_JournalAppendFromIntake()
```

## ✅ Conditions de journalisation

Le script journalise uniquement si :

```text
ready_to_journal = YES
mandatory_fields_missing_count = 0
parse_status = OK ou REVIEW_REQUIRED_ACCEPTABLE ou BLOCKED_ACCEPTABLE
payload_id / payload_hash non déjà présents dans 🧾 DECISION_JOURNAL
```

## 🔒 Garde-fous

```text
HUMAN_REVIEW_ONLY
NO_AUTO_ORDER
NO_AUTO_SIZING
NO_BROKER_EXECUTION
NO_REAL_ORDER
NO_SECRET
NO_TRIGGER
NO_MENU_MUTATION
NO_EXTERNAL_CALL
```

## 🧠 Signification de Gem / GEM

Dans ce MVP, `gem_profile` ne veut pas dire obligatoirement “Google Gemini Gem”.

Il signifie plutôt :

```text
profil d’exécution IA attendu
```

Exemples :

```text
GEM_GENERAL_REVIEW
GEM_SIGNAL_REVIEW
GEM_RISK_REVIEW
GEM_LEXIQUE_EDUCATIONAL
```

Pour l’usage quotidien, le champ important reste :

```text
ai_runtime_id
```

Exemple :

```text
nomGEM_FULL_REVIEW_001
```
