# 🧹 RUNBOOK — P1-D Journal Cleanup / Duplicate Guard 0.4.5

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App  
> **Version :** `MVP_QAIC_P1D_JOURNAL_CLEANUP_DUPLICATE_GUARD_0.4.5`  
> **Date :** 2026-06-11  
> **Statut :** `P1D_JOURNAL_CLEANUP_DUPLICATE_GUARD_READY_FOR_REVIEW`  
> **Base :** P1-C 0.4.4 Full Fusion  

---

## 1. 🎯 Objectif

Traiter proprement le cas observé :

```text
row 2 = tentative partielle 0.4.3
row 3 = entrée officielle valide 0.4.4
```

P1-D ajoute :

```text
dry-run audit
détection lignes partielles
détection doublons journal_id
marquage DEPRECATED optionnel
aucune suppression automatique
```

---

## 2. Fichier Apps Script

```text
03_APPS_SCRIPT/apps_script/mvpqaic_10_p1d_journal_cleanup_duplicate_guard.gs
```

---

## 3. Fonctions publiques

```javascript
MVPQAIC_P1D_JournalCleanupDryRun()
MVPQAIC_P1D_MarkPartialRowsDeprecated()
```

---

## 4. Séquence recommandée

### Étape 1 — audit sans écriture

```javascript
MVPQAIC_P1D_JournalCleanupDryRun()
```

Résultat attendu si row 2 existe encore :

```text
partial_rows_count >= 1
official_p1c_rows_count = 1
```

### Étape 2 — marquer les lignes partielles

```javascript
MVPQAIC_P1D_MarkPartialRowsDeprecated()
```

Cette fonction :

```text
ne supprime rien
écrit validation_status = DEPRECATED sur les lignes partielles
ajoute une note si la colonne notes existe
```

### Étape 3 — vérifier

```javascript
MVPQAIC_P1D_JournalCleanupDryRun()
```

---

## 5. Suppression manuelle possible

Si tu préfères un journal propre :

```text
supprimer row 2 manuellement
garder row 3
```

C’est acceptable car row 2 est une écriture partielle non officielle.
