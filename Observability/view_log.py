#!/usr/bin/env python3
"""Pretty-print recent events from events.jsonl as a table."""

import json
import sys
from pathlib import Path

LOG_PATH = Path(__file__).parent / "events.jsonl"

DEFAULT_LIMIT = 20

# Column widths
TIME_W, TOOL_W, STATUS_W = 19, 12, 7


def load_events():
    if not LOG_PATH.exists():
        return []
    events = []
    with LOG_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def format_time(ts: str) -> str:
    # "2026-09-24T15:53:16.427642+00:00" -> "2026-09-24 15:53:16"
    return ts.replace("T", " ")[:19]


def print_table(events):
    header = f"{'TIME':<{TIME_W}}  {'TOOL':<{TOOL_W}}  {'STATUS':<{STATUS_W}}  DETAIL"
    print(header)
    print("-" * len(header))
    for e in events:
        time_str = format_time(e.get("timestamp", ""))
        tool = (e.get("tool_name") or "?")[:TOOL_W]
        status = "ok" if e.get("success", True) else "FAIL"
        detail = e.get("input_summary", "")
        # keep detail on one line, trim if long
        detail = detail.replace("\n", " ")
        if len(detail) > 60:
            detail = detail[:57] + "..."
        print(f"{time_str:<{TIME_W}}  {tool:<{TOOL_W}}  {status:<{STATUS_W}}  {detail}")


def main():
    limit = DEFAULT_LIMIT
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            pass

    events = load_events()
    if not events:
        print("No events logged yet.")
        return

    recent = events[-limit:]
    print(f"Showing last {len(recent)} of {len(events)} events\n")
    print_table(recent)


if __name__ == "__main__":
    main()