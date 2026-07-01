"""Static review-only MVP QAIC to QAIC Python bridge contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


CONTRACT_ID = "MVP_QAIC_TO_QAIC_BRIDGE_R1"
CONTRACT_VERSION = "R1"
MODE = "REVIEW_ONLY_LOCAL_HANDOFF"
SOURCE_SYSTEM = "MVP_QAIC"
TARGET_SYSTEM = "QAIC_PY"

REQUIRED_TOP_LEVEL_KEYS = (
    "contract_id",
    "contract_version",
    "mode",
    "source_system",
    "target_system",
    "created_by",
    "created_at_utc",
    "safety",
    "portfolio_input",
    "gem_prompt",
    "gem_response",
    "review_queue",
    "decision_journal",
    "qaic_import",
    "evidence",
)

REQUIRED_SAFETY_FLAGS = {
    "no_runtime": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
}

REQUIRED_SCOPE_MODULES = (
    "P112_GEM_PORTFOLIO_PROMPT_MODULE",
    "P113_PORTFOLIO_INPUT_NORMALIZER_IMAGE_REVIEW",
    "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
    "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE",
    "P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE",
    "P196_REAL_CASE_PORTFOLIO_GEM_INPUTS",
)

FORBIDDEN_ACTIONS = (
    "broker action",
    "order action",
    "sizing action",
    "provider live call",
    "Sheet/BQ write",
    "Apps Script execution",
    "runtime launch",
    "public deploy",
)


def build_bridge_contract_payload() -> dict[str, Any]:
    """Build the static R1 review-only bridge payload."""
    return {
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "mode": MODE,
        "source_system": SOURCE_SYSTEM,
        "target_system": TARGET_SYSTEM,
        "created_by": "P_R16F2H9A_R3",
        "created_at_utc": "2026-07-01T15:10:04Z",
        "safety": {
            **REQUIRED_SAFETY_FLAGS,
            "scope_modules": list(REQUIRED_SCOPE_MODULES),
            "forbidden_actions": list(FORBIDDEN_ACTIONS),
        },
        "portfolio_input": {
            "source_module": "P196_REAL_CASE_PORTFOLIO_GEM_INPUTS",
            "reference_path": (
                "01_OPERATOR_INPUTS/P196_REAL_CASE_PORTFOLIO_GEM_INPUTS/"
                "TEXT/README_INPUTS.md"
            ),
            "capture_mode": "local_operator_supplied_read_only",
        },
        "gem_prompt": {
            "source_module": "P112_GEM_PORTFOLIO_PROMPT_MODULE",
            "artifact_role": "portfolio_prompt_source",
            "handoff_state": "review_ready",
        },
        "gem_response": {
            "source_module": "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
            "artifact_role": "captured_response_source",
            "handoff_state": "review_queue_ready",
        },
        "review_queue": {
            "source_module": "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
            "required_review_state": "human_review_required",
        },
        "decision_journal": {
            "source_module": "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE",
            "artifact_role": "decision_journal_candidate",
            "write_policy": "local_candidate_only",
        },
        "qaic_import": {
            "import_mode": "review_only_import_ready",
            "target_system": TARGET_SYSTEM,
            "accepted_payload_state": "analysis_ready_read_only",
            "execution_allowed": False,
        },
        "evidence": {
            "contract_doc": "docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_CONTRACT_R1.md",
            "status_doc": "docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_STATUS_R1.md",
            "sample_json": (
                "data/samples/mvp_qaic_bridge/"
                "MVP_QAIC_TO_QAIC_BRIDGE_SAMPLE_R1.json"
            ),
        },
    }


def validate_bridge_contract_payload(payload: Mapping[str, Any]) -> list[str]:
    """Return human-readable validation errors for the R1 bridge payload."""
    errors: list[str] = []

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in payload:
            errors.append(f"missing top-level key: {key}")

    expected_constants = {
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "mode": MODE,
        "source_system": SOURCE_SYSTEM,
        "target_system": TARGET_SYSTEM,
    }
    for key, expected in expected_constants.items():
        if payload.get(key) != expected:
            errors.append(f"{key} must be {expected}")

    safety = payload.get("safety")
    if not isinstance(safety, Mapping):
        errors.append("safety must be a mapping")
        safety = {}

    for key, expected in REQUIRED_SAFETY_FLAGS.items():
        if safety.get(key) is not expected:
            errors.append(f"safety.{key} must be {expected}")

    scope_modules = safety.get("scope_modules")
    if not isinstance(scope_modules, list):
        errors.append("safety.scope_modules must be a list")
        scope_modules = []
    for module in REQUIRED_SCOPE_MODULES:
        if module not in scope_modules:
            errors.append(f"safety.scope_modules missing {module}")

    forbidden_actions = safety.get("forbidden_actions")
    if not isinstance(forbidden_actions, list):
        errors.append("safety.forbidden_actions must be a list")
        forbidden_actions = []
    for action in FORBIDDEN_ACTIONS:
        if action not in forbidden_actions:
            errors.append(f"safety.forbidden_actions missing {action}")

    qaic_import = payload.get("qaic_import")
    if not isinstance(qaic_import, Mapping):
        errors.append("qaic_import must be a mapping")
        qaic_import = {}
    if qaic_import.get("import_mode") != "review_only_import_ready":
        errors.append("qaic_import.import_mode must be review_only_import_ready")
    if qaic_import.get("execution_allowed") is not False:
        errors.append("qaic_import.execution_allowed must be False")

    return errors


def load_bridge_contract_sample(path: Path | str) -> dict[str, Any]:
    """Load a bridge contract sample JSON file."""
    sample_path = Path(path)
    return json.loads(sample_path.read_text(encoding="utf-8"))
