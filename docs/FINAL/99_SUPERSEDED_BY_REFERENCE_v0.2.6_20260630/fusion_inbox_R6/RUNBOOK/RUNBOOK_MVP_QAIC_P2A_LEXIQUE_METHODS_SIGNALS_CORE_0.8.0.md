# 🛠️ MVP QAIC — P2-A Lexique, Méthodes & Signaux Core 0.8.0

## Objectif
Créer la fondation Lexique-first du MVP QAIC avant toute évolution UI, prompts ou QAIC bridge.

## Script
`scripts/mvpqaic_30_lexique_methods_signals_core.gs`

## Fonctions publiques
```javascript
MVPQAIC_LexiqueVersion()
MVPQAIC_LexiqueStatus()
MVPQAIC_LexiqueSetup()
MVPQAIC_LexiqueRefresh()
MVPQAIC_LexiqueSearch()
MVPQAIC_LexiqueRunAllFast()
```

## Onglets créés/maintenus
- `📚 LEXIQUE_CRYPTO`
- `📈 METHODES_TRADING`
- `🚦 SIGNAUX_TRADING`
- `🧠 SIGNAL_RULES`
- `🔎 LEXIQUE_SEARCH`

## Ordre de run recommandé
```javascript
MVPQAIC_LexiqueVersion()
MVPQAIC_LexiqueStatus()
MVPQAIC_LexiqueRunAllFast()
```

## Sécurité
- `HUMAN_REVIEW_ONLY`
- `NO_AUTO_ORDER`
- `NO_AUTO_SIZING`
- `NO_BROKER_EXECUTION`
- `NO_EXTERNAL_NETWORK`
- `NO_SECRET_VALUE_READ`
- `NO_DELETE_HIDE_MENU_TRIGGER_MUTATION`

## Validation attendue
- `status = OK` pour `MVPQAIC_LexiqueRunAllFast()`
- 5 onglets P2-A présents
- lignes seed écrites : lexique, méthodes, signaux, signal rules
- aucun blocker
