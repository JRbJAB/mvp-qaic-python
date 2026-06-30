# 🧭 Instructions impératives UI — MVP QAIC — 1.0.2

## Statut
`MANDATORY_UI_STANDARD_ACTIVE`

## Règle permanente
Chaque onglet visible du MVP QAIC doit être un cockpit opérationnel lisible, pas une table brute.

## Obligatoire pour chaque onglet visible
- Colonnes essentielles à gauche, audit/détails à droite.
- Hauteur de ligne forcée compacte pour les lignes simples : `24 px` par défaut.
- Textes longs en `CLIP`, pas en wrap massif qui gonfle les lignes.
- Largeurs de colonnes maîtrisées par script.
- Freeze utile, limité, sans bloquer la navigation horizontale.
- Filtres activés sur la ligne d’en-tête utile.
- Couleurs métier cohérentes : OK vert, REVIEW orange, BLOCKED/INVALID rouge, informations bleu/gris.
- Zéro ligne blanche décorative.
- Aucun nouvel onglet UI sans nécessité démontrée.
- Toute fonction qui crée, rafraîchit ou modifie un onglet visible doit appeler son formatteur UI en dernier.

## Onglets prioritaires actuels
- `🧪 GPT_RESPONSE_INTAKE` : cockpit de test Gem/GPT.
- `🧾 DECISION_JOURNAL` : journal officiel, ouvert automatiquement après journalisation.
- `🧭 PROMPT_IMPROVEMENT_QUEUE` : lecture prioritaire du `next_prompt_draft`.
- `📘 PROMPT_LIBRARY` : lecture prioritaire de `prompt_template_to_copy`.

## Règle spéciale DECISION_JOURNAL
`MVPQAIC_JournalAppendFromIntake()` doit :
1. bloquer les lignes incomplètes ;
2. ajouter une ligne complète uniquement ;
3. appliquer l’ergonomie ultime ;
4. ouvrir automatiquement `🧾 DECISION_JOURNAL` sur la ligne ajoutée.

## Règle spéciale mémoire projet
Cette règle UI est prioritaire pour tous les futurs scripts MVP QAIC / QAIC / QAIT : pas de livraison “fonctionnelle mais illisible”.
