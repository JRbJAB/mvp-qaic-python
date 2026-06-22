# P122 Daily Operator Commands

## 1. Create daily prompt from portfolio text

```powershell
python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_RUN" --pasted-text-file "portfolio_input.txt" --run-id "DAILY-GEM-RUN"
```

## 2. Paste the generated prompt into GEM manually

Open:

`05_EXPORTS/DAILY_GEM_RUN/P118_RUNTIME_PACK/P116_GEM_PROMPT_COPY_PASTE.md`

## 3. Capture GEM response locally

```powershell
python -m mvp_qaic_py.gem_response_review_queue --output-dir "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE" --response-text-file "gem_response.txt" --source-prompt-run-id "DAILY-GEM-RUN" --response-run-id "DAILY-GEM-RESPONSE"
```

## 4. Bridge to local decision journal candidate

```powershell
python -m mvp_qaic_py.gem_response_decision_journal_bridge --output-dir "05_EXPORTS/DAILY_GEM_JOURNAL_CANDIDATE" --response-capture-json-file "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE/P119_RESPONSE_CAPTURE.json" --journal-entry-id "DAILY-GEM-JOURNAL-CANDIDATE"
```

## 5. Optional smoke check

```powershell
python -m mvp_qaic_py.gem_daily_loop_smoke --output-dir "05_EXPORTS/DAILY_GEM_E2E_SMOKE" --run-id "DAILY-GEM-E2E-SMOKE"
```

## Hard stop

Do not write to Sheets. Do not run Apps Script. Do not create orders. Do not auto-apply GEM output.
