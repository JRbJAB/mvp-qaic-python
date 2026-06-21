# 🏗️ Architecture cible MVP QAIC Python 0.1.0

## 🧭 Positionnement

Le MVP Sheets / Apps Script / WebApp reste le système fonctionnel de référence pour le Lexique et la KB. Python devient progressivement une couche locale d’ingestion, validation, contrats, tests, CLI et rapports. Le moteur QAIC avancé est un système distinct, raccordable plus tard par un bridge P7.

## 🧱 Couches cibles

| Couche | Responsabilité | Règle |
|---|---|---|
| Sources MVP | Sheets, Apps Script, WebApp | Source explicitement nommée, non mutée |
| Ingestion | Lecture d’exports versionnés | Aucun accès live implicite |
| Contrats | Données, prompts, runtime | Validation avant transformation |
| Domaine | Lexique, prompts, journal, intake, qualité | Sans broker ni trading engine |
| Présentation | CLI et rapports locaux | Lecture seule |
| Bridges | WebApp et outils externes | Adaptateurs isolés, désactivés par défaut |
| QAIC bridge | Interface vers moteur avancé | P7 optionnel, contrat strict |

## 📁 Responsabilités des dossiers

- `02_SOURCE_MAPS/` : inventaires et correspondances de sources.
- `03_CONTRACTS/` : schémas versionnés et invariants.
- `04_PYTHON_STAGING/` : plans de package, tests et CLI, sans exécution au P0.
- `05_EXPORTS/` : futurs exports contrôlés, jamais des secrets.
- `06_REPORTS/` : preuves de lots et manifestes.
- `07_ARCHIVES/` : snapshots documentaires non destructifs.
- `99_SANDBOX_NO_LIVE/` : essais isolés sans accès live.

## 🔄 Flux futur autorisé

```text
Export approuvé → empreinte → ingestion locale → validation contrat
→ normalisation → tests → rapport read-only → revue humaine
```

Le flux inverse d’import reste interdit avant P6 et nécessite un plan, un diff, une sauvegarde source, un `GO` humain et une procédure de rollback vérifiée.

## 🔌 Bridges

- **AppSheet** : vues et synchronisation via contrat, jamais directement depuis le domaine.
- **Looker** : datasets de reporting validés et read-only.
- **Stitch** : échange par formats versionnés et idempotents.
- **Antigravity** : adaptateur nommé et isolé jusqu’à clarification de son contrat.
- **WebApp** : readiness checks et DTO stables avant toute intégration.

## 🛡️ Sécurité et rollback

Aucun auto-trading, broker, ordre, sizing, Revolut API ou écriture live. En erreur : arrêter le lot, conserver les preuves, invalider la sortie, ne pas toucher aux sources, restaurer uniquement depuis un snapshot approuvé si une phase future autorise une mutation.
