"""Report model factories."""

from __future__ import annotations

from typing import Any

from .estd_refs import validator_id_for


def static_result(
    check_id: str,
    status: str,
    message: str,
    route_id: str = "route.common",
    severity: str = "low",
    findings: list[dict[str, Any]] | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    return {
        "checkId": check_id,
        "routeId": route_id,
        "validatorId": validator_id_for(route_id),
        "status": status,
        "severity": severity,
        "message": message,
        "command": command or "",
        "findings": findings or [],
    }


def finding(
    finding_id: str,
    severity: str,
    route_id: str,
    doc_id: str,
    section: str,
    title: str,
    doc_path: str,
    file_path: str,
    line: int,
    message: str,
    recommendation: str,
    source: str = "static",
) -> dict[str, Any]:
    return {
        "id": finding_id,
        "severity": severity,
        "status": "open",
        "routeId": route_id,
        "estd": {
            "docId": doc_id,
            "section": section,
            "title": title,
            "path": doc_path,
        },
        "file": file_path,
        "line": line,
        "message": message,
        "recommendation": recommendation,
        "evidenceStatus": "known",
        "source": source,
    }
