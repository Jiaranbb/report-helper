#!/usr/bin/env python3
"""Shared configuration loader for report-helper scripts."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = SKILL_DIR / "config.local.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "output_dir": "./output",
    "work_dir": "./output/work",
    "intermediate_dir": "./output/intermediate",
    "log_path": "./output/report-log.md",
    "log_insert_after_heading": "",
    "log_insert_after_marker": "\n---\n\n",
    "author": "",
    "source": "web research",
    "chrome_path": "",
    "dyld_fallback_library_path": "",
}

ENV_MAP = {
    "output_dir": "REPORT_HELPER_OUTPUT_DIR",
    "work_dir": "REPORT_HELPER_WORK_DIR",
    "intermediate_dir": "REPORT_HELPER_INTERMEDIATE_DIR",
    "log_path": "REPORT_HELPER_LOG_PATH",
    "log_insert_after_heading": "REPORT_HELPER_LOG_INSERT_AFTER_HEADING",
    "log_insert_after_marker": "REPORT_HELPER_LOG_INSERT_AFTER_MARKER",
    "author": "REPORT_HELPER_AUTHOR",
    "source": "REPORT_HELPER_SOURCE",
    "chrome_path": "REPORT_HELPER_CHROME",
    "dyld_fallback_library_path": "REPORT_HELPER_DYLD_FALLBACK",
}


def _config_path(explicit_path: str | Path | None = None) -> Path:
    env_path = os.getenv("REPORT_HELPER_CONFIG")
    path = explicit_path or env_path or DEFAULT_CONFIG_PATH
    return Path(path).expanduser()


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"config must be a JSON object: {path}")
    return data


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    path = _config_path(config_path)

    if path.exists():
        config.update({key: value for key, value in _read_json(path).items() if value is not None})

    for key, env_name in ENV_MAP.items():
        value = os.getenv(env_name)
        if value not in (None, ""):
            config[key] = value

    return config


def get_config_value(key: str, default: Any = None) -> Any:
    return load_config().get(key, default)


def get_config_path(key: str, default: str | Path | None = None) -> Path | None:
    value = get_config_value(key, default)
    if value in (None, ""):
        return None
    return Path(str(value)).expanduser()
