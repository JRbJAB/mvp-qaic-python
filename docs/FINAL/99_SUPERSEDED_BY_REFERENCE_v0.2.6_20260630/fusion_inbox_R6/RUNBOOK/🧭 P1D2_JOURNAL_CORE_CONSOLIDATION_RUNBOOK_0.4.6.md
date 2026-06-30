# 🧭 RUNBOOK — P1-D2 Journal Core Consolidation 0.4.6

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App  
> **Version :** `MVP_QAIC_P1D2_JOURNAL_CORE_CONSOLIDATION_0.4.6`  
> **Date :** 2026-06-11  
> **Statut :** `P1D2_JOURNAL_CORE_CONSOLIDATION_READY_FOR_REVIEW`  
> **Base :** P1-D 0.4.5 Full Fusion  

---

## 1. 🎯 Objectif

Fusionner durablement :

```text
append P1-C
cleanup / duplicate guard P1-D
```

dans un seul script :

```text
mvpqaic_09_p1_journal_core.gs
```

---

## 2. Fonctions publiques

```javascript
MVPQAIC_JournalStatus()
MVPQAIC_JournalAppendFirstAuditEntry()
MVPQAIC_JournalCleanupDryRun()
MVPQAIC_JournalMarkPartialRowsDeprecated()
```

---

## 3. Séquence recommandée

```javascript
MVPQAIC_JournalStatus()
MVPQAIC_JournalCleanupDryRun()
MVPQAIC_JournalAppendFirstAuditEntry()
MVPQAIC_JournalStatus()
```

Si l’entrée existe déjà :

```text
ALREADY_EXISTS
```

---

## 4. Après suppression manuelle de row 2

Résultat attendu :

```text
partial_rows_count = 0
duplicate_journal_id_count = 0
official_p1c_rows_count = 1
p1_test_entry_exists = true
```

---

## 5. Rôle futur du journal

Le journal devient le registre qualité du MVP :

```text
audit GPT
décisions humaines
données manquantes
blockers
qualité prompts
priorisation intégrations QAIC
préparation dashboard
```
