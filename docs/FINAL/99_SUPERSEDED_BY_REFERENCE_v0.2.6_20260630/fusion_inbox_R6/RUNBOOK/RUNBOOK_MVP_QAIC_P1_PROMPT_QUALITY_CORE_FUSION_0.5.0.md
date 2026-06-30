# 🛠️ MVP QAIC — Runbook P1 Prompt Quality Core Fusion 0.5.0

> **Version :** `MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.5.0_SAFE_FULL_FUSION_P1E_P1F`  
> **Date :** 2026-06-11  
> **Statut :** `SAFE_RUNTIME_READY_FOR_VALIDATION`

## 🎯 Objectif

Fusionner proprement P1-E et P1-F dans un seul script durable :

```text
mvpqaic_11_p1_prompt_quality_core.gs
```

Le core couvre :

```text
DECISION_JOURNAL → GPT_QUALITY_DASHBOARD → PROMPT_IMPROVEMENT_QUEUE
```

## 🔐 Sécurité

```text
HUMAN_REVIEW_ONLY
NO_BROKER
NO_ORDER
NO_SIZING
NO_SECRET
```

Le script lit uniquement :

```text
DECISION_JOURNAL
GPT_QUALITY_DASHBOARD
```

Le script écrit uniquement :

```text
GPT_QUALITY_DASHBOARD
PROMPT_IMPROVEMENT_QUEUE
```

## 🧩 Installation propre

### Cas recommandé

Remplacer l'ancien P1-E par le script fusionné :

```text
mvpqaic_11_p1_prompt_quality_core.gs
```

Ne pas garder durablement les anciens scripts live :

```text
mvpqaic_11_p1e_prompt_quality_dashboard.gs
mvpqaic_12_p1f_prompt_improvement_queue.gs
```

Après validation runtime, les archiver en ZIP/docs puis les retirer du live Apps Script.

## ✅ Ordre de test

### 1. Core status

```javascript
MVPQAIC_PromptQualityCoreStatus()
```

Attendu :

```text
status = OK
journal_sheet_exists = true
dashboard_sheet_exists = true/false
queue_sheet_exists = true/false
can_refresh_dashboard = true
safety = HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET
```

### 2. Dashboard status

```javascript
MVPQAIC_PromptQualityDashboardStatus()
```

Attendu :

```text
status = OK
journal_sheet_exists = true
journal_rows >= 1
can_refresh = true
```

### 3. Dashboard refresh

```javascript
MVPQAIC_PromptQualityDashboardRefresh()
```

Attendu :

```text
status = REFRESHED
dashboard_sheet = GPT_QUALITY_DASHBOARD
journal_rows >= 1
prompt_actions_count >= 1
safety = NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET
```

### 4. Queue status

```javascript
MVPQAIC_PromptImprovementQueueStatus()
```

Attendu :

```text
status = OK
source_sheet_exists = true
can_refresh = true
```

### 5. Queue refresh

```javascript
MVPQAIC_PromptImprovementQueueRefresh()
```

Attendu :

```text
status = REFRESHED
target_sheet = PROMPT_IMPROVEMENT_QUEUE
queue_rows_written >= 1
p0_count >= 1
p1_count >= 1
safety = HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET
```

## 🎨 UI Sheets obligatoire

Les onglets générés doivent rester des outils de décision :

```text
synthèse en haut
freeze rows/columns
filtres
colonnes décision/action à gauche
colonnes audit à droite
hauteur de ligne normale
largeurs adaptées
couleurs métier utiles
validations de listes
pas de ligne blanche décorative
```

## 🧭 Décision après validation

Si les 5 fonctions sont OK :

```text
P1-E + P1-F = VALIDÉ FUSION
```

Garder dans Apps Script live :

```text
mvpqaic_09_p1_journal_core.gs
mvpqaic_11_p1_prompt_quality_core.gs
```

Archiver / retirer du live :

```text
mvpqaic_11_p1e_prompt_quality_dashboard.gs
mvpqaic_12_p1f_prompt_improvement_queue.gs
```

## ⏭️ Suite logique

Après validation fusion :

```text
P1-G — Prompt Library / Prompt Contract Update
```
