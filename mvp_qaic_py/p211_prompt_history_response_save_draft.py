from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from mvp_qaic_py.p210_prompt_history_operator_workflow import (
    build_prompt_history_operator_workflow,
)

_SAFE_CHARS = re.compile(r"[^A-Za-z0-9_.-]+")
MAX_RESPONSE_PREVIEW_CHARS = 1200


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_draft_slug(value: str, *, fallback: str = "gem_response_draft") -> str:
    slug = _SAFE_CHARS.sub("_", value.strip())
    slug = slug.strip("._-")
    return slug[:120] or fallback


def build_response_draft_payload(
    project_root: str | Path,
    *,
    card_id: str | None = None,
    query: str = "",
    gem_response_text: str,
    generated_at: str | None = None,
) -> dict[str, Any]:
    workflow = build_prompt_history_operator_workflow(
        project_root,
        card_id=card_id,
        action="save_gem_response_local",
        query=query,
        gem_response_text=gem_response_text,
        generated_at=generated_at,
    )

    blockers = list(workflow.get("blockers", []))
    selected_path = workflow.get("workflow", {}).get("selected_path")
    selected_title = workflow.get("workflow", {}).get("selected_title")

    status = "OK_P211_PROMPT_HISTORY_RESPONSE_DRAFT_READY"
    if blockers:
        status = "REVIEW_P211_PROMPT_HISTORY_RESPONSE_DRAFT"

    stamp = (generated_at or _utc_now()).replace(":", "").replace("-", "")
    stamp = safe_draft_slug(stamp, fallback="timestamp")
    title_slug = safe_draft_slug(str(selected_title or "unselected_prompt"))

    draft_id = f"P211_{stamp}_{title_slug}"

    response_text = gem_response_text.strip()
    response_preview = response_text[:MAX_RESPONSE_PREVIEW_CHARS]

    return {
        "STATUS": status,
        "draft_id": draft_id,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "generated_at": workflow.get("generated_at"),
        "project_root": workflow.get("project_root"),
        "source_prompt_path": selected_path,
        "source_prompt_title": selected_title,
        "response_text_present": bool(response_text),
        "response_preview": response_preview,
        "write_plan": {
            "mode": "LOCAL_OPERATOR_REVIEW_ONLY",
            "json_filename": f"{draft_id}.json",
            "md_filename": f"{draft_id}.md",
            "auto_apply_gem_response": False,
            "requires_human_review": True,
        },
        "workflow": workflow,
        "local_only": True,
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "provider_call_executed": False,
        "auto_apply_gem_response": False,
        "google_sheets_write": False,
        "apps_script_execution": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P212_PROMPT_HISTORY_RESPONSE_DRAFT_UI_FAST_FUSE",
    }


def build_response_draft_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# P211 — GEM Response Draft",
        "",
        f"- Status: `{payload['STATUS']}`",
        f"- Draft ID: `{payload['draft_id']}`",
        f"- Source prompt: `{payload.get('source_prompt_path')}`",
        "- Mode: `LOCAL_OPERATOR_REVIEW_ONLY`",
        "- Human review required: `true`",
        "- Auto-apply GEM response: `false`",
        "",
        "## Response preview",
        "",
        payload.get("response_preview") or "_No response text provided._",
        "",
    ]
    return "\n".join(lines)


def write_response_draft_files(
    payload: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Any]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / payload["write_plan"]["json_filename"]
    md_path = output / payload["write_plan"]["md_filename"]

    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    md_path.write_text(build_response_draft_markdown(payload), encoding="utf-8")

    return {
        **payload,
        "json_path": str(json_path),
        "md_path": str(md_path),
        "files_written": True,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--card-id", default=None)
    parser.add_argument("--query", default="")
    parser.add_argument("--gem-response-text", required=True)
    parser.add_argument("--generated-at", default=None)
    args = parser.parse_args()

    payload = build_response_draft_payload(
        args.project_root,
        card_id=args.card_id,
        query=args.query,
        gem_response_text=args.gem_response_text,
        generated_at=args.generated_at,
    )

    if args.output_dir:
        payload = write_response_draft_files(payload, args.output_dir)

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
