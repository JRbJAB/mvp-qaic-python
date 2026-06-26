# P_REFLEX_12F_R14 — Backward Compatibility Migration OS

But: stabiliser le contrat Migration OS sans regression UI.

- `migration_os.py` porte le noyau de donnees stable.
- `migration_tracker.py` conserve les marqueurs publics attendus par les tests R9B/R10/R11.
- La vue visible conserve `Type | Source | Cible | % | Statut`, `AVG` et `ROWS`.
- Les 15 lignes historiques sont conservees.
- Les donnees vivantes de la matrice globale sont ajoutees en essentiel seulement.
- Les fonctions brutes Apps Script sont dedoublonnees et non affichees en spam.
