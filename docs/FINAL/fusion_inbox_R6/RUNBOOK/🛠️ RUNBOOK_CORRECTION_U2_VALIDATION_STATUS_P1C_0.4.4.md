# 🛠️ RUNBOOK — Correction U2 Validation Status P1-C 0.4.4

## Si la ligne est déjà ajoutée

Dans `DECISION_JOURNAL`, cellule `U2` ou colonne `validation_status` :

```text
remplacer HUMAN_REVIEW_ONLY par REVIEW_REQUIRED
```

Ne pas modifier :

```text
gpt_response_audit_status = GPT_RESPONSE_INSUFFICIENT_DATA
analysis_level = INSUFFICIENT_DATA
decision_status = REVIEW_REQUIRED
human_final_decision = NO_ACTION
sl_summary = BLOCKED
```

## Ensuite

Relancer :

```javascript
MVPQAIC_P1C_JournalStatus()
```

Puis :

```javascript
MVPQAIC_P1C_AppendFirstAuditJournalEntry()
```

Résultat attendu :

```text
ALREADY_EXISTS
```
