#!/usr/bin/env python3
"""Render a report-helper internal Markdown build file to PDF with Chrome fallback."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from report_helper_config import get_config_path, get_config_value


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MD_TO_PDF = SKILL_DIR / "scripts" / "md_to_pdf.py"
DEFAULT_CHROME = get_config_path("chrome_path")
DEFAULT_WORK_DIR = get_config_path("work_dir", "./output/work")


def has_pdf(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Render internal Markdown build file to PDF with fallback")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", default="")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--author", default=get_config_value("author", ""))
    parser.add_argument("--md-to-pdf", type=Path, default=DEFAULT_MD_TO_PDF)
    parser.add_argument("--chrome", type=Path, default=DEFAULT_CHROME)
    args = parser.parse_args()
    html_path = (DEFAULT_WORK_DIR or args.output.parent) / f"{args.output.stem}.html"

    cmd = [
        sys.executable,
        str(args.md_to_pdf),
        str(args.input),
        str(args.output),
        "--author",
        args.author,
        "--html-output",
        str(html_path),
    ]
    if args.title:
        cmd.extend(["--title", args.title])
    if args.subtitle:
        cmd.extend(["--subtitle", args.subtitle])

    env = os.environ.copy()
    dyld_fallback = get_config_value("dyld_fallback_library_path", "")
    if dyld_fallback:
        env.setdefault("DYLD_FALLBACK_LIBRARY_PATH", dyld_fallback)
    result = subprocess.run(cmd, env=env)
    if result.returncode == 0 and has_pdf(args.output):
        print(f"[OK] PDF generated: {args.output}")
        return 0

    if not html_path.exists():
        print("[ERROR] md_to_pdf failed and no HTML fallback was generated", file=sys.stderr)
        return result.returncode or 1
    if args.chrome is None:
        print("[ERROR] Chrome path is not configured for fallback rendering", file=sys.stderr)
        return result.returncode or 1
    if not args.chrome.exists():
        print(f"[ERROR] Chrome not found: {args.chrome}", file=sys.stderr)
        return result.returncode or 1

    chrome_cmd = [
        str(args.chrome),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={args.output}",
        html_path.as_uri(),
    ]
    chrome_result = subprocess.run(chrome_cmd)
    if chrome_result.returncode == 0 and has_pdf(args.output):
        html_path.unlink(missing_ok=True)
        print(f"[OK] PDF generated with Chrome fallback: {args.output}")
        return 0
    print("[ERROR] Chrome fallback failed", file=sys.stderr)
    return chrome_result.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
