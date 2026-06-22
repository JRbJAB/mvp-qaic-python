# P122 Daily GEM Loop Runbook

## Daily manual flow

1. Prepare `portfolio_input.txt` locally.
2. Generate P118 daily prompt pack.
3. Copy the prompt manually into GEM.
4. Paste GEM response into `gem_response.txt`.
5. Run P119 capture to create review queue.
6. Run P120 bridge to create local journal candidate.
7. Read blockers and missing data before any decision.

## Interpretation

- `BLOCKED`: do not continue until blockers are resolved manually.
- `REVIEW_REQUIRED`: missing data or manual verification still needed.
- `READY_FOR_HUMAN_DECISION`: still human-only; no automatic order or sizing.

## Future step

P123 may add a local input helper, but not a live UI/deployment layer.
