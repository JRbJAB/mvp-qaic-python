# P118 Daily Operator Shortcut Commands

## Recommended: pasted text file

```powershell
python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_REVIEW" --pasted-text-file "portfolio_input.txt" --notes "Daily manual portfolio review. Human review only." --run-id "DAILY-GEM-REVIEW"
```

## Screenshot reference mode

```powershell
python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_IMAGE_REVIEW" --image-reference "portfolio_capture.png" --notes "Image reference only. No OCR claim." --run-id "DAILY-GEM-IMAGE-REVIEW"
```

## Local smoke/sample mode

```powershell
python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_SAMPLE" --use-default-sample --run-id "DAILY-GEM-SAMPLE"
```
