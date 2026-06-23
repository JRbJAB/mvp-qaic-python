# P165-R3 — Initial Sheet & Apps Script Functional Source Access Layer

## Decision

- This is the correction layer for the Python migration.
- P132/P133 remains a runtime contract only, not the final business reference prompt.
- The initial Google Sheet / Apps Script system is recovered into Python-friendly registries.
- No runtime prompt modification, no Sheet write, no Apps Script execution, no CLASP push.

## Summary

- `APPS_SCRIPT_MODULE_COUNT`: `22`
- `APPS_SCRIPT_FUNCTION_COUNT`: `2738`
- `PROMPT_ENGINE_FUNCTION_COUNT`: `2296`
- `FUNCTIONAL_MIGRATION_MAP_COUNT`: `22`

## Top prompt/AI recovery candidates

- `appsscript.json` / `` family=`MANIFEST` role=`OTHER`
- `mvpqaic_00_setup_p0.js` / `` family=`SETUP_FOUNDATION` role=`OTHER`
- `mvpqaic_00_setup_p0.js` / `` family=`SETUP_FOUNDATION` role=`OTHER`
- `mvpqaic_00_setup_p0.js` / `` family=`SETUP_FOUNDATION` role=`OTHER`
- `mvpqaic_00_setup_p0.js` / `` family=`SETUP_FOUNDATION` role=`OTHER`
- `mvpqaic_01_knowledge_engine.js` / `MVPQAIC_ExplainDecision` family=`KNOWLEDGE_SEARCH` role=`DECISION_JOURNAL`
- `mvpqaic_03_import_csv_seeds.js` / `` family=`IMPORT_SEEDS` role=`INGESTION_INTAKE`
- `mvpqaic_03_import_csv_seeds.js` / `` family=`IMPORT_SEEDS` role=`INGESTION_INTAKE`
- `mvpqaic_03_import_csv_seeds.js` / `` family=`IMPORT_SEEDS` role=`INGESTION_INTAKE`
- `mvpqaic_04_p0b2_expansion.js` / `MVPQAIC_GetPrompt` family=`QAIC_BRIDGE` role=`PROMPT_OR_AI`
- `mvpqaic_04_p0b2_expansion.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_04_p0b2_expansion.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_04_p0b2_expansion.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_04_p0b2_expansion.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_04_p0b2_expansion.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_04_p0b2_expansion.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_04_p0b2_expansion.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_05_p0b3_institutional_readiness.js` / `MVPQAIC_GetDecisionMatrix` family=`QAIC_BRIDGE` role=`DECISION_JOURNAL`
- `mvpqaic_05_p0b3_institutional_readiness.js` / `MVPQAIC_GetGPTBridge` family=`QAIC_BRIDGE` role=`PROMPT_OR_AI`
- `mvpqaic_05_p0b3_institutional_readiness.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_05_p0b3_institutional_readiness.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_05_p0b3_institutional_readiness.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_05_p0b3_institutional_readiness.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_05_p0b3_institutional_readiness.js` / `` family=`QAIC_BRIDGE` role=`OTHER`
- `mvpqaic_05_p0b3_institutional_readiness.js` / `` family=`QAIC_BRIDGE` role=`OTHER`

## Next

`P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_OR_LIVE_EXPORT`
