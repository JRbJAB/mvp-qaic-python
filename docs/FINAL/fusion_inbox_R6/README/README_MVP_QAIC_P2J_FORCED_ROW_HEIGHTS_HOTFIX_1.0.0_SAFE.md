# 🛠️ MVP QAIC — P2-J Forced Row Heights Hotfix 1.0.0 SAFE

## Objectif
Corriger définitivement les hauteurs de lignes dans `🧭 PROMPT_IMPROVEMENT_QUEUE` et `📘 PROMPT_LIBRARY`.

## Correction
- Utilise `setRowHeightsForced(...)` quand disponible.
- Applique `WrapStrategy.CLIP` sur la plage affichée.
- Force les hauteurs en dernier, après remap, filtres, validations, couleurs et largeurs.
- Garde `next_prompt_draft` et `prompt_template_to_copy` en largeur normale `420 px`.
- Ne crée aucun onglet, aucun trigger, aucune mutation menu, aucun delete/hide.

## Installation
Remplacer uniquement :

```text
mvpqaic_11_p1_prompt_quality_core.gs
```

Puis lancer :

```javascript
MVPQAIC_PromptWorkflowSheetsOptimize()
```

## Attendu
Le résultat doit mentionner :

```text
row_height_forced: 24
wrap_strategy: CLIP
```
