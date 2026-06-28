# MVP QAIC Reflex Server Scripts R5K

Status: OK_MVP_QAIC_REFLEX_SERVER_SCRIPTS_R5K_READY

Fix:
- START defaults to npm via REFLEX_USE_NPM=true.
- START does not stop on npm warning stderr during version checks.
- START detects rolldown native binding failures.
- START repairs @rolldown/binding-win32-*-msvc from node architecture.
- STATUS detects rolldown native binding failures and gives action.
- STOP remains port-safe and can optionally kill known local Reflex children.

Safety:
- NO_RUNTIME_START=True for this installer.
- NO_PUBLIC_DEPLOY=True.
- NO_BROKER_ORDER_SIZING=True.
- NO_SHEET_WRITE=True.
- NO_BIGQUERY_WRITE=True.

Next: run scripts/START_REFLEX_LOCAL_SAFE.ps1 -CleanWeb once.
