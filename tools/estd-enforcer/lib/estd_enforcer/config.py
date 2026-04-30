"""Consumer repository config parsing."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .constants import DEFAULT_CONFIG
from .errors import ToolError


def parse_scalar(value: str) -> Any:
    cleaned = value.strip().strip('"').strip("'")
    lowered = cleaned.lower()
    if cleaned == "[]":
        return []
    if cleaned.startswith("[") and cleaned.endswith("]"):
        inner = cleaned[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"').strip("'") for item in inner.split(",")]
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?[0-9]+", cleaned):
        return int(cleaned)
    return cleaned


def load_config(repo: Path, config_path: Path) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    resolved = config_path if config_path.is_absolute() else repo / config_path
    if not resolved.exists():
        return config

    lines = resolved.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.split("#", 1)[0].strip()
        index += 1
        if not line or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in config:
            continue
        value = value.strip()
        if key == "requiredStaticTools" and not value:
            items: list[str] = []
            while index < len(lines) and lines[index].lstrip().startswith("- "):
                items.append(lines[index].split("- ", 1)[1].strip().strip('"').strip("'"))
                index += 1
            config[key] = items
        else:
            config[key] = parse_scalar(value)

    if int(config.get("version", 0)) not in {1, 2}:
        raise ToolError("Only .estd config versions 1 and 2 are supported.")
    if config["mode"] not in {"blocking", "advisory"}:
        raise ToolError("Config mode must be 'blocking' or 'advisory'.")
    if config["scope"] not in {"changed-files", "full-repo"}:
        raise ToolError("Config scope must be 'changed-files' or 'full-repo'.")
    if config["validationStrategy"] != "static-first":
        raise ToolError("Config validationStrategy must be 'static-first'.")
    if config["llmPolicy"] not in {"gaps-only", "disabled"}:
        raise ToolError("Config llmPolicy must be 'gaps-only' or 'disabled'.")
    if int(config["minScore"]) < 0 or int(config["minScore"]) > 100:
        raise ToolError("Config minScore must be between 0 and 100.")
    if not isinstance(config["requiredStaticTools"], list):
        raise ToolError("Config requiredStaticTools must be a list.")
    return config


def is_submodule_opted_in(repo: Path, config: dict[str, Any]) -> bool:
    standards_path = str(config["standardsPath"]).strip().strip("/")
    if not standards_path:
        return False

    submodule_path = repo / standards_path
    gitmodules_path = repo / ".gitmodules"
    if not submodule_path.exists() or not gitmodules_path.exists():
        return False
    if not (submodule_path / "tools/estd-enforcer/bin/estd-enforce").exists():
        return False

    try:
        gitmodules = gitmodules_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False

    pattern = re.compile(r"^\s*path\s*=\s*" + re.escape(standards_path) + r"\s*$", re.MULTILINE)
    return bool(pattern.search(gitmodules))
