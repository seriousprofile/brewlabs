#!/usr/bin/env python3
"""Claude Code PostToolUse/PostToolUseFailure hook: appends one compact JSON line
per tool call to events.jsonl (metadata only, no full tool responses)."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_PATH = Path(__file__).parent / "events.jsonl"
MAX_SUMMARY_CHARS = 200

# The one input field that best identifies what each tool call did.
SUMMARY_FIELDS: dict[str, str] = {
    "Read": "file_path",
    "Write": "file_path",
    "Edit": "file_path",
    "NotebookEdit": "notebook_path",
    "Bash": "command",
    "PowerShell": "command",
    "Glob": "pattern",
    "Grep": "pattern",
    "Agent": "description",
    "Skill": "skill",
    "WebFetch": "url",
    "WebSearch": "query",
}


def truncate(text: str, limit: int = MAX_SUMMARY_CHARS) -> str:
    return text if len(text) <= limit else text[:limit] + "…"


def summarize_input(tool_name: str, tool_input: Any) -> str:
    """Return a short one-line description of the tool call's input."""
    if not isinstance(tool_input, dict):
        return ""
    field = SUMMARY_FIELDS.get(tool_name)
    if field and field in tool_input:
        return truncate(str(tool_input[field]))
    # Unknown tools (e.g. MCP): list the argument names, not their values.
    return truncate("args: " + ", ".join(sorted(tool_input)))


def succeeded(payload: dict[str, Any]) -> bool:
    if payload.get("hook_event_name") == "PostToolUseFailure":
        return False
    response = payload.get("tool_response")
    return not (isinstance(response, dict) and response.get("interrupted"))


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # If Claude Code sends nothing/malformed data, fail quietly
        # rather than breaking the tool call itself.
        return

    tool_name = payload.get("tool_name") or ""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": payload.get("session_id"),
        "tool_name": tool_name,
        "input_summary": summarize_input(tool_name, payload.get("tool_input")),
        "success": succeeded(payload),
    }

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


if __name__ == "__main__":
    main()
