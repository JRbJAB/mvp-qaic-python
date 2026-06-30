# 🧠 DECISION JOURNAL — Usage futur & Prompt Improvement Loop 0.4.6

## 1. À quoi sert le journal ?

Le journal sert à transformer les réponses GPT et QAIC en données exploitables :

```text
prompt_id
payload_id
réponse GPT auditée
scores
signaux
données manquantes
blockers
décision humaine
résultat attendu
```

## 2. Correction des prompts

Le journal permet de détecter :

```text
signal_id absents
scores non justifiés
blockers oubliés
format de sortie non respecté
données inventées
SL absent
confiance trop élevée
```

Ces anomalies alimentent :

```text
PROMPT_LIBRARY
GPT_PROMPT_RUNTIME_SPEC
OUTPUT_TEMPLATES
GPT_RESPONSE_AUDIT_PROMPT
```

## 3. Qualité data

Les champs `missing_data` et `blockers` permettent de prioriser :

```text
portfolio snapshot
prix
volume
BTC regime
spread
funding / OI
TVL
unlocks
source freshness
```

## 4. Cockpit AppSheet / dashboard

Le journal devient source pour :

```text
% réponses validées
% REVIEW_REQUIRED
% BLOCKED
top missing_data
top blockers
tokens souvent rejetés
prompts à améliorer
```

## 5. Règle de gouvernance

```text
Aucune décision ne devient exploitable sans entrée journal et audit.
```
