# R21K Cockpit Queue Data Contract - No Runtime

Status: R21K defines the cockpit-ready data contract for the QAIC review queue.

## Source chain

- Source state: `R21J_R6_VALIDATED_BY_READONLY_HEAD_AUDIT`
- Source tag: `mvp-qaic-r21j-r6-docs-only-supersede-seal-no-runtime-20260701`
- Source product doc: `docs/PRODUCT/R21J_OPERATOR_QAIC_REVIEW_QUEUE_NO_RUNTIME.md`

## Purpose

R21K converts the R21J review queue into a stable data contract for future cockpit
surfaces. It does not create a visual page, a static page, an export folder, a
process runner, a provider call, or any write to Sheets or BigQuery.

## Required cockpit trace groups

- BRAND_CONFIG_TRACE_COCKPIT_READY=True
- UI_TRACKER_TRACE_COCKPIT_READY=True
- TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY=True
- CDC_CONTRACT_TRACE_COCKPIT_READY=True
- QAIC_BRIDGE_TRACE_COCKPIT_READY=True
- OPERATOR_QAIC_REVIEW_QUEUE_COCKPIT_READY=True

## Brand and visual config trace

- QAIT_CHARTE_TEMPLATE=BOUND
- MVP_QAIC_LOGO_VALIDATED=BOUND
- preserve_q_candlesticks_signal_line=True
- The cockpit contract must show that validated brand assets are bound.
- Generated previews must not replace validated logo assets.

## Contract outputs

Tracked source files only:

- `mvp_qaic_py/cockpit_queue_data_contract_r21k.py`
- `tests/test_r21k_cockpit_queue_data_contract.py`
- `docs/PRODUCT/R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME.md`

## Safety locks

- NO_CODEX=True
- NO_RUNTIME=True
- NO_DOCKER=True
- NO_PROVIDER_CALL=True
- NO_BROKER_ORDER_SIZING=True
- NO_SHEET_BQ_WRITE=True
- NO_MARKUP_OUTPUT=True
- NO_EXPORT_DIRECTORY_OUTPUT=True
- QAIC_EXECUTION_ALLOWED=False
- HUMAN_REVIEW_REQUIRED=True

## Next

R21L can bind this data contract to a cockpit model or UI surface only after a
new Drive-first reference audit and without starting any UI engine process.

## R21K source validation trace
- SOURCE_R21J_R6_VALIDATED=True
- SOURCE_R21J_HEAD=a9a9fb79caccdb8674ae5c2555cb55044575910c
- SOURCE_R21J_TAG=mvp-qaic-r21j-r6-docs-only-supersede-seal-no-runtime-20260701
- COCKPIT_QUEUE_DATA_CONTRACT=READY
- BRAND_CONFIG_TRACE_COCKPIT_READY=True
- UI_TRACKER_TRACE_COCKPIT_READY=True
- TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY=True
- CDC_CONTRACT_TRACE_COCKPIT_READY=True
- QAIC_BRIDGE_TRACE_COCKPIT_READY=True