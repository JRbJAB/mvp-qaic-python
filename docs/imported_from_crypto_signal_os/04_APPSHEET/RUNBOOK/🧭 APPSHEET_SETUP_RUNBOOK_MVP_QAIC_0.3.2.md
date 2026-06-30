# 🧭 APPSHEET SETUP RUNBOOK — MVP QAIC 0.3.2

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App  
> **Version :** `MVP_QAIC_APPSHEET_RUNBOOK_0.3.2`  
> **Date :** 2026-06-11  
> **Statut :** `P0C_APPSHEET_MVP_READINESS_READY_FOR_DRIVE_REVIEW`  

---

## 1. Préparation

Google Sheet source :

```text
🛠️ MVP QAIC — Crypto Signal OS — DEV
```

Avant création AppSheet, vérifier :

```javascript
MVPQAIC_P0B5_Status()
MVPQAIC_Status_FullSignalMapping_50_50()
MVPQAIC_BuildFullTradePlanPrompt()
```

---

## 2. Création AppSheet

1. Ouvrir AppSheet.
2. Créer une app depuis Google Sheets.
3. Sélectionner `🛠️ MVP QAIC — Crypto Signal OS — DEV`.
4. Laisser AppSheet détecter les tables.
5. Corriger les keys selon le document `TABLES_AND_COLUMNS`.
6. Mettre toutes les tables en read-only sauf `DECISION_JOURNAL`.

---

## 3. Configurer les accès

```text
Knowledge tables = READ_ONLY
Runtime payload tables = READ_ONLY
Bridge tables = READ_ONLY
DECISION_JOURNAL = ADDS_ONLY
```

---

## 4. Créer les vues

Ordre recommandé :

```text
Home
Knowledge Search
Methods
Signal Library
QAIC Signal Mapping
Trade Plan
GPT Payloads
Risk Center
Decision Journal
QAIC Bridge
```

---

## 5. Tester

Exécuter le test plan complet :

```text
04_APPSHEET/TESTS/🧪 APPSHEET_TEST_PLAN_MVP_QAIC_0.3.2.md
```

---

## 6. Ne pas publier si

```text
Buy/Sell/Execute visible
broker write possible
payload modifiable
tables sources éditables
secret visible
journal absent
```
