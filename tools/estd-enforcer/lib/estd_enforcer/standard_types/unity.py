"""Unity client route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    if Path(lowered).suffix == ".cs" or lowered.startswith(("assets/", "projectsettings/", "packages/")):
        return {"route.unity-client"}
    return set()
