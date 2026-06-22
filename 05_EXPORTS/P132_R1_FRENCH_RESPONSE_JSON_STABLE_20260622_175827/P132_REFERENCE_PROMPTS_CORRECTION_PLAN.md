
# P132 Reference Prompts Correction Plan

## Question: when do we correct the current main GEM reference prompts?

We do it in two phases.

### Phase A — Today functional version

P132 is the functional layer for today's test:
- one multimodal GEM prompt,
- image attached directly to the main prompt,
- optional Revolut X copied text,
- USD as reference currency,
- output JSON schema,
- image usage evidence gate.

This avoids blocking today's test on a risky global refactor.

### Phase B — Controlled reference prompt sync

After P132/P133 are validated with one real GEM response, patch the existing reference prompts in a controlled batch:
- identify current GEM principal prompt files,
- replace EUR-centric fields with USD-centric fields,
- add image attachment language,
- add image_usage_evidence requirement,
- add no-order/no-sizing/no-auto-apply constraints,
- keep backward compatibility wrappers where needed,
- run tests and export a prompt diff report.

Recommended next:
- P133: GEM response capture and image usage gate.
- P134: Reference prompt inventory + patch plan read-only.
- P135: Apply reference prompt sync if P133 real response passes.
