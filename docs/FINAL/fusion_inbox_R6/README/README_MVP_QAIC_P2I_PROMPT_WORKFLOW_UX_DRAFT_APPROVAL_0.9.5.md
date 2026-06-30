# 🛠️ MVP QAIC — P2-I Prompt Workflow UX & Draft Approval — 0.9.5

## Objectif
Centraliser la boucle de test Gem dans `🧪 GPT_RESPONSE_INTAKE` et rendre lisibles les onglets `🧭 PROMPT_IMPROVEMENT_QUEUE` et `📘 PROMPT_LIBRARY`.

## Scripts à remplacer

```text
scripts/mvpqaic_11_p1_prompt_quality_core.gs
scripts/mvpqaic_23_gpt_response_intake_core.gs
```

## Fonctions ajoutées

```javascript
MVPQAIC_PromptWorkflowSheetsOptimize()
MVPQAIC_PromptDraftApplyApprovedToLibrary()
MVPQAIC_IntakeApplyApprovedDraftToLibrary()
```

## Boutons recommandés dans 🧪 GPT_RESPONSE_INTAKE

```text
👁️ Preview refs     → MVPQAIC_IntakePrepareRefs
🧪 Analyser réponse → MVPQAIC_IntakeAnalyzeRawResponse
🧾 Journaliser      → MVPQAIC_JournalAppendFromIntake
🔁 Boucle qualité   → MVPQAIC_IntakePostJournalPromptLoop
✅ Appliquer draft  → MVPQAIC_IntakeApplyApprovedDraftToLibrary
🆕 Nouveau test     → MVPQAIC_IntakeNewBlank
```

## Process compact

```text
1. 🧪 GPT_RESPONSE_INTAKE : choisir ai_runtime_id + prompt_id.
2. Cliquer 👁️ Preview refs.
3. Copier prompt_template_to_copy dans le Gem.
4. Coller la réponse Gem dans raw_response.
5. Cliquer 🧪 Analyser réponse.
6. Vérifier parse_status + mandatory_fields_missing_count.
7. Passer ready_to_journal = YES.
8. Cliquer 🧾 Journaliser.
9. Cliquer 🔁 Boucle qualité : dashboard + queue + draft + ouverture auto de 🧭 PROMPT_IMPROVEMENT_QUEUE.
10. Dans 🧭 PROMPT_IMPROVEMENT_QUEUE : vérifier next_prompt_draft.
11. Si validé humainement : mettre human_review_status = APPROVED_TO_LIBRARY.
12. Cliquer ✅ Appliquer draft.
13. Vérifier 📘 PROMPT_LIBRARY.prompt_template_to_copy.
14. Cliquer 🆕 Nouveau test et retester le Gem.
```

## Sécurité

```text
HUMAN_REVIEW_ONLY
NO_AUTO_PROMOTION
NO_DELETE
NO_HIDE
NO_TRIGGER
NO_MENU_MUTATION
NO_BROKER
NO_ORDER
NO_SIZING
NO_SECRET
```

Le draft n’est jamais promu tout seul : il est appliqué uniquement si `human_review_status = APPROVED_TO_LIBRARY` sur une ligne `ADAPTIVE_NEXT_PROMPT_DRAFT`.
