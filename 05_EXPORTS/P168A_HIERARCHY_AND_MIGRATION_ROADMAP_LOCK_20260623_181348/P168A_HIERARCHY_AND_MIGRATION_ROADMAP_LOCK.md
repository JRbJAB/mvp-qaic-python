# P168A — Hierarchy and Migration Roadmap Lock

- Status: `P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_READY_REVIEW_ONLY`
- Project: `MVP_QAIC_PY`
- Hierarchy locked: `True`
- Blocker count: `0`
- Next: `P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY`

## Source milestones

- P165 export: `C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901\05_EXPORTS\P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_20260623_193121`
- Apps Script modules: `22`
- Apps Script functions: `2738`
- Prompt/GPT/GEM functions: `2296`
- P166 source candidates: `4288`
- P167 review items: `5`
- P167 pending review: `5`

## Locked domain boundaries

### MVP_QAIC_PY

- Owner role: MVP product and operator layer
- Allowed scope: lexique, webapp/NiceGUI local private, prompt cockpit, prompt review, Sheets snapshots/read-only data migration, Apps Script functional recovery, operator handoff
- Forbidden scope: broker execution, real orders, auto sizing, Revolut X execution backend, QAIT assets, public deploy without explicit release gate
- Source of truth: mvp-qaic-python repository + reviewed Sheets/App Script snapshots

### QAIC_PY

- Owner role: private crypto trading backend
- Allowed scope: technical backend, market/scoring/risk engine, Revolut X crypto lane, execution-capable modules locked by human review and safety gates
- Forbidden scope: MVP public/webapp product surface, QAIT Revolut Invest lane, unreviewed prompt apply
- Source of truth: qaic-python-min-cost-dev-factory repository

### QAIT_PY

- Owner role: actions and commodities trading backend
- Allowed scope: actions, commodities, Revolut Invest lane, BigQuery/read-only inventories, provider-specific evidence packs
- Forbidden scope: MVP prompt cockpit, MVP lexique/webapp, QAIC Revolut X crypto lane
- Source of truth: qait-python-min-cost-dev-factory repository

## Recommended roadmap

### P0 — P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY

- Domain: `MVP_QAIC_PY`
- Objective: Create a deterministic local Python snapshot layer for key MVP Sheets tabs using read-only exports or already-approved local snapshots.
- Inputs: P165 source registry, live Sheets IDs, CONFIG/lexique/journal/prompt tables
- Outputs: tab registry, bounded CSV snapshots, schema/readiness report
- Apply mode: `READ_ONLY_NO_SHEET_WRITE`
- Status: `RECOMMENDED_NEXT`

### P1 — P169_APPS_SCRIPT_TO_PYTHON_FUNCTIONAL_PORT_SELECTOR

- Domain: `MVP_QAIC_PY`
- Objective: Convert the 22 Apps Script modules and 2738 function index into a ranked Python migration backlog by feature lane.
- Inputs: P165_R3_APPS_SCRIPT_MODULE_INVENTORY.csv, P165_R3_FUNCTIONAL_MIGRATION_MAP.csv
- Outputs: module backlog, feature parity matrix, port/no-port decisions
- Apply mode: `LOCAL_REVIEW_ONLY`
- Status: `NEXT_AFTER_SNAPSHOT`

### P2 — P170_PROMPT_COCKPIT_BINDING_TO_REFERENCE_PROMPT

- Domain: `MVP_QAIC_PY`
- Objective: Bind the reviewed reference prompt draft to local operator/NiceGUI prompt cockpit without automatic runtime replacement.
- Inputs: P166 reference draft, P167 review workbench, operator approval
- Outputs: prompt cockpit draft binding, preview smoke, manual apply gate
- Apply mode: `HUMAN_REVIEW_ONLY`
- Status: `WAIT_AFTER_P167_HUMAN_REVIEW`

### P3 — QAIC_PY_HANDOFF_BACKEND_BOUNDARY_CHECK

- Domain: `QAIC_PY`
- Objective: Keep trading/backend execution outside MVP_QAIC_PY and document any later handoff contract to QAIC_PY.
- Inputs: MVP reviewed outputs only; no broker state copied into MVP
- Outputs: handoff contract, no-live safety checklist
- Apply mode: `SEPARATE_REPOSITORY_ONLY`
- Status: `NOT_MVP_NEXT_BATCH`

### P4 — QAIT_PY_NOOP_BOUNDARY_CONFIRMATION

- Domain: `QAIT_PY`
- Objective: Keep actions/commodities and Revolut Invest work completely outside MVP_QAIC_PY.
- Inputs: none for MVP batch
- Outputs: boundary note only
- Apply mode: `NOOP_FOR_MVP`
- Status: `OUT_OF_SCOPE_FOR_MVP`

## Safety

- No Google Sheets write.
- No Apps Script execution.
- No CLASP push.
- No broker/order/sizing.
- No runtime prompt modification.
- Review-only roadmap lock.
