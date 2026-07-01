# MVP QAIC to QAIC Bridge Contract R1

Contract ID: `MVP_QAIC_TO_QAIC_BRIDGE_R1`

Status: R1 review-only local handoff contract.

This contract defines the first repository-level bridge from MVP QAIC to the future private QAIC Python engine import layer. It is a local, review-only handoff for analysis-ready payloads. It is not a broker bridge, not an execution bridge, and not a runtime launch contract.

## Constants

| Name | Value |
| --- | --- |
| `CONTRACT_ID` | `MVP_QAIC_TO_QAIC_BRIDGE_R1` |
| `CONTRACT_VERSION` | `R1` |
| `MODE` | `REVIEW_ONLY_LOCAL_HANDOFF` |
| `SOURCE_SYSTEM` | `MVP_QAIC` |
| `TARGET_SYSTEM` | `QAIC_PY` |

## Required Payload Keys

The JSON payload must contain exactly these required top-level keys:

- `contract_id`
- `contract_version`
- `mode`
- `source_system`
- `target_system`
- `created_by`
- `created_at_utc`
- `safety`
- `portfolio_input`
- `gem_prompt`
- `gem_response`
- `review_queue`
- `decision_journal`
- `qaic_import`
- `evidence`

## Safety Lock

The safety block is mandatory and locked:

```json
{
  "no_runtime": true,
  "no_provider_call": true,
  "no_broker_order_sizing": true,
  "no_sheet_bq_write": true,
  "human_review_required": true,
  "qaic_execution_allowed": false
}
```

## Included Scope

The bridge explicitly includes these MVP-side sources:

- `P112_GEM_PORTFOLIO_PROMPT_MODULE`
- `P113_PORTFOLIO_INPUT_NORMALIZER_IMAGE_REVIEW`
- `P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE`
- `P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE`
- `P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE`
- `P196_REAL_CASE_PORTFOLIO_GEM_INPUTS`

## Forbidden Scope

The bridge explicitly forbids:

- broker action
- order action
- sizing action
- provider live call
- Sheet/BQ write
- Apps Script execution
- runtime launch
- public deploy

## Handoff Boundary

MVP QAIC provides portfolio input/capture references, GEM prompt metadata, GEM response capture metadata, review queue state, and decision journal candidates. QAIC Python receives only a future import-ready read-only payload shape for local analysis review.

QAIC import mode is `review_only_import_ready`. QAIC execution is not allowed.

## Artifacts

- Python contract: `mvp_qaic_py/qaic_bridge_contract.py`
- Sample payload: `data/samples/mvp_qaic_bridge/MVP_QAIC_TO_QAIC_BRIDGE_SAMPLE_R1.json`
- Status document: `docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_STATUS_R1.md`
