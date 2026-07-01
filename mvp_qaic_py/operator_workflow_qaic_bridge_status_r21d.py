"""R21D no-runtime operator workflow status for the MVP QAIC -> QAIC bridge.

This module is intentionally static and side-effect free. It performs no runtime
startup, no network call, no provider call, no broker action, and no sheet/BQ
write. It gives the operator a stable bridge-status model while Reflex runtime
remains paused by R21B.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from typing import Any

WORKFLOW_ID = "R21D_OPERATOR_WORKFLOW_QAIC_BRIDGE_STATUS_NO_RUNTIME"
QAIC_BRIDGE_CONTRACT_ID = "MVP_QAIC_TO_QAIC_BRIDGE_R1"
QAIC_BRIDGE_ROUTE = "/qaic-bridge"
REFLEX_RUNTIME_STATUS = "PAUSED"
H9_CHAIN_STATUS = "CLOSED_FAILED_NO_COMMIT_ROLLBACK_DONE"


@dataclass(frozen=True)
class OperatorWorkflowStep:
    """Single no-runtime operator workflow step."""

    order: int
    key: str
    title: str
    status: str
    operator_action: str
    evidence: str


@dataclass(frozen=True)
class QaicBridgeOperatorStatus:
    """Static status model for operator review and QAIC handoff."""

    workflow_id: str = WORKFLOW_ID
    qaic_bridge_contract_id: str = QAIC_BRIDGE_CONTRACT_ID
    qaic_bridge_route: str = QAIC_BRIDGE_ROUTE
    reflex_runtime_status: str = REFLEX_RUNTIME_STATUS
    h9_runtime_chain_status: str = H9_CHAIN_STATUS
    handoff_mode: str = "review_only_local_handoff"
    qaic_execution_allowed: bool = False
    human_review_required: bool = True
    safety_flags: dict[str, bool] = field(
        default_factory=lambda: {
            "no_runtime": True,
            "no_docker": True,
            "no_reflex_run": True,
            "no_provider_call": True,
            "no_broker_order_sizing": True,
            "no_sheet_bq_write": True,
            "no_apps_script_execution": True,
            "no_public_deploy": True,
        }
    )
    steps: tuple[OperatorWorkflowStep, ...] = field(
        default_factory=lambda: (
            OperatorWorkflowStep(
                1,
                "bridge_contract",
                "Verify MVP to QAIC bridge contract",
                "sealed",
                "Review the static handoff contract and confirm the review-only boundary.",
                "docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_CONTRACT_R1.md",
            ),
            OperatorWorkflowStep(
                2,
                "operator_cockpit_binding",
                "Review operator cockpit bridge status",
                "sealed",
                "Use the private cockpit route marker /qaic-bridge as the canonical bridge entry point.",
                "mvp_qaic_reflex_ui/qaic_bridge_operator_binding.py",
            ),
            OperatorWorkflowStep(
                3,
                "human_review_queue",
                "Prepare human-review handoff to QAIC",
                "ready",
                "Validate that the handoff remains local, review-only, and execution-disabled.",
                "data/samples/mvp_qaic_bridge/MVP_QAIC_TO_QAIC_BRIDGE_SAMPLE_R1.json",
            ),
            OperatorWorkflowStep(
                4,
                "reflex_runtime_boundary",
                "Keep Reflex runtime outside the critical path",
                "paused",
                "Do not restart Reflex runtime until the R21B runner policy is superseded by a reviewed runner.",
                "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            ),
        )
    )

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation."""

        return {
            "workflow_id": self.workflow_id,
            "qaic_bridge_contract_id": self.qaic_bridge_contract_id,
            "qaic_bridge_route": self.qaic_bridge_route,
            "reflex_runtime_status": self.reflex_runtime_status,
            "h9_runtime_chain_status": self.h9_runtime_chain_status,
            "handoff_mode": self.handoff_mode,
            "qaic_execution_allowed": self.qaic_execution_allowed,
            "human_review_required": self.human_review_required,
            "safety_flags": dict(self.safety_flags),
            "steps": [step.__dict__ for step in self.steps],
        }


def build_bridge_operator_status() -> QaicBridgeOperatorStatus:
    """Build the no-runtime operator bridge status model."""

    return QaicBridgeOperatorStatus()


def render_status_markdown(status: QaicBridgeOperatorStatus | None = None) -> str:
    """Render the bridge status as operator-friendly Markdown."""

    status = status or build_bridge_operator_status()
    lines = [
        "# R21D - MVP QAIC operator workflow and QAIC bridge status",
        "",
        f"WORKFLOW_ID={status.workflow_id}",
        f"QAIC_BRIDGE_CONTRACT_ID={status.qaic_bridge_contract_id}",
        f"QAIC_BRIDGE_ROUTE={status.qaic_bridge_route}",
        f"REFLEX_RUNTIME_STATUS={status.reflex_runtime_status}",
        f"H9_RUNTIME_CHAIN_STATUS={status.h9_runtime_chain_status}",
        f"HANDOFF_MODE={status.handoff_mode}",
        f"QAIC_EXECUTION_ALLOWED={status.qaic_execution_allowed}",
        f"HUMAN_REVIEW_REQUIRED={status.human_review_required}",
        "",
        "## Safety flags",
    ]
    for key, value in status.safety_flags.items():
        lines.append(f"- {key}={value}")
    lines.extend(["", "## Operator steps"])
    for step in status.steps:
        lines.append(
            f"{step.order}. [{step.status}] {step.title} - {step.operator_action} Evidence: {step.evidence}"
        )
    return "\n".join(lines) + "\n"


def render_static_preview_html(status: QaicBridgeOperatorStatus | None = None) -> str:
    """Render a static WYSIWYG-like HTML preview with no runtime dependency."""

    status = status or build_bridge_operator_status()
    flags = "".join(
        f"<li><code>{escape(key)}</code>: <strong>{str(value)}</strong></li>"
        for key, value in status.safety_flags.items()
    )
    steps = "".join(
        "<article class='step'>"
        f"<span class='badge'>{escape(step.status)}</span>"
        f"<h3>{step.order}. {escape(step.title)}</h3>"
        f"<p>{escape(step.operator_action)}</p>"
        f"<p><small>Evidence: <code>{escape(step.evidence)}</code></small></p>"
        "</article>"
        for step in status.steps
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <title>R21D MVP QAIC Operator Workflow</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; background: #f6f7fb; color: #172033; }}
    main {{ max-width: 1040px; margin: auto; }}
    .hero, .step {{ background: white; border: 1px solid #d9deea; border-radius: 16px; padding: 20px; margin: 14px 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }}
    .card {{ background: #ffffff; border: 1px solid #d9deea; border-radius: 14px; padding: 14px; }}
    .badge {{ display: inline-block; border: 1px solid #9aa8c7; border-radius: 999px; padding: 4px 10px; font-size: 12px; text-transform: uppercase; }}
    code {{ background: #edf1f8; padding: 2px 5px; border-radius: 6px; }}
  </style>
</head>
<body>
<main>
  <section class=\"hero\">
    <h1>R21D - MVP QAIC operator workflow</h1>
    <p><strong>Bridge:</strong> {escape(status.qaic_bridge_contract_id)} at <code>{escape(status.qaic_bridge_route)}</code></p>
    <p><strong>Reflex runtime:</strong> {escape(status.reflex_runtime_status)}. Product work continues without runtime blocking.</p>
  </section>
  <section class=\"grid\">
    <div class=\"card\"><strong>Handoff mode</strong><br>{escape(status.handoff_mode)}</div>
    <div class=\"card\"><strong>QAIC execution allowed</strong><br>{status.qaic_execution_allowed}</div>
    <div class=\"card\"><strong>Human review required</strong><br>{status.human_review_required}</div>
    <div class=\"card\"><strong>H9 chain</strong><br>{escape(status.h9_runtime_chain_status)}</div>
  </section>
  <section class=\"hero\">
    <h2>Safety flags</h2>
    <ul>{flags}</ul>
  </section>
  <section>
    <h2>Operator steps</h2>
    {steps}
  </section>
</main>
</body>
</html>
"""
