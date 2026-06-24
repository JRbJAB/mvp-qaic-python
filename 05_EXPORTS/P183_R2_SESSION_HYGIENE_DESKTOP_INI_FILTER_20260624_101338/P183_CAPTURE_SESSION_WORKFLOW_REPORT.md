# P183 Capture To Session Link And Prompt Run Workflow

- STATUS: OK_P183_CAPTURE_TO_SESSION_LINK_WORKFLOW_READY
- workflow_ready: True
- active_prompt_count: 1
- capture_count: 0
- gem_response_count: 0
- session_created: True
- blocker_count: 0

Workflow:
1. Upload capture portfolio locally.
2. Use active prompt from Prompt Studio.
3. Query GEM manually outside Python.
4. Paste/save GEM response locally.
5. Create review-only session link.
6. Human review required before any next action.

Safety:
- GEM_CALL_EXECUTED=False
- AUTO_APPLY_GEM_RESPONSE=False
- SOURCE_PROMPT_MODIFIED=False
- GOOGLE_SHEETS_WRITE=False
- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False
- APPS_SCRIPT_EXECUTION=False
- CLASP_PUSH=False
- PUBLIC_SERVE=False
- BROKER=False
- ORDER=False
- SIZING=False

Next:
- P184_REAL_GEM_SESSION_REVIEW_AND_RESPONSE_PARSER
