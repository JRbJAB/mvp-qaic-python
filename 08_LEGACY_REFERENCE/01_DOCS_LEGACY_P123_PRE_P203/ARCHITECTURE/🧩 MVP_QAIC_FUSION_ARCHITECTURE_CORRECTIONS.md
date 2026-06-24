# MVP QAIC — Fusion réelle et corrections d'architecture

## Fusion réelle

La fusion validée est documentaire, produit et opératoire. Elle ne fusionne pas les responsabilités
d'exécution trading entre MVP et QAIC backend.

- MVP QAIC : lexique, méthodes, prompts, WebApp/UI future, review opérateur.
- QAIC backend : calcul privé, scoring, risk, providers, Revolut X, execution-capable locked.

## Corrections techniques intégrées

- P119 parse JSON robuste : BOM, texte brut, code fence JSON.
- P119 déduplication des blockers entre payload explicite et détection texte.
- P121 smoke end-to-end local vérifie P118 -> P119 -> P120.
- P122 stop pack impose l'arrêt après handoff sauf demande explicite.

## Interdiction permanente côté MVP

- `NO_BROKER`.
- `NO_ORDER`.
- `NO_AUTO_SIZING`.
- `NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.
