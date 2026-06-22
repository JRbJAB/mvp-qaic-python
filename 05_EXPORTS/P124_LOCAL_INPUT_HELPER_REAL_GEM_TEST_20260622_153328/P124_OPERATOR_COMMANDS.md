# P124 Operator Commands

## Step 1 - Generate daily GEM prompt

```powershell
python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\P118_DAILY_PROMPT_PACK" --pasted-text-file "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\portfolio_input.txt" --run-id "P124-REAL-GEM-TEST-20260622-P118"
```

## Step 2 - Paste prompt manually into GEM

Open:

`G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\P118_DAILY_PROMPT_PACK\P118_RUNTIME_PACK\P116_GEM_PROMPT_COPY_PASTE.md`

## Step 3 - Paste GEM response into local file

`G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\gem_response.txt`

## Step 4 - Capture GEM response and review queue

```powershell
python -m mvp_qaic_py.gem_response_review_queue --output-dir "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\P119_GEM_RESPONSE_CAPTURE" --response-text-file "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\gem_response.txt" --source-prompt-run-id "P124-REAL-GEM-TEST-20260622-P118" --response-run-id "P124-REAL-GEM-TEST-20260622-P119"
```

## Step 5 - Bridge to local decision journal candidate

```powershell
python -m mvp_qaic_py.gem_response_decision_journal_bridge --output-dir "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\P120_DECISION_JOURNAL_CANDIDATE" --response-capture-json-file "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\P119_GEM_RESPONSE_CAPTURE\P119_RESPONSE_CAPTURE.json" --journal-entry-id "P124-REAL-GEM-TEST-20260622-P120-JOURNAL"
```

## Optional - local smoke only

```powershell
python -m mvp_qaic_py.gem_daily_loop_smoke --output-dir "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_153328\P121_E2E_SMOKE_OPTIONAL" --run-id "P124-REAL-GEM-TEST-20260622-P121-SMOKE"
```

## Hard stop

No Sheet write. No Apps Script. No broker. No order. No sizing. No Revolut X real access from MVP.
`NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.
