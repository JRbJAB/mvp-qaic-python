# 🧭 RUNBOOK — MVP QAIC Crypto Signal OS 0.3.0

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App  
> **Version :** `MVP_QAIC_DOCS_P0B6_GOVERNANCE_0.3.0`  
> **Date :** 2026-06-11  
> **Statut :** `P0B6_GOVERNANCE_READY_FOR_DRIVE_REVIEW`  
> **Format :** Markdown `.md`  
> **Base source :** CDC / Planning / Instructions `0.2.2_ANTIGRAVITY_P0_PROCESS_READY`  


---

## 1. 🎯 Objectif du runbook

Ce runbook décrit les opérations sûres pour exploiter le MVP QAIC :

```text
installer
importer
vérifier
générer un payload GPT
auditer un prompt
préparer AppSheet
journaliser
```

---

## 2. 🔒 Règles de sécurité avant toute action

```text
HUMAN_REVIEW_ONLY
NO_AUTO_ORDER
NO_AUTO_SIZING
NO_BROKER_EXECUTION
NO_REAL_ORDER
NO_SECRET_IN_SHEET
NO_SECRET_IN_APPS_SCRIPT
NO_TRADING_BOT
NO_AUTOMATIC_TRAILING_ORDER
REVOLUT_X_READONLY_ONLY
```


---

## 3. ✅ Statuts rapides à lancer

### P0-B4 / P0-B5 / Mapping

```javascript
MVPQAIC_P0B4_Status()
MVPQAIC_P0B5_Status()
MVPQAIC_Status_FullSignalMapping_50_50()
```

### Résultat attendu

```text
P0-B4 tables = OK
P0-B5 tables = OK
SIGNAL_EVALUATION_RULES = 50 / OK
QAIC_SIGNAL_MAPPING >= 50 / OK
QAIC_SIGNAL_MAPPING_COVERAGE = 50 / OK
```

---

## 4. 🧠 Générer un payload GPT complet

### Payload complet trading review

```javascript
MVPQAIC_BuildFullTradePlanPrompt()
```

### Payload buy analysis

```javascript
MVPQAIC_BuildBuyTradePlanPrompt()
```

### Vérifier la sortie

Onglet :

```text
GPT_INPUT_PAYLOADS
```

Dernière ligne attendue :

```text
source_mode = MVP_QAIC_P0B5_TRADE_PLAN_EXTENSION
status = READY_FOR_MANUAL_COPY_PASTE
validation_status = VALIDATED
```

---

## 5. 🧪 Checklist payload GPT

Le prompt doit contenir :

```text
A. Niveau d’analyse réellement utilisé
B. Scoring QAIC demandé
C. Signaux QAIC utilisés
D. Plan / décision
E. Garde-fous
P0-B5 — Trade Plan Methods & Trailing Logic Extension
Méthode de calcul obligatoire
Token Type Profiles
Trade Plan Methods
TP/SL Calculation Rules
Trailing Playbook
Position Follow-up Rules
```

Si une section manque :

```text
STOP
ne pas copier au GPT
corriger script ou tables
```

---

## 6. 🧾 Copier vers GPT Crypto

Procédure actuelle :

```text
1. Ouvrir GPT_INPUT_PAYLOADS
2. Copier generated_prompt de la dernière ligne validée
3. Coller dans GPT Crypto
4. Lire la réponse
5. Vérifier aucune invention de prix/TP/SL
6. Journaliser la décision humaine
```

---

## 7. 📝 Journaliser une décision

Onglet cible :

```text
DECISION_JOURNAL
```

Champs recommandés :

```text
journal_id
timestamp
payload_id
prompt_id
asset
analysis_level
decision_status
scores_summary
signals_summary
missing_data
blockers
human_final_decision
notes
run_id
validation_status
```

---

## 8. 🔌 Portfolio / Revolut X read-only

Tant que `PORTFOLIO_SNAPSHOT` est vide, le payload doit indiquer :

```text
NO_PORTFOLIO_ROWS
ne pas inventer positions, PRU, PnL ou exposition
```

Quand QAIC/Revolut X read-only est disponible :

```text
QAIC/Revolut X read-only
→ PORTFOLIO_SNAPSHOT
→ MVPQAIC_BuildFullTradePlanPrompt()
→ GPT_INPUT_PAYLOADS
```

---

## 9. 🚫 Erreurs courantes

| Symptôme | Cause probable | Action |
|---|---|---|
| `Logging output too large` | Prompt long | Vérifier `GPT_INPUT_PAYLOADS`, pas les logs |
| `NO_PORTFOLIO_ROWS` | Snapshot vide | Normal si aucune position importée |
| `SCORE_NOT_AVAILABLE` | Données insuffisantes | Normal, ne pas forcer |
| `REVIEW_REQUIRED` | Donnée critique absente | Normal |
| `BLOCKED` | SL absent ou blocker critique | Normal |
| Fonctions P0-B5 ne trouvent pas P0-B4 | P0-B4 0.2.8 non installé | Remplacer script P0-B4 |
| Mapping < 50 | Full signal mapping non lancé | Lancer `MVPQAIC_Install_FullSignalMapping_50_50()` |

---

## 10. 🔜 Passer à AppSheet P0-C

Avant P0-C :

```javascript
MVPQAIC_P0B5_Status()
MVPQAIC_Status_FullSignalMapping_50_50()
MVPQAIC_BuildFullTradePlanPrompt()
```

Critères :

```text
GPT_INPUT_PAYLOADS dernière ligne VALIDATED
SIGNAL_EVALUATION_RULES 50 OK
QAIC_SIGNAL_MAPPING_COVERAGE 50 OK
aucune fonction d’ordre broker
```
