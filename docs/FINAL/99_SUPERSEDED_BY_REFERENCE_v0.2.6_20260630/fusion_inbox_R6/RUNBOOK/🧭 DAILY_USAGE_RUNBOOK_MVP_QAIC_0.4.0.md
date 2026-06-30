# 🧭 Daily Usage Runbook — MVP QAIC P1 0.4.0

> **Version :** `MVP_QAIC_DAILY_USAGE_RUNBOOK_0.4.0`  
> **Statut :** `P1_GPT_RESPONSE_AUDIT_DECISION_JOURNAL_READY_FOR_DRIVE_REVIEW`  

---

## 1. Routine quotidienne

```text
1. Ouvrir Sheet DEV / AppSheet
2. Vérifier QAIC_RUNTIME_BRIDGE_STATUS
3. Vérifier QAIC_SIGNAL_MAPPING_COVERAGE = 50/50
4. Générer ou consulter dernier GPT_INPUT_PAYLOADS
5. Copier le payload vers GPT Crypto
6. Auditer la réponse GPT
7. Journaliser la décision
8. Ne rien exécuter automatiquement
```

---

## 2. Fonctions Apps Script utiles

```javascript
MVPQAIC_P0B5_Status()
MVPQAIC_Status_FullSignalMapping_50_50()
MVPQAIC_BuildFullTradePlanPrompt()
```

---

## 3. Checklist avant analyse

| Question | Attendu |
|---|---|
| Données portfolio disponibles ? | Oui ou NO_PORTFOLIO_ROWS |
| Signal mapping complet ? | 50/50 |
| Payload validé ? | VALIDATED |
| Garde-fous présents ? | HUMAN_REVIEW_ONLY |
| GPT réponse auditée ? | Oui |
| Décision journalisée ? | Oui |

---

## 4. No-Go quotidien

```text
payload non validé
mapping < 50/50
réponse GPT non auditée
SL absent mais décision trade proposée
broker execution visible
données inventées
```
