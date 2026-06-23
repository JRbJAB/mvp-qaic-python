# P164 — Historical Prompt Audit & Reference Rebuild

## Decision

- `P132_P133_PORTFOLIO_MULTIMODAL_REVIEW` is demoted to `CURRENT_RUNTIME_CONTRACT_REFERENCE`.
- The final reference prompt must be rebuilt from historical/global prompt material.
- P164 is review-only and does not modify the runtime prompt.

## Top candidates

### 1. `mvp_qaic_py/p164_historical_prompt_audit_reference_rebuild.py`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `321`
- hits: `demande globale|plusieurs points|mission globale|prompt global|prompt de référence|prompt historique|gem|portfolio|capture|image|revolut|json|human_review|human review|review_required|risk|risque|decision|décision|hard rules|no broker|no order|no sizing|P132|P133|path_historical_bonus|path_prompt_bonus`

> ycache__", ".pytest_cache", ".ruff_cache", "node_modules", } ALLOWED_SUFFIXES = {".py", ".md", ".txt", ".csv", ".json", ".html", ".yaml", ".yml"} KEYWORDS = { "demande globale": 30, "plusieurs points": 28, "mission globale": 24, "prompt global": 22, "prompt de référence": 22, "prompt historique": 20, "gem": 14, "portfolio": 14, "capture": 12, "image": 12, "revolut": 12, "json": 10, "human_review": 12, "human review": 12, "review_required": 10, "risk": 8, "risque": 8, "decision": 8, "décision": 8, "hard rules": 7, "no broker": 8, "no order": 8, "no sizing": 8, "P132": -14, "P133": -14, } @dataclass(frozen=True) class PromptCandidate: rel_path: str suffix: str size_bytes: int source_kind: str score: int keyword_hits: str excerpt: str def _read(path: Path) -> str: if path.stat().st_size > 260_000: return "" for enc in ("utf-8", "utf-8-sig", "cp1252"): try: return path.read_text(encoding=enc

### 2. `tests/test_p164_historical_prompt_audit_reference_rebuild.py`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `263`
- hits: `demande globale|plusieurs points|mission globale|prompt global|gem|portfolio|capture|image|revolut|json|human_review|human review|review_required|risque|décision|hard rules|no broker|no order|no sizing|P132|P133|path_historical_bonus|path_prompt_bonus`

> multimodal_gem_image_prompt_usd_contract.py", "P132 P133 portfolio prompt image json hard rules", ) _write( tmp_path / "archives" / "prompt_global_ancien.md", "Demande globale en plusieurs points GEM portfolio capture image JSON human_review no broker no order no sizing", ) rows = build_inventory(tmp_path) kinds = {r.rel_path: r.source_kind for r in rows} assert ( kinds["mvp_qaic_py/multimodal_gem_image_prompt_usd_contract.py"] == "CURRENT_RUNTIME_CONTRACT_REFERENCE" ) assert "HISTORICAL" in kinds["archives/prompt_global_ancien.md"] def test_p164_writes_reference_candidate_review_only(tmp_path: Path) -> None: _write( tmp_path / "old_prompts" / "prompt_global_ancien.md", "Prompt global: demande globale en plusieurs points. GEM portfolio capture écran Revolut image JSON risque décision REVIEW_REQUIRED.", ) summary = build_and_write_export(tmp_path) assert summary["STATUS"].startswith("OK_P

### 3. `mvp_qaic_py/multimodal_gem_image_prompt_usd_contract.py`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `139`
- hits: `gem|portfolio|capture|image|revolut|json|human_review|human review|review_required|risk|decision|hard rules|no broker|no order|no sizing|P132|P133|path_prompt_bonus`

> mps( build_expected_gem_output_schema(), ensure_ascii=False, indent=2, sort_keys=True ) return f""" # P132 GEM Multimodal Portfolio Prompt — Revolut X / USD ## Input mode You will receive: 1. One attached image/screenshot from Revolut X or a similar crypto portfolio interface. 2. Optional copied text from the same interface. The image is part of this main prompt. Do not ask for or create a separate preliminary step where you only read the image. Perform the portfolio extraction and review in this single response. ## Langue de réponse - Réponds en français pour tous les textes rédigés, explications, résumés, commentaires et notes. - Conserve exactement les noms de champs JSON, les statuts techniques, les enums, les booléens et les marqueurs de sécurité définis dans le schéma. - Ne traduis pas les clés JSON. - Si la réponse est en JSON, les valeurs textuelles peuvent être en français, mais

### 4. `05_EXPORTS/P140_NICEGUI_COCKPIT_REPLICA_RENDERER_20260623_120204/P140_NICEGUI_REPLICA_APP.py`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `138`
- hits: `gem|portfolio|capture|revolut|json|human_review|human review|review_required|risk|risque|decision|décision|no broker|no order|no sizing|P133`

> \n "required_decision_matrix_rules",\n "required_output_template",\n "required_data_requirements",\n "required_qaic_mappings",\n "revolut_x_inclusion_mode",\n "portfolio_required",\n "journal_write_required",\n "execution_modes",\n "risk_guards",\n "priority",\n "validation_status"\n ],\n "filter_view_count": 0,\n "frozen_column_count": 0,\n "frozen_row_count": 1,\n "has_basic_filter": true,\n "header_rows_preview": [\n [\n "stable_id",\n "prompt_id",\n "runtime_name",\n "required_sections",\n "required_signal_families",\n "required_decision_matrix_rules",\n "required_output_template",\n "required_data_requirements",\n "required_qaic_mappings",\n "revolut_x_inclusion_mode",\n "portfolio_required",\n "journal_write_required",\n "execution_modes",\n "risk_guards",\n "priority",\n "validation_status"\n ],\n [\n "runtime_p1_portfolio",\n "prompt_01_portfolio_analysis",\n "P1 Portfolio Runtim

### 5. `mvp_qaic_py/gem_portfolio_prompt_module.py`

- kind: `PROMPT_RELATED_SOURCE_CANDIDATE`
- score: `136`
- hits: `gem|portfolio|capture|image|revolut|json|human_review|human review|review_required|risk|decision|path_prompt_bonus`

> automatic order execution, return `BLOCKED`. - Keep `human_decision_only=true` and `no_order_no_sizing=true`. ## User goal {payload["user_goal"]} ## Portfolio input mode `{payload["portfolio_input_mode"]}` ## Portfolio pasted text ```text {pasted_text or "NONE"} ``` ## Portfolio image / capture reference `{image_reference or "NONE"}` If this is image/capture based, do not claim OCR or visual extraction unless explicit extracted text is supplied. Ask for human confirmation of visible assets/quantities/values. ## Structured positions {positions_md} ## Market context ```text {payload["market_context"] or "NONE"} ``` ## Risk profile `{payload["risk_profile"]}` ## Missing data already known {missing} ## Blockers already known {blockers} ## Questions for user {questions} ## Required output JSON shape ```json {json.dumps(payload["expected_output_schema"], ensure_ascii=False, indent=2)} ``` """

### 6. `05_EXPORTS/P138C_R9_CUSTOM_OAUTH_CLIENT_SAFE_WRITE_20260623_113901/P138C_BACKUP___PROMPT_LIBRARY.csv`

- kind: `EXPORT_ARCHIVE_REFERENCE`
- score: `134`
- hits: `gem|portfolio|revolut|human_review|human review|review_required|risk|risque|decision|décision|no order|no sizing|path_prompt_bonus`

> ring_basis | missing_data | blockers | quality_score,score_id | risk_guard | missing_data | blockers | confidence_score | quality_score,critical_trade_metric | portfolio_metric_for_portfolio_decision | risk_guard_for_trade_decision,optional_metric | weak_confidence | partial_context,NO_SCORE_INVENTION | NO_PROXY_SCORE_WITHOUT_LABEL | NO_TRADE_PLAN_FROM_PARTIAL_SCORE,EXPLICIT_SCORE_FIELDS_WITH_NOT_AVAILABLE_ALLOWED,Return NOT_AVAILABLE or REVIEW_REQUIRED if data is missing.,P0_BLOCKER,HUMAN_REVIEW,,P2VCLN-20260612-172612,12/06/2026,MVP_QAIC_P2AB_LIBRARY_USED_BY_AND_PROMPT_DETAIL_FIX_1.1.8_SAFE,Seeded scoring contract rebuilt by P2-X.,,,NON_NEGOTIABLE P1G-GEM-LEXIQUE-001,Profil Gem — Lexique éducatif,RUNTIME_PROFILE,Profil runtime/Gem — GEM_LEXIQUE_EDUCATIONAL,GEM_LEXIQUE_EDUCATIONAL,RUNTIME_PROFILE,RUNTIME_CAPABILITY_PROFILE,ACTIVE,READY_TO_TEST,KEEP_CORE_OR_PROFILE,Contrat socle ou profi

### 7. `05_EXPORTS/P150B_LOCAL_PRIVATE_RELEASE_PACK_20260623_132954/release_evidence/P140_NICEGUI_COCKPIT_REPLICA_RENDERER/P140_NICEGUI_COMPONENT_MODEL.json`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `130`
- hits: `gem|portfolio|capture|revolut|json|human_review|human review|review_required|risk|risque|decision|décision|no order|no sizing|P133`

> l_families", "required_decision_matrix_rules", "required_output_template", "required_data_requirements", "required_qaic_mappings", "revolut_x_inclusion_mode", "portfolio_required", "journal_write_required", "execution_modes", "risk_guards", "priority", "validation_status" ], "filter_view_count": 0, "frozen_column_count": 0, "frozen_row_count": 1, "has_basic_filter": true, "header_rows_preview": [ [ "stable_id", "prompt_id", "runtime_name", "required_sections", "required_signal_families", "required_decision_matrix_rules", "required_output_template", "required_data_requirements", "required_qaic_mappings", "revolut_x_inclusion_mode", "portfolio_required", "journal_write_required", "execution_modes", "risk_guards", "priority", "validation_status" ], [ "runtime_p1_portfolio", "prompt_01_portfolio_analysis", "P1 Portfolio Runtime", "portfolio_snapshot,revolut_x_status,decision_matrix,data_qual

### 8. `05_EXPORTS/P140_NICEGUI_COCKPIT_REPLICA_RENDERER_20260623_120204/P140_NICEGUI_COMPONENT_MODEL.json`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `130`
- hits: `gem|portfolio|capture|revolut|json|human_review|human review|review_required|risk|risque|decision|décision|no order|no sizing|P133`

> l_families", "required_decision_matrix_rules", "required_output_template", "required_data_requirements", "required_qaic_mappings", "revolut_x_inclusion_mode", "portfolio_required", "journal_write_required", "execution_modes", "risk_guards", "priority", "validation_status" ], "filter_view_count": 0, "frozen_column_count": 0, "frozen_row_count": 1, "has_basic_filter": true, "header_rows_preview": [ [ "stable_id", "prompt_id", "runtime_name", "required_sections", "required_signal_families", "required_decision_matrix_rules", "required_output_template", "required_data_requirements", "required_qaic_mappings", "revolut_x_inclusion_mode", "portfolio_required", "journal_write_required", "execution_modes", "risk_guards", "priority", "validation_status" ], [ "runtime_p1_portfolio", "prompt_01_portfolio_analysis", "P1 Portfolio Runtime", "portfolio_snapshot,revolut_x_status,decision_matrix,data_qual

### 9. `mvp_qaic_py/gem_prompt_usability_pack.py`

- kind: `PROMPT_RELATED_SOURCE_CANDIDATE`
- score: `128`
- hits: `gem|portfolio|capture|image|revolut|json|human_review|human review|review_required|decision|path_prompt_bonus`

> PASTED_TEXT = ( "BTC 0.10 value EUR 6500; ETH 1.20 value EUR 4200; " "USDC 1000 value EUR 920; source=manual sample; prices not verified." ) DEFAULT_STRUCTURED_PORTFOLIO = { "source": "manual_sample", "human_review_only": True, "positions": [ {"asset": "BTC", "quantity": "0.10", "value_eur": "6500", "confidence": "manual"}, {"asset": "ETH", "quantity": "1.20", "value_eur": "4200", "confidence": "manual"}, {"asset": "USDC", "quantity": "1000", "value_eur": "920", "confidence": "manual"}, ], "notes": "Sample only. Do not infer live price, PnL, broker state, order, or sizing.", } def build_usability_contract() -> dict[str, Any]: return { "contract": "P117_PROMPT_GEM_RUNTIME_USABILITY_PACK", "version": VERSION, "status": "LOCAL_ONLY_READY_FOR_OPERATOR_REVIEW", "purpose": "Make P116 GEM prompt runtime usable for daily manual portfolio reviews.", "primary_command": "python -m mvp_qaic_py.gem_p

### 10. `mvp_qaic_py/gem_loop_operator_handoff.py`

- kind: `SUPPORTING_PROMPT_CONTEXT`
- score: `128`
- hits: `gem|portfolio|capture|revolut|json|human_review|human review|review_required|decision|no broker|no order|no sizing`

> or field in CHECKLIST_FIELDS}) def _daily_commands_markdown() -> str: return "\n".join( [ "# P122 Daily Operator Commands", "", "## 1. Create daily prompt from portfolio text", "", "```powershell", 'python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_RUN" --pasted-text-file "portfolio_input.txt" --run-id "DAILY-GEM-RUN"', "```", "", "## 2. Paste the generated prompt into GEM manually", "", "Open:", "", "`05_EXPORTS/DAILY_GEM_RUN/P118_RUNTIME_PACK/P116_GEM_PROMPT_COPY_PASTE.md`", "", "## 3. Capture GEM response locally", "", "```powershell", 'python -m mvp_qaic_py.gem_response_review_queue --output-dir "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE" --response-text-file "gem_response.txt" --source-prompt-run-id "DAILY-GEM-RUN" --response-run-id "DAILY-GEM-RESPONSE"', "```", "", "## 4. Bridge to local decision journal candidate", "", "```powershell", 'python -m mvp_q

### 11. `mvp_qaic_py/gem_multimodal_response_capture_gate.py`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `126`
- hits: `gem|portfolio|capture|image|revolut|json|human_review|human review|review_required|décision|no broker|no order|no sizing|P133`

> , "NO_SHEET_WRITE", ) REQUIRED_TOP_LEVEL_KEYS = ( "status", "source_type", "reference_currency", "image_used", "copy_paste_text_used", "image_usage_evidence", "portfolio", "assets", "missing_data", "unclear_data", "human_review_required", "no_order_no_sizing", ) REQUIRED_IMAGE_EVIDENCE_KEYS = ( "status", "visual_evidence_summary", "visible_platform_or_context", "blockers", ) REQUIRED_PORTFOLIO_KEYS = ( "total_value_usd", "unrealized_pnl_usd", "unrealized_pnl_pct", "cash_usd_value", "cash_allocation_pct", ) REQUIRED_ASSET_KEYS = ( "symbol", "asset_name", "quantity", "price_usd", "value_usd", "allocation_pct", "unrealized_pnl_usd", "unrealized_pnl_pct", "confidence", "notes", ) @dataclass(frozen=True) class GemMultimodalResponseGateRequest: response_text_path: Path output_dir: Path run_id: str = "P133-GEM-MULTIMODAL-RESPONSE-CAPTURE-GATE" generated_at_utc: str | None = None source_image_pa

### 12. `05_EXPORTS/P138A2_R2_SELF_CONTAINED_PATH_CHECK_FIX_20260622_234501/P138A_MIGRATION_PAYLOAD.json`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `126`
- hits: `gem|portfolio|revolut|json|human_review|human review|review_required|risk|risque|decision|décision|no broker|no order|no sizing|P133`

> status", "target_sheet", "target_row_strategy", "write_status", "human_review_status", "blockers" ], "migration_candidates": [ { "migration_id": "MIG-prompt_01_portfolio_analysis-fe293d100e8c", "source_spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0", "source_tab": "GPT_PROMPT_RUNTIME_SPEC", "source_row": 2, "source_hash": "fe293d100e8c14fd942573a8bf46c52bf36ac6fbbb2c463543cf4eae265b0729", "prompt_id": "prompt_01_portfolio_analysis", "base_prompt_id": null, "parent_prompt_id": null, "prompt_family": null, "gem_id": "UNKNOWN_GEM", "prompt_profile": null, "record_type": null, "status": null, "validation_status": "VALIDATED", "is_reference_locked": false, "raw_prompt_text": "", "prompt_text_field_used": null, "python_simplification_action": "NORMALIZE_AND_PREPARE_VALIDATED_UPSERT", "p137_correction_status": "BLOCKED_NO_PROMPT_TEXT", "p133_compatibility_status": "BLOCKED", "ta

### 13. `mvp_qaic_py/p137_prompt_corrections_apply_queue.py`

- kind: `CURRENT_RUNTIME_CONTRACT_REFERENCE`
- score: `124`
- hits: `gem|portfolio|capture|image|revolut|json|human_review|human review|review_required|risk|no broker|no order|no sizing|P132|P133|path_prompt_bonus`

> not candidates: return None return max(candidates, key=lambda path: path.stat().st_mtime) def _fallback_prompt(gem_id: str) -> str: return f"""# MVP QAIC — GEM Portfolio Prompt Base Gem cible: {gem_id} Prompt source non trouvé automatiquement. Utiliser ce fichier comme base temporaire, puis remplacer par le dernier prompt P132/P134 validé. Objectif: analyser une capture Revolut X / portefeuille crypto en mode éducatif, analytique, human review only. Sécurité: - no broker - no order - no sizing - no auto apply """ def load_source_prompt(request: P137Request) -> tuple[str, Path | None]: selected = request.prompt_file or _find_latest_prompt(request.exports_dir) if selected and selected.exists(): return _read_text(selected), selected return _fallback_prompt(request.gem_id), None def build_prompt_corrections_queue(gem_profile: dict[str, Any]) -> list[dict[str, Any]]: gem_id = gem_profile["gem

### 14. `mvp_qaic_py/gem_prompt_runner_pack.py`

- kind: `PROMPT_RELATED_SOURCE_CANDIDATE`
- score: `124`
- hits: `gem|portfolio|capture|image|revolut|json|human_review|review_required|risk|decision|path_prompt_bonus`

> t[str] = [] review_questions: list[str] = [] if mode not in INPUT_MODES: missing_data.append("valid_input_mode") review_questions.append("Confirm the portfolio input mode.") if mode == "NONE": missing_data.extend(["portfolio_positions", "portfolio_values"]) review_questions.append( "Provide portfolio positions as pasted text, structured JSON, or image reference." ) elif mode == "IMAGE_REVIEW_REQUIRED": missing_data.extend( [ "human_confirmed_asset_symbols", "human_confirmed_quantities", "human_confirmed_values", "human_confirmed_visible_prices_if_any", ] ) review_questions.extend( [ "Confirm every visible asset symbol.", "Confirm every visible quantity.", "Confirm every visible value.", "Confirm that no hidden line is being assumed.", ] ) elif mode in {"PASTED_TEXT", "PASTED_TEXT_DRAFT"}: if not pasted_text or not pasted_text.strip(): missing_data.append("pasted_portfolio_text") review_q

### 15. `05_EXPORTS/P118_GEM_DAILY_OPERATOR_SHORTCUT_20260622_133524/P118_RUNTIME_PACK/P116_GEM_PROMPT_COPY_PASTE.md`

- kind: `EXPORT_ARCHIVE_REFERENCE`
- score: `124`
- hits: `gem|portfolio|image|revolut|json|human_review|human review|review_required|risk|decision|path_prompt_bonus`

> # MVP QAIC - GEM Portfolio Review Prompt ## Mission Review the portfolio input for educational and decision-support purposes only. Return a structured JSON answer matching the expected schema. ## Hard safety rules - HUMAN_REVIEW_ONLY. - Do not place, suggest placing, cancel, replace, or automate any order. - Do not calculate position sizing. - Do not claim OCR or automatic image extraction. - Do not invent assets, quantities, prices, values, TP, SL, or trailing levels. - If the input is incomplete or image-based, return REVIEW_REQUIRED with missing_data. ## Normalized portfolio input ```json { "blockers": [], "human_review_required": true, "image_reference": null, "input_mode": "PASTED_TEXT_DRAFT", "integration": { "p113_normalizer": "fallback_used", "warnings": [] }, "missing_data": [], "no_ocr_claim": true, "no_visual_extraction_claim": true, "notes": "P118 daily operator shortcut. Hum

## Next

`P165_HUMAN_REVIEW_REFERENCE_PROMPT_SELECTION_OR_STOP`
