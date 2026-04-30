"""Technical documentation route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    if Path(lowered).suffix == ".md" or any(token in lowered for token in ("adr", "runbook", "rca", "tad", "docs/")):
        return {"route.technical-docs"}
    return set()
