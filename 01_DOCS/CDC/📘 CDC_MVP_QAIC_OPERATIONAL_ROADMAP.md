# CDC — MVP QAIC Operational Roadmap

## Objectif produit

Construire une boucle opérateur exploitable pour revue crypto éducative et support décisionnel :
entrée portfolio/capture, prompt GEM, réponse GEM, review queue, entrée journal locale.

## Hors périmètre

- Trading automatique.
- Ordres broker.
- Sizing automatique.
- Accès Revolut X réel depuis MVP.
- `NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.
- Écriture Google Sheets sans décision explicite séparée.

## Roadmap opérationnelle

| Version | Horizon | Objectif | Critère d'acceptation |
|---|---:|---|---|
| V0.1 | fait | Boucle GEM locale | P118-P122 scellés |
| V0.2 | 1-3 jours | Premier vrai test opérateur | vrai portfolio + vraie réponse GEM + journal local |
| V0.3 | 3-7 jours | Ergonomie locale | helper d'entrée + dossiers run propres |
| V0.4 | 1-2 semaines | Mini cockpit local | interface simple input -> prompt -> capture -> journal |
| V0.5 | 2-4 semaines | Pont MVP vers QAIC privé | export propre sans ordre ni sizing |
| V0.6 | 3-5 semaines | Portfolio review usuel | templates par cas d'usage |
| V0.7 | 4-6 semaines | Historique et qualité | registry runs + métriques erreurs |
| V1.0 | 4-8 semaines | Version opérationnelle contrôlée | usage quotidien stable et auditable |

## Definition of Done V1.0

- Run quotidien en moins de 5 minutes.
- Prompt GEM généré depuis input local.
- Réponse GEM capturée.
- Missing data et blockers visibles.
- Journal local généré.
- Aucune action live implicite.
- Séparation MVP public / QAIC privé respectée.
