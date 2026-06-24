# MVP QAIC P202 — Navigation IA Audit & Stitch Brief

## Diagnostic

Le menu actuel est trop plat. Il mélange routes Python, futurs onglets Sheets, suivi migration, documentation, diagnostics, GEM, release et pages legacy. Résultat : l'utilisateur ne sait plus où cliquer, ni quelles pages sont utiles au quotidien.

## Principe cible

La navigation doit être organisée en 5 espaces :

1. Command Center : état global, prochaines actions, blockers, KPIs.
2. Utiliser l'outil : flux prompt/capture/réponse/review/décision.
3. Cockpits Sheets utiles : vrais onglets Sheets à créer/importer plus tard.
4. Administration & Migration : migration-control, docs, obligations, Apps Script map.
5. Release & Diagnostics : gates, runtime contract, release final, safety.

## Règles UI obligatoires

- Sidebar gauche collapsible, workspace-level.
- Top bar avec action courante, statut, environnement local/private, bouton stop/update.
- Dans chaque page : résumé en haut, puis tableau principal.
- Tableaux : recherche ouverte, filtres, tri, pagination, colonnes courtes, pas de troncature des accents.
- Toujours montrer : status, next_action, blockers, evidence, write_policy.
- Les futurs onglets Sheets doivent être nommés comme des onglets Sheets, pas comme des routes Python.
- Les routes legacy doivent être masquées ou fusionnées.

## Brief Stitch futur

### Layout

- Header compact : nom produit, statut local, prochaine action.
- Sidebar collapsible : 5 espaces seulement.
- Main area : largeur maximale, cards synthèse, tableau utile.
- Right drawer optionnel : aide/context docs.

### Pages Stitch prioritaires

1. Command Center
2. Utiliser l'outil
3. Cockpits Sheets
4. Migration Control
5. Instructions & Docs
6. Release Gate

### Palette

- Vert : prêt / validé
- Orange : review / waiting input
- Rouge : blocked / forbidden / live write interdit
- Bleu : info / local private
- Violet : futur / post-Python

### Typographie

- Police UI compatible accents : Segoe UI / Inter / Noto Sans.
- Tables : 13–14px, line-height 1.4, no clipping.
- Titres métiers en français, enums techniques conservées.

## Décision

Ne pas finaliser visuellement dans NiceGUI avant cette refonte IA. NiceGUI reste cockpit privé. Stitch viendra ensuite pour industrialiser l'UI.

## Next

P203_NAV_SIDEBAR_WORKSPACE_REFACTOR_OR_STITCH_PREP
