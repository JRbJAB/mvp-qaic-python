# P117 CLI Commands

## pasted_text_file

```powershell
python -m mvp_qaic_py.gem_prompt_runtime_cli --output-dir "05_EXPORTS/GEM_RUN_PASTED_TEXT" --input-mode PASTED_TEXT_DRAFT --pasted-text-file "portfolio_input.txt" --notes "Manual pasted portfolio review. Human review only." --run-id "MANUAL-GEM-RUN"
```

## image_review_required

```powershell
python -m mvp_qaic_py.gem_prompt_runtime_cli --output-dir "05_EXPORTS/GEM_RUN_IMAGE_REVIEW" --input-mode IMAGE_REVIEW_REQUIRED --image-reference "portfolio_capture.png" --notes "Image reference only. No OCR claim. Human review required." --run-id "MANUAL-IMAGE-REVIEW"
```

## structured_json

```powershell
python -m mvp_qaic_py.gem_prompt_runtime_cli --output-dir "05_EXPORTS/GEM_RUN_STRUCTURED" --input-mode STRUCTURED --structured-json-file "portfolio_structured.json" --notes "Structured manual input. Human review only." --run-id "MANUAL-STRUCTURED-REVIEW"
```
