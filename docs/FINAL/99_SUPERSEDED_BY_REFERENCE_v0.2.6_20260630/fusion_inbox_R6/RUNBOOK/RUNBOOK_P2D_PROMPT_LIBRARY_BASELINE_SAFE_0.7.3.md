# 📘 Runbook — P2-D Prompt Library Baseline Safe 0.7.3

## 1. Replace script
Replace the full content of `mvpqaic_11_p1_prompt_quality_core.gs` with the provided script.

## 2. Status check
Run:

```javascript
MVPQAIC_PromptQualityCoreStatus()
```

Expected: status OK, emoji frontend sheets detected.

## 3. Initialize baseline prompt library safely
Run:

```javascript
MVPQAIC_PromptLibraryInitBaselineSafe()
```

Expected:
- status OK
- mode APPEND_OR_INIT_ONLY_NO_OVERWRITE_APPROVED_PROMPTS
- rows_appended > 0 if `📘 PROMPT_LIBRARY` was empty
- overwrite_prompt_library false
- active_prompt_auto_promotion false

## 4. Check adaptive loop
Run:

```javascript
MVPQAIC_PromptAdaptiveLoopStatus()
MVPQAIC_PromptAdaptiveNextDraftBuild()
```

Expected:
- PROMPT_LIBRARY rows_read > 0
- draft stays in `🧭 PROMPT_IMPROVEMENT_QUEUE`
- promotion_allowed NO

## Notes
`MVPQAIC_PromptLibraryRefresh()` now routes to the same safe baseline init path to avoid destructive `sheet.clear()` behavior.
