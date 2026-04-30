"""Jenkins CI/CD route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    name = Path(lowered).name
    suffix = Path(lowered).suffix
    if name == "jenkinsfile" or lowered.startswith("jenkins/") or suffix == ".groovy":
        return {"route.jenkins-cicd"}
    return set()
