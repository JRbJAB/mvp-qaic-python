# P144 — Prompt Cockpit Workflows

- Status: `P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY`
- Workflow steps: `11`
- Source CSV count: `65`

## Operator flow

1. `select_prompt`
2. `select_variant`
3. `attach_context`
4. `review_lexique_bridge`
5. `copy_prompt`
6. `queue_review`
7. `import_gem_response_in_p145`

## Safety

- Human review required
- No auto apply GEM response
- No Sheet write
- No broker/order/sizing
- No public deploy

Next: `P145_GEM_RESPONSE_IMPORT_E2E`
