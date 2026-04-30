"""ESTD exception file parsing and validation."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

from .estd_refs import doc_path_for, section_exists
from .config import parse_scalar


def parse_exception_records(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current is not None:
                records.append(current)
            current = {}
            stripped = stripped[2:].strip()
        if current is None:
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        current[key.strip()] = str(parse_scalar(value))
    if current is not None:
        records.append(current)
    return records


def validate_exceptions(repo: Path, config: dict[str, Any]) -> list[str]:
    exception_path = Path(str(config["exceptionsFile"]))
    resolved = exception_path if exception_path.is_absolute() else repo / exception_path
    records = parse_exception_records(resolved)
    errors: list[str] = []
    today = dt.date.today()
    required = [
        "id",
        "estdId",
        "section",
        "reason",
        "approver",
        "expiresOn",
        "remediationPlan",
        "ticket",
    ]

    for index, record in enumerate(records):
        label = record.get("id", f"record {index + 1}")
        for field in required:
            if not record.get(field):
                errors.append(f"Exception {label} missing {field}.")
        if str(record.get("securityCritical", "")).lower() != "false":
            errors.append(f"Exception {label} must declare securityCritical: false.")

        doc_id = record.get("estdId", "")
        section = record.get("section", "")
        doc_path = doc_path_for(doc_id)
        if doc_path is None:
            errors.append(f"Exception {label} cites unknown ESTD doc: {doc_id}.")
        elif section and not section_exists(doc_path, section):
            errors.append(f"Exception {label} cites missing section {doc_id} {section}.")

        try:
            expires_on = dt.date.fromisoformat(record.get("expiresOn", ""))
            if expires_on < today:
                errors.append(f"Exception {label} expired on {expires_on.isoformat()}.")
        except ValueError:
            errors.append(f"Exception {label} has invalid expiresOn date.")

    return errors
