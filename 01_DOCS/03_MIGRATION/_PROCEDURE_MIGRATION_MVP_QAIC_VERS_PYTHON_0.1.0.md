# 🚚 Procédure de migration MVP QAIC vers Python 0.1.0

## 🔐 Préconditions communes

1. Nommer la source de vérité et son propriétaire.
2. Fixer le périmètre, la version, les formats et critères d’acceptation.
3. Vérifier qu’aucun secret n’entre dans les artefacts.
4. Travailler sur exports ou miroirs locaux, jamais sur le live par défaut.
5. Produire le compte rendu batch standard et obtenir la revue requise.

## 🪜 Phases et portes de contrôle

| Phase | Actions | Gate de sortie |
|---|---|---|
| P0 Référence | Docs, architecture, procédure, manifeste | Revue documentaire |
| P1 Inventaire | Miroir des fichiers, feuilles, routes et objets KB | Couverture et provenance vérifiées |
| P2 Contrats | Schémas, contraintes, exemples valides/invalides | Validation métier et technique |
| P3 Squelette | Plan des modules, dépendances et interfaces | Aucun comportement live |
| P4 CLI read-only | Import local, validation, rapports | Zéro mutation externe |
| P5 Tests | Unitaires, contrats, fixtures, non-régression | Suite reproductible au vert |
| P6 Export/import | Diff, approbation, sauvegarde, import contrôlé | `GO` humain explicite |
| P7 Bridge QAIC | Interface optionnelle et isolée | Désactivée par défaut, revue sécurité |

## 🔍 Procédure par lot

1. Capturer l’identifiant et l’empreinte de l’export source.
2. Copier seulement dans la zone de staging autorisée.
3. Valider encodage, colonnes, types, clés et cardinalités.
4. Transformer de façon déterministe et idempotente.
5. Comparer totaux, clés, erreurs et changements attendus.
6. Générer un rapport local et classer les rejets en quarantaine.
7. Faire approuver tout passage vers une destination live.
8. Archiver le rapport ; ne jamais supprimer la source.

## ↩️ Rollback

- P0 à P5 : abandonner les sorties locales invalides ; le MVP reste inchangé.
- P6 : arrêter à la première divergence, ne pas poursuivre partiellement, appliquer uniquement le plan de restauration pré-approuvé.
- P7 : désactiver le bridge et revenir au fonctionnement MVP autonome.
- Toujours conserver manifeste, empreintes, logs expurgés, diff et décision humaine.

## 🚨 Règles d’arrêt

Bloquer toute mutation si la source de vérité, le contrat, la destination, l’autorisation, le snapshot ou le rollback est absent. Sont toujours interdits dans ce référentiel : auto-trading, broker, ordres, sizing, Revolut API, secrets et écritures live sans `GO`.

## 🧾 Format batch

```text
STATUS
SOURCE_OF_TRUTH
SCOPE
ACTIONS_DONE
OUTPUTS_CREATED
SAFETY_FLAGS
BLOCKERS
NEXT
```
