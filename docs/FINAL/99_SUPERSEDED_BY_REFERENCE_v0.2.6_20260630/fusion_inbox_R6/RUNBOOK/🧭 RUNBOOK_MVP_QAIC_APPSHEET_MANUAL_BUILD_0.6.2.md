# 🧭 Runbook — MVP QAIC AppSheet & contrôles manuels — 0.6.2 REAL FUSION REPAIR

> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION`  
> **Mode :** `HUMAN_REVIEW_ONLY`  
> **AppSheet :** build manuel non déployé.

## 1. Contrôle Data / Tables

| Table | Permission cible | Delete | Statut |
|---|---|---|---|
| SEARCH_COCKPIT | Read-only | OFF | OK |
| LEXIQUE_MASTER | Read-only | OFF | OK |
| PROMPT_LEXIQUE_BRIDGE | Read-only | OFF | REVIEW clé |
| PROMPT_CONTEXT_PACKS | Read-only | OFF | REVIEW clé/colonnes |
| PROMPT_LIBRARY | Read-only | OFF | OK |
| PROMPT_READY_TO_COPY | Read-only | OFF | REVIEW clé |
| PROMPT_RUN_QUEUE | Adds/updates contrôlés | OFF | OK |
| RESPONSE_INTAKE_QUEUE | Adds/updates contrôlés | OFF | OK |
| JOURNAL_APPEND_QUEUE | Adds/updates contrôlés ou read-only selon test | OFF | OK |
| DECISION_JOURNAL | Read-only | OFF | OK |

## 2. Contrôle UX / Views

| Vue | Source | Check |
|---|---|---|
| MVP QAIC Home | SEARCH_COCKPIT | Recherche visible |
| Lexique | LEXIQUE_MASTER | Consultation terme/méthode/signal |
| Prompts Ready | PROMPT_READY_TO_COPY | Prompt copiable |
| Run Queue | PROMPT_RUN_QUEUE | Prompt + réponse visible |
| Decision Journal | DECISION_JOURNAL | Audit read-only |

## 3. Contrôle workflow manuel

| Étape | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir Run Queue | prompt_to_copy visible |
| 2 | Copier prompt | Envoi manuel vers Gem/ChatGPT |
| 3 | Coller réponse | Response Intake / champ réponse |
| 4 | Revue blockers | Missing data et blockers visibles |
| 5 | Journaliser | Decision Journal read-only après append |

## 4. Contrôle futur Portfolio/Broker

| Étape | Autorisé maintenant | Autorisé plus tard |
|---|---|---|
| Portfolio Revolut X read-only | Oui, à construire | Oui |
| Alertes risque | Oui | Oui |
| Manual Trade Ticket | Oui | Oui |
| Paper trading | Préparation | Oui |
| Dry-run broker | Non AppSheet / oui QAIC Python futur | Oui après gates |
| Ordre réel | Non | Seulement projet séparé gated |
| TP/SL/trailing live | Non | Seulement QAIC Python/backend sécurisé |

## 5. Réponse obligatoire si blocker

```text
BLOCKED / REVIEW_REQUIRED
missing_data = ...
blockers = ...
no_order_no_sizing = TRUE
```
