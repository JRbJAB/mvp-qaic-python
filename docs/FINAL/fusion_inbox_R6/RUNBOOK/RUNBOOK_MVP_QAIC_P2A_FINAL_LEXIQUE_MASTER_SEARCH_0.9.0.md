# 📚 MVP QAIC — P2-A FINAL Lexique Master + Search Cockpit — Runbook 0.9.0

## Objectif
Créer uniquement deux onglets frontend générés :

- `📚 LEXIQUE_MASTER`
- `🔎 SEARCH_COCKPIT`

Le script lit les sources existantes, sans créer de bases parallèles.

## Script
Ajouter dans Apps Script :

`mvpqaic_31_lexique_master_search_cockpit_core.gs`

Supprimer manuellement l'ancien script raté si présent :

`mvpqaic_30_lexique_methods_signals_core.gs`

## Fonctions à lancer

```javascript
MVPQAIC_LexiqueMasterVersion()
MVPQAIC_LexiqueMasterStatus()
MVPQAIC_LexiqueMasterRunAllFast()
```

Puis, pour rechercher : modifier `B2:B5` dans `🔎 SEARCH_COCKPIT`, puis relancer :

```javascript
MVPQAIC_SearchCockpitRefresh()
```

## Sécurité
Aucun delete/hide/menu/trigger/network/broker/order/sizing/secret.
