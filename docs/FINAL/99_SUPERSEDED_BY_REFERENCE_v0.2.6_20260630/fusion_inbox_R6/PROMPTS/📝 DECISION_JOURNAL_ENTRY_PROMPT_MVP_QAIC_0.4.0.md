# 📝 Prompt — Générer une entrée Decision Journal MVP QAIC 0.4.0

> **Version :** `MVP_QAIC_DECISION_JOURNAL_ENTRY_PROMPT_0.4.0`  
> **Statut :** `P1_GPT_RESPONSE_AUDIT_DECISION_JOURNAL_READY_FOR_DRIVE_REVIEW`  

---

## Prompt

```text
Transforme l’analyse suivante en entrée DECISION_JOURNAL MVP QAIC.

Contraintes :
- aucune exécution broker ;
- aucune recommandation certaine ;
- décision humaine uniquement ;
- si données manquantes, indique REVIEW_REQUIRED ;
- si SL absent, indique BLOCKED ;
- si réponse GPT rejetée, indique GPT_RESPONSE_REJECTED.

Champs à produire :
journal_id_placeholder
created_at_placeholder
payload_id
gpt_response_audit_status
asset
token_type
analysis_level
decision_status
human_final_decision
scores_summary
signals_summary
missing_data
blockers
entry_summary
tp_summary
sl_summary
trailing_summary
portfolio_context
notes
run_id
validation_status

Analyse à convertir :
[COLLER ICI]
```
