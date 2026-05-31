#!/usr/bin/env python3
"""Check report-helper first-use environment and configuration."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from report_helper_config import DEFAULT_CONFIG_PATH, load_config


SKILL_DIR = Path(__file__).resolve().parents[1]
CONFIG_EXAMPLE = SKILL_DIR / "config.example.json"
VALID_FORMATS = {"pdf", "epub"}


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def normalize_formats(value: object) -> list[str]:
    if isinstance(value, str):
        items = [item.strip().lower() for item in value.split(",")]
    elif isinstance(value, list):
        items = [str(item).strip().lower() for item in value]
    else:
        return []
    return [item for item in items if item]


def status_line(ok: bool, message: str) -> str:
    return f"[{'OK' if ok else '!!'}] {message}"


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    print("report-helper environment check")

    py_ok = sys.version_info >= (3, 9)
    print(status_line(py_ok, f"python: {sys.version.split()[0]}"))
    if not py_ok:
        errors.append("Python 3.9+ is required.")

    example_ok = CONFIG_EXAMPLE.exists()
    print(status_line(example_ok, f"config.example.json: {CONFIG_EXAMPLE}"))
    if not example_ok:
        errors.append("config.example.json is missing.")

    local_ok = DEFAULT_CONFIG_PATH.exists()
    print(status_line(local_ok, f"config.local.json: {DEFAULT_CONFIG_PATH}"))
    if not local_ok:
        errors.append("Create config.local.json from config.example.json before first use.")

    config = load_config()
    author = str(config.get("author", "")).strip()
    author_ok = bool(author)
    print(status_line(author_ok, "author is configured" if author_ok else "author is empty"))
    if not author_ok:
        errors.append("Fill author in config.local.json. It is the report byline.")

    formats = normalize_formats(config.get("delivery_formats", []))
    formats_ok = bool(formats) and all(item in VALID_FORMATS for item in formats)
    print(status_line(formats_ok, f"delivery_formats: {formats or '(empty)'}"))
    if not formats_ok:
        errors.append('Set delivery_formats to ["pdf"], ["epub"], or ["pdf", "epub"].')

    output_dir = Path(str(config.get("output_dir", "./output"))).expanduser()
    work_dir = Path(str(config.get("work_dir", "./output/work"))).expanduser()
    intermediate_dir = Path(str(config.get("intermediate_dir", "./output/intermediate"))).expanduser()
    print(status_line(True, f"output_dir: {output_dir}"))
    print(status_line(True, f"work_dir: {work_dir}"))
    print(status_line(True, f"intermediate_dir: {intermediate_dir}"))

    markdown_ok = has_module("markdown")
    weasyprint_ok = has_module("weasyprint")
    print(status_line(markdown_ok, "python package: markdown"))
    print(status_line(weasyprint_ok, "python package: weasyprint"))

    chrome_value = str(config.get("chrome_path", "")).strip()
    chrome_path = Path(chrome_value).expanduser() if chrome_value else None
    chrome_ok = bool(chrome_path and chrome_path.exists())
    if chrome_value:
        print(status_line(chrome_ok, f"chrome_path: {chrome_path}"))
    else:
        print(status_line(False, "chrome_path is not configured"))
        warnings.append("Chrome fallback is unavailable unless chrome_path or REPORT_HELPER_CHROME is configured.")

    if "pdf" in formats:
        if not markdown_ok:
            errors.append("PDF generation requires the markdown package for the internal Markdown-to-HTML render step.")
        if not weasyprint_ok and not chrome_ok:
            errors.append("PDF generation requires WeasyPrint or a configured Chrome fallback.")

    if "epub" in formats and not markdown_ok:
        warnings.append("EPUB can be generated without markdown, but installing markdown improves formatting.")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("\nRequired fixes:")
        for error in errors:
            print(f"- {error}")
        print("\nSuggested install command:")
        print("python3 -m pip install markdown weasyprint")
        return 1

    print("\nEnvironment check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
