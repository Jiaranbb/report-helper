#!/usr/bin/env python3
"""Append a report entry to a markdown log."""

from __future__ import annotations

import argparse
from pathlib import Path

from report_helper_config import get_config_path, get_config_value


DEFAULT_LOG = get_config_path("log_path", "output/report-log.md")
DEFAULT_INSERT_AFTER_HEADING = str(get_config_value("log_insert_after_heading", ""))
DEFAULT_INSERT_AFTER_MARKER = str(get_config_value("log_insert_after_marker", "\n---\n\n"))


def insert_after_log_header(log_text: str, entry: str, heading: str = "", marker: str = "\n---\n\n") -> str:
    if heading and heading in log_text:
        title_index = log_text.index(heading)
        if marker in log_text[title_index:]:
            insert_at = log_text.index(marker, title_index) + len(marker)
            return log_text[:insert_at] + entry + log_text[insert_at:]
    if log_text and not log_text.endswith("\n"):
        log_text += "\n"
    return log_text + "\n" + entry


def build_entry(date: str, title: str, body: str, links: list[str], bullets: list[str]) -> str:
    lines = [f"## [{date}] write | {title}", "", body.strip(), ""]
    for link in links:
        lines.append(f"- {link}")
    for bullet in bullets:
        lines.append(f"- {bullet}")
    return "\n".join(lines).rstrip() + "\n\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Append report-helper entry to markdown log")
    parser.add_argument("--log-path", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--insert-after-heading", default=DEFAULT_INSERT_AFTER_HEADING)
    parser.add_argument("--insert-after-marker", default=DEFAULT_INSERT_AFTER_MARKER)
    parser.add_argument("--date", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--link", action="append", default=[])
    parser.add_argument("--bullet", action="append", default=[])
    args = parser.parse_args()

    entry = build_entry(args.date, args.title, args.body, args.link, args.bullet)
    args.log_path.parent.mkdir(parents=True, exist_ok=True)
    log_text = args.log_path.read_text(encoding="utf-8") if args.log_path.exists() else ""
    if entry.strip() in log_text:
        print(f"[SKIP] entry already exists: {args.title}")
        return 0
    args.log_path.write_text(
        insert_after_log_header(log_text, entry, args.insert_after_heading, args.insert_after_marker),
        encoding="utf-8",
    )
    print(f"[OK] appended log entry: {args.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
