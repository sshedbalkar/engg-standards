"""ESTD document and citation helpers."""

from __future__ import annotations

import re
from pathlib import Path

from .constants import DOCS_ROOT, STANDARDS_ROOT, VALIDATORS_ROOT


def validator_id_for(route_id: str) -> str:
    return "validator." + route_id.removeprefix("route.")


def doc_path_for(doc_id: str) -> Path | None:
    matches = sorted(DOCS_ROOT.glob(f"{doc_id}_-*.md"))
    return matches[0] if matches else None


def extract_validator_docs(validator_path: Path | None) -> list[str]:
    if validator_path is None:
        return []
    content = validator_path.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"ESTD[0-9]+", content)), key=lambda item: int(item[4:]))


def normalize_section(section: str) -> str:
    cleaned = section.strip()
    cleaned = re.sub(r"^ESTD[0-9]+\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.lstrip("§").strip()
    return cleaned


def heading_matches(section: str, heading: str) -> bool:
    cleaned = normalize_section(section)
    if not cleaned:
        return False
    normalized_heading = heading.lower()
    normalized_section = cleaned.lower()
    numeric = re.match(r"^([0-9]+(?:\.[0-9]+)*)", cleaned)
    if numeric:
        number = re.escape(numeric.group(1))
        return re.search(rf"^#+\s+{number}(\.|\s|$)", heading) is not None
    return normalized_section in normalized_heading


def section_exists(doc_path: Path, section: str) -> bool:
    for line in doc_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") and heading_matches(section, line):
            return True
    return False
