# P137 — GEM Output Contract

Contract: `P137_GEM_OUTPUT_CONTRACT`
Gem: `GEM_GENERAL_REVIEW`
Prompt profile: `P132_R2_MULTIMODAL_PORTFOLIO_USD`

## Required JSON keys

- `status`
- `gem_id`
- `prompt_profile`
- `reference_currency`
- `image_used`
- `image_usage_evidence`
- `portfolio_extract`
- `missing_data`
- `blockers`
- `human_review_required`
- `no_order_no_sizing`
- `safety`

## Hard safety

- `human_review_required`: `True`
- `no_order_no_sizing`: `True`
- `no_broker_execution`: `True`
- `no_auto_apply`: `True`
- `no_invented_portfolio_data`: `True`
