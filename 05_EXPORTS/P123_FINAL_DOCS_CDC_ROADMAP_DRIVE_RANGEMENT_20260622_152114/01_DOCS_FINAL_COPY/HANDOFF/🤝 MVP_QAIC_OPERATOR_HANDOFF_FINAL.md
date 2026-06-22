# MVP QAIC — Operator Handoff Final

## Statut

P122 a établi le point d'arrêt opérateur. P123 consolide la documentation finale.

## Commande quotidienne type

```powershell
python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_RUN" --pasted-text-file "portfolio_input.txt" --run-id "DAILY-GEM-RUN"
```

## Après réponse GEM

```powershell
python -m mvp_qaic_py.gem_response_review_queue --output-dir "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE" --response-text-file "gem_response.txt" --source-prompt-run-id "DAILY-GEM-RUN" --response-run-id "DAILY-GEM-RESPONSE"
```

## Bridge journal local

```powershell
python -m mvp_qaic_py.gem_response_decision_journal_bridge --output-dir "05_EXPORTS/DAILY_GEM_JOURNAL_CANDIDATE" --response-capture-json-file "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE/P119_RESPONSE_CAPTURE.json" --journal-entry-id "DAILY-GEM-JOURNAL-CANDIDATE"
```

## Stop condition

Stop après documentation, sauf test manuel GEM réel ou helper local d'entrée demandé.

Notes : P123-R5 final docs. TRUE fusion initial version to P122, exact NO_REVOLUTX_REAL_ACCESS_FROM_MVP marker, MD emoji deliverables, CDC roadmap, Drive rangement, existing docs integrated.
