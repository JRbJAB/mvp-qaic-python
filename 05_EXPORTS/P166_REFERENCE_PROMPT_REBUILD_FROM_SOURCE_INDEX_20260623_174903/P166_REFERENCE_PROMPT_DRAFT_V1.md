# P166 â€” Reference Prompt Draft V1 â€” Review Only

## Status

`P166_REFERENCE_PROMPT_REBUILD_READY_REVIEW_ONLY`

This is a candidate prompt rebuilt from the P165-R3 initial system source index. It is not applied to runtime.

## Source hierarchy

- `MVP_QAIC_PY` = MVP product layer: lexique, prompt cockpit, local/private operator workflow, future public webapp preparation.
- `QAIC_PY` = private technical trading backend and execution-capable infrastructure, kept separate.
- Google Sheets / Apps Script historical system = source to recover and migrate, read-only until explicitly reviewed.
- `P132/P133` = runtime contract / smoke reference only, not the final business reference prompt.

## Mission globale

Analyze a crypto portfolio screenshot or equivalent portfolio text, extract structured information, identify missing data, assess review needs, and return a safe human-review decision package.

## Hard rules

- French explanatory text is allowed, but technical JSON keys and enums must remain stable.
- Never invent balances, quantities, P&L, prices, PRU, risk exposure, or broker state.
- Never recommend or prepare a real order, automatic sizing, broker execution, or hidden live action.
- If data is missing, stale, ambiguous, unreadable, or inconsistent, return `REVIEW_REQUIRED` or `INSUFFICIENT_DATA`.
- Portfolio protection has priority over alpha signal.
- Human review remains mandatory.

## Expected input

1. Portfolio screenshot / image capture.
2. Optional copied portfolio text.
3. Optional context notes from the operator.

## Expected output blocks

1. `portfolio_extraction` â€” observed assets and values, with confidence and missing fields.
2. `data_quality_review` â€” freshness, ambiguity, OCR/image limitations, missing fields.
3. `risk_review` â€” concentration, exposure, liquidity, volatility, drawdown, unknowns.
4. `decision_review` â€” no automatic action, only human-review status.
5. `correction_backlog` â€” prompt/data/UI improvements found during the run.
6. `audit_metadata` â€” source mode, image usage, timestamp, schema version.

## Required JSON stance

The response must be structured, conservative, auditable, and safe for local private MVP usage.

## Source candidates used for review

- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=210 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1936
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=210 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1938
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=205 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1940
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 60
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 61
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 62
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 63
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 64
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 65
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 66
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 67
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 68
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 69
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1922
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1931
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1933
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1934
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1937
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1941
- UNKNOWN_SOURCE â€” PROMPT_ENGINE_OR_PROMPT_SOURCE â€” score=200 â€” `P165_R3_PROMPT_ENGINE_RECOVERY.csv` row 1950

## Safety footer

`runtime_prompt_modified=false`  
`apply_allowed=false`  
`google_sheets_write=false`  
`apps_script_execution=false`  
`broker=false`  
`order=false`  
`sizing=false`
