"""Java SEAM and SmartFox route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    name = Path(lowered).name
    suffix = Path(lowered).suffix
    if suffix == ".java" or name in {"pom.xml", "build.gradle", "settings.gradle"}:
        if any(token in lowered for token in ("smartfox", "/sfs", "sfs/", "extension", "room")):
            return {"route.smartfox-server"}
        return {"route.java-seam-api"}
    return set()
