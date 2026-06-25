"""Private operator preview selector for the MVP QAIC Reflex shell.

This module only prepares safe local commands and metadata.
It never starts a server, opens a browser, publishes, writes to Sheets/BQ,
or performs broker/order/sizing actions.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data_binding import build_local_data_binding_payload
from .navigation import ui_shell_payload
from .registry import SAFETY_FLAGS


@dataclass(frozen=True)
class PrivatePreviewCommand:
    command_id: str
    title: str
    command: tuple[str, ...]
    host: str
    port: int
    server_start_allowed: bool
    browser_open_allowed: bool
    public_deploy_allowed: bool
    live_action_allowed: bool
    operator_must_run_manually: bool


def build_private_preview_command() -> PrivatePreviewCommand:
    return PrivatePreviewCommand(
        command_id="REFLEX_LOCAL_PRIVATE_PREVIEW_MANUAL_ONLY",
        title="Manual local private Reflex preview",
        command=(
            "python",
            "-m",
            "reflex",
            "run",
            "--env",
            "dev",
            "--backend-host",
            "127.0.0.1",
            "--frontend-port",
            "3000",
        ),
        host="127.0.0.1",
        port=3000,
        server_start_allowed=False,
        browser_open_allowed=False,
        public_deploy_allowed=False,
        live_action_allowed=False,
        operator_must_run_manually=True,
    )


def build_private_preview_selector_payload() -> dict[str, object]:
    command = build_private_preview_command()
    ui_shell = ui_shell_payload()
    data_binding = build_local_data_binding_payload()

    return {
        "selector_status": "READY_FOR_MANUAL_PRIVATE_PREVIEW",
        "selected_command_id": command.command_id,
        "title": command.title,
        "manual_command": list(command.command),
        "host": command.host,
        "port": command.port,
        "server_start_allowed_now": command.server_start_allowed,
        "browser_open_allowed_now": command.browser_open_allowed,
        "public_deploy_allowed": command.public_deploy_allowed,
        "live_action_allowed": command.live_action_allowed,
        "operator_must_run_manually": command.operator_must_run_manually,
        "safety_flags": SAFETY_FLAGS,
        "ui_navigation_group_count": ui_shell["navigation_group_count"],
        "ui_navigation_item_count": ui_shell["navigation_item_count"],
        "data_binding_mode": data_binding["binding_mode"],
        "docs_source_count": data_binding["docs_source_count"],
        "export_source_count": data_binding["export_source_count"],
        "next_recommended_batch": "P_REFLEX_06_MANUAL_PRIVATE_PREVIEW_OBSERVATION_GATE",
    }


def selector_is_safe_for_local_private_preview() -> bool:
    payload = build_private_preview_selector_payload()
    return (
        payload["server_start_allowed_now"] is False
        and payload["browser_open_allowed_now"] is False
        and payload["public_deploy_allowed"] is False
        and payload["live_action_allowed"] is False
        and payload["operator_must_run_manually"] is True
        and payload["data_binding_mode"] == "LOCAL_READONLY"
        and payload["host"] == "127.0.0.1"
    )
