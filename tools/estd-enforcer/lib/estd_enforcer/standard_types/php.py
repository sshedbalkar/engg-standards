"""PHP monolith route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    name = Path(lowered).name
    if Path(lowered).suffix == ".php" or name in {"composer.json", "composer.lock"}:
        return {"route.php-monolith"}
    return set()
