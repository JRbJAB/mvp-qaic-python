# R21F - Drive-first reference lock memo

Date: 2026-07-01
Status: active project instruction lock after R21B/R21C/R21D/R21E.

## Mandatory rule

For every next MVP QAIC / QAIC / QAIT project action, the assistant must not work from memory only.

Before proposing, generating, patching, auditing, committing, tagging, pushing, or running any batch, the assistant must:

1. Read or search Drive source of truth.
2. Verify docs/FINAL/CURRENT_REFERENCE_INDEX.md.
3. Verify active final docs.
4. Verify CDC, tool registry, and UI tracker references in Drive or repo before any patch/binding touching these domains.
5. Stop inventing from memory.
6. Stop generating a batch without auditing the relevant referentials first.

## Operational lock

`	ext
DRIVE_LIVE_ACCESS=True
DRIVE_SOURCE_OF_TRUTH_REQUIRED=True
READ_CURRENT_REFERENCE_INDEX_BEFORE_PROJECT_BATCH=True
READ_FINAL_DOCS_BEFORE_PROJECT_BATCH=True
READ_CDC_TOOL_REGISTRY_UI_TRACKER_REFERENCES_BEFORE_PATCH=True
NO_MEMORY_ONLY=True
NO_APPROXIMATION=True
NO_BATCH_WITHOUT_REFERENTIAL_AUDIT=True
NO_RUNTIME_OR_CODEX_RUNNER_BEFORE_RELEVANT_REFERENCES_AUDITED=True
`

## Consequence

If the required references cannot be read or verified, the only allowed response is a read-only audit request/action. No integration batch, no source patch, no runtime, no Codex runner, no commit/tag/push.

## Relation with R21B Reflex runtime closure

This lock complements R21B. Reflex runtime remains paused; product work may continue only after reading the relevant final docs and referentials.
