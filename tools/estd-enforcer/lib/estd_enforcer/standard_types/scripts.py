"""Internal scripts and automation route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    name = Path(lowered).name
    script_roots = ("scripts/", "bin/", "tools/")
    if Path(lowered).suffix in {".sh", ".py"} or lowered.startswith(script_roots) or name == "makefile":
        return {"route.internal-scripts"}
    return set()
