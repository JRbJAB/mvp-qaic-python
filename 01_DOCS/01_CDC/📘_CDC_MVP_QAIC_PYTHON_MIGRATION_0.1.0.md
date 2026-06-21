# 📋 CDC — Migration MVP QAIC vers Python 0.1.0

## 🎯 Objet et résultat attendu

Préparer une architecture Python compatible avec le MVP Google Sheets / Apps Script / WebApp, sans remplacer le MVP ni introduire de moteur de trading. Le lot P0.7.6 livre uniquement la référence, les limites et la procédure de migration.

## ✅ Exigences fonctionnelles

- Conserver le MVP **Lexique / KB / WebApp first**.
- Inventorier en P1 les sources Apps Script, Sheets, WebApp et Lexique/KB sous forme de miroir documentaire.
- Formaliser en P2 les contrats de données, prompts et runtime.
- Préparer en P3 un squelette de package sans logique live.
- Produire en P4 des rapports CLI locaux en lecture seule.
- Couvrir en P5 les validations unitaires, contractuelles et d’intégration hors live.
- Encadrer en P6 l’export/import par contrôles, diff et approbation humaine.
- Garder en P7 le bridge QAIC avancé optionnel, séparé et désactivé par défaut.

## 🧩 Domaines à migrer

1. Lexique KB : entrées, alias, catégories, statut et provenance.
2. Prompt library : identifiants, versions, variables, règles et tests.
3. Decision journal : décisions, contexte, horodatage et traçabilité.
4. GPT response intake : enveloppe, parsing, validation et quarantaine.
5. Quality dashboard : métriques calculées depuis des données validées.
6. WebApp readiness : vues, contrats d’API future et checks de préparation.
7. Bridges AppSheet / Looker / Stitch / Antigravity : adaptateurs futurs, sans couplage au cœur.

## 🛡️ Exigences non fonctionnelles

- Lecture seule par défaut, sorties locales, déterministes et auditables.
- Validation stricte des schémas et rejet explicite des données invalides.
- Aucun secret dans le dépôt ou les exports.
- Journalisation sans données sensibles.
- Compatibilité des formats documentée et versionnée.
- Rollback par abandon des artefacts Python et retour à la source MVP inchangée.

## ⛔ Hors périmètre

Auto-trading, broker, ordres, sizing, API Revolut, moteur QAIC avancé intégré, mutation live, écriture Google Sheets, déploiement Apps Script et gestion de secrets.

## 📏 Critères d’acceptation P0

- Arborescence de référence présente.
- Documents P0.7.6 et manifeste présents.
- Mapping des domaines et phases P0 à P7 défini.
- Garde-fous et procédure de rollback documentés.
- Aucune action live ou code Python exécutable créé.

## 🧾 Compte rendu batch

Chaque lot doit exposer : `STATUS`, `SOURCE_OF_TRUTH`, `SCOPE`, `ACTIONS_DONE`, `OUTPUTS_CREATED`, `SAFETY_FLAGS`, `BLOCKERS`, `NEXT`.
