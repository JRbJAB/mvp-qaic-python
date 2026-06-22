
# P130 Operator Commands

## Step 1 — Check P124 handoff

Open:

```text
G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_20260622_164559\P130_P124_HANDOFF
```

Use `portfolio_input.txt` as the portfolio input for the manual GEM prompt flow.

## Step 2 — Paste GEM answer

Paste the GEM answer into:

```text
G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_20260622_164559\P130_P124_HANDOFF\gem_response.txt
```

## Step 3 — Run P125 review UX

```powershell
python -m mvp_qaic_py.gem_manual_test_review_pack --output-dir "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_20260622_164559\P130_P125_REVIEW_OUTBOX" --p124-run-dir "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_20260622_164559\P130_P124_HANDOFF" --run-id P130-P125
```

## Step 4 — Run P126 registry

```powershell
python -m mvp_qaic_py.daily_run_registry --output-dir "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_20260622_164559\P130_P126_REGISTRY_OUTBOX" --exports-dir "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS" --run-id P130-P126
```

## Safety

HUMAN_REVIEW_ONLY / NO_OCR_CLAIM / NO_AUTOMATED_VISUAL_EXTRACTION / NO_INVENTED_PORTFOLIO_DATA / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING / NO_AUTO_APPLY_GEM_RESPONSE.
