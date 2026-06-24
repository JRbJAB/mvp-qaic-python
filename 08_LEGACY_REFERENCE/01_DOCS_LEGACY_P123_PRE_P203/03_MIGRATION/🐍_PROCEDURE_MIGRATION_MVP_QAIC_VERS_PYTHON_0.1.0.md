# 🗺️ Mapping Apps Script vers modules Python 0.1.0

Ce mapping est une cible de conception, pas du code exécutable. Les noms finaux sont confirmés après l’inventaire P1.

| Domaine MVP | Cible Python proposée | Contrat principal | Sortie read-only |
|---|---|---|---|
| Lexique KB | `qaic_mvp.lexique` | entrée, alias, catégorie, provenance | rapport de cohérence |
| Prompt library | `qaic_mvp.prompts` | prompt versionné, variables, statut | catalogue validé |
| Decision journal | `qaic_mvp.decisions` | décision, contexte, horodatage | journal filtrable |
| GPT response intake | `qaic_mvp.gpt_intake` | enveloppe, payload, validation | rejets et synthèse |
| Quality dashboard | `qaic_mvp.quality` | métriques et dimensions | dashboard dataset |
| WebApp readiness | `qaic_mvp.webapp` | DTO, routes futures, checks | readiness report |
| AppSheet bridge | `qaic_mvp.bridges.appsheet` | échange versionné | aperçu de synchronisation |
| Looker bridge | `qaic_mvp.bridges.looker` | dataset analytique | export reporting |
| Stitch bridge | `qaic_mvp.bridges.stitch` | batch idempotent | journal d’échange |
| Antigravity bridge | `qaic_mvp.bridges.antigravity` | contrat à qualifier en P1/P2 | diagnostic uniquement |
| QAIC engine bridge | `qaic_mvp.bridges.qaic_engine` | interface P7 séparée | simulation hors live |

## 🔁 Correspondances techniques indicatives

| Apps Script / Sheets | Cible future | Condition |
|---|---|---|
| Fonctions de lecture de ranges | adaptateur d’ingestion d’exports | pas d’API Google au P0 |
| Validation de colonnes | modèles et validateurs de contrats | erreurs explicites |
| Triggers | commandes planifiées externes futures | aucun trigger live implicite |
| Propriétés / configuration | configuration typée | secrets hors dépôt |
| Logs | journal structuré expurgé | aucune donnée sensible |
| HTMLService / WebApp | DTO et couche présentation | découplée du domaine |

## ⛔ Exclusions

Aucun module broker, ordre, sizing, auto-trading ou Revolut. Le bridge QAIC n’appartient pas au package cœur et reste réservé à P7.
