"""Database route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    database_tokens = ("migration", "migrations", "schema", "mysql", "mongo", "atlas")
    if Path(lowered).suffix == ".sql" or any(token in lowered for token in database_tokens):
        return {"route.database"}
    return set()
