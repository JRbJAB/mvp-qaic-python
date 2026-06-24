# P177 Operator Prompt Smoke — GEM Portfolio Image

Utilise le prompt MVP QAIC portfolio/image en mode review-only.

Contraintes:
- Ne pas passer d’ordre.
- Ne pas calculer de sizing automatique.
- Ne pas appliquer automatiquement la réponse GEM.
- Retourner REVIEW_REQUIRED si les données nécessaires manquent.
- Garder les enums techniques inchangés.

Entrée attendue:
- Capture écran portfolio crypto.
- Texte copié optionnel.

Sortie attendue:
- JSON structuré.
- Résumé français.
- missing_data.
- blockers.
- safety_audit.
