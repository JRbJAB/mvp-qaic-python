# P_REFLEX_12F_R12_MIGRATION_OS_CONSOLIDATION

Consolidation stable du Migration Tracker.

## Contrat

- `migration_os.py` porte la logique autonome Python.
- `migration_tracker.py` porte uniquement l'affichage Reflex.
- Les 15 lignes historiques sont preservees.
- L'UX tableau `Type / Source / Cible / % / Statut` est preservee.
- Les donnees globales restent vivantes via `MIGRATION_GLOBAL_MATRIX*.json`.
- Les 2738 fonctions brutes ne sont pas affichees dans Mission Control : elles sont dedoublonnees et agregees.
- `/migration/global` reste le drill-down detail.
