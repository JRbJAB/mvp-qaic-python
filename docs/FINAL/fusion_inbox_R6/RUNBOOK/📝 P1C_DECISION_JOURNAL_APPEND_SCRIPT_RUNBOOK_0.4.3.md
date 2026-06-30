# 📝 RUNBOOK — P1-C Decision Journal Append Script 0.4.3

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App  
> **Version :** `MVP_QAIC_P1C_DECISION_JOURNAL_APPEND_SCRIPT_0.4.3`  
> **Date :** 2026-06-11  
> **Statut :** `P1C_DECISION_JOURNAL_APPEND_SCRIPT_READY_FOR_DRIVE_REVIEW`  
> **Base :** P1-C 0.4.2 Full Fusion  

---

## 1. 🎯 Objectif

Ajouter automatiquement et une seule fois l’entrée test P1-C dans `DECISION_JOURNAL`.

Le module est :

```text
append-only
idempotent
sans ordre broker
sans sizing
sans exécution réelle
sans secret
```

---

## 2. Fichier Apps Script

```text
03_APPS_SCRIPT/apps_script/mvpqaic_09_p1c_decision_journal_append.gs
```

---

## 3. Fonctions publiques

```javascript
MVPQAIC_P1C_AppendFirstAuditJournalEntry()
MVPQAIC_P1C_JournalStatus()
```

---

## 4. Séquence recommandée

```text
1. Coller le script complet dans Apps Script.
2. Exécuter MVPQAIC_P1C_JournalStatus().
3. Vérifier DECISION_JOURNAL présent.
4. Exécuter MVPQAIC_P1C_AppendFirstAuditJournalEntry().
5. Relancer MVPQAIC_P1C_JournalStatus().
6. Vérifier ALREADY_EXISTS si relancé.
```

---

## 5. Logique payload_id

Le script tente de récupérer automatiquement :

```text
dernière ligne VALIDATED de GPT_INPUT_PAYLOADS
```

Fallback si introuvable :

```text
GPTP-TO_CONFIRM_FROM_SHEET
```

---

## 6. CSV fallback

Fichier :

```text
02_SHEETS/EXPORTS_CSV/DECISION_JOURNAL_P1C_TEST_ENTRY_0.4.3.csv
```

Usage :

```text
import manuel uniquement si tu ne veux pas exécuter le script
```

---

## 7. No-Go

Bloquer si :

```text
DECISION_JOURNAL absent
headers incohérents impossibles à corriger
secret détecté
champ ordre/sizing demandé
```
