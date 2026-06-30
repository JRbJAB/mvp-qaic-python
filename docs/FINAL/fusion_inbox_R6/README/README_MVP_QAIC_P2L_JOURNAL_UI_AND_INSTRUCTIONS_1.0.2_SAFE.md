# MVP QAIC P2-L — Journal UI & Instructions 1.0.2 SAFE

## Fichiers
- `scripts/mvpqaic_23_gpt_response_intake_core.gs`
- `docs/INSTRUCTIONS_UI_IMPERATIVE_MVP_QAIC_1.0.2.md`

## À remplacer
Remplacer uniquement :
`mvpqaic_23_gpt_response_intake_core.gs`

## Fonctions utiles
- `MVPQAIC_JournalAppendFromIntake()` : journalise puis ouvre `🧾 DECISION_JOURNAL`.
- `MVPQAIC_JournalFormatUltimate()` : applique / réapplique l’ergonomie ultime du journal.
- `MVPQAIC_JournalMarkIncompleteAppends()` : marque les lignes incomplètes existantes sans suppression.

## Sécurité
- No delete.
- No hide.
- No trigger.
- No menu mutation.
- No broker/order/sizing/secret.
- Journal append bloqué si champs essentiels vides.
