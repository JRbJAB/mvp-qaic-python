# P117 Prompt GEM Runtime Quickstart

## Goal

Generate a local GEM prompt pack for manual crypto portfolio review.

## Fast path

1. Put your portfolio text in `portfolio_input.txt`, or keep a screenshot reference path.
2. Run one of the commands below.
3. Open `P116_GEM_PROMPT_COPY_PASTE.md`.
4. Copy it manually into GEM.
5. Paste GEM output into the next review/journal workflow.

## Commands

### Pasted text file

```powershell
python -m mvp_qaic_py.gem_prompt_runtime_cli --output-dir "05_EXPORTS/GEM_RUN_PASTED_TEXT" --input-mode PASTED_TEXT_DRAFT --pasted-text-file "portfolio_input.txt" --notes "Manual pasted portfolio review. Human review only." --run-id "MANUAL-GEM-RUN"
```

### Screenshot / image reference

```powershell
python -m mvp_qaic_py.gem_prompt_runtime_cli --output-dir "05_EXPORTS/GEM_RUN_IMAGE_REVIEW" --input-mode IMAGE_REVIEW_REQUIRED --image-reference "portfolio_capture.png" --notes "Image reference only. No OCR claim. Human review required." --run-id "MANUAL-IMAGE-REVIEW"
```

### Structured JSON

```powershell
python -m mvp_qaic_py.gem_prompt_runtime_cli --output-dir "05_EXPORTS/GEM_RUN_STRUCTURED" --input-mode STRUCTURED --structured-json-file "portfolio_structured.json" --notes "Structured manual input. Human review only." --run-id "MANUAL-STRUCTURED-REVIEW"
```

## Hard safety

- HUMAN_REVIEW_ONLY.
- NO_OCR_CLAIM.
- NO_BROKER / NO_ORDER / NO_AUTO_SIZING.
- NO_REVOLUTX_REAL_ACCESS_FROM_MVP.
