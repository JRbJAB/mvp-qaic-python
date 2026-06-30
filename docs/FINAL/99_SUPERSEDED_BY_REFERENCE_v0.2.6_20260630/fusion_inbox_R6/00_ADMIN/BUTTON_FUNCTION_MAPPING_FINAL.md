# 🔘 Mapping final boutons → fonctions

## 🧪 GPT_RESPONSE_INTAKE
- 👁️ Preview refs → `MVPQAIC_IntakePrepareRefs`
- 🧪 Analyser réponse → `MVPQAIC_IntakeAnalyzeRawResponse`
- 🧾 Journaliser → `MVPQAIC_JournalAppendFromIntake`
- 🔁 Boucle qualité → `MVPQAIC_IntakePostJournalPromptLoop`
- ✅ Appliquer draft → `MVPQAIC_IntakeApplyApprovedDraftToLibrary`
- 🆕 Nouveau test → `MVPQAIC_IntakeNewBlank`

## 🎛️ PROMPT_VARIANT_CONTROL_CENTER
- 🔄 Refresh cockpit → `MVPQAIC_RuntimePromptControlCenterRun`
- 🧭 Navigation safe status → `MVPQAIC_ControlCenterActionHandoffStatus`
- 📍 Ouvrir cible recommandée → `MVPQAIC_ControlCenterOpenRecommendedTarget`
- 🧪 Batch status → `MVPQAIC_P2Batch3_Status`

## 📘 PROMPT_LIBRARY / 🧭 PROMPT_IMPROVEMENT_QUEUE
- 🎨 Format / audit stable → `MVPQAIC_PromptWorkflowAuditRepairSafe`
- ✅ Appliquer draft → `MVPQAIC_PromptDraftApplyApprovedToLibrary`
