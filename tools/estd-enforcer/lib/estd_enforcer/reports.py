"""Report validation, merging, rendering, and persistence."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .estd_refs import doc_path_for, section_exists, validator_id_for
from .constants import SCHEMA_VERSION
from .models import finding


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_report_shape(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ["schemaVersion", "status", "score", "routes", "findings"]
    for key in required:
        if key not in report:
            errors.append(f"Report missing required field: {key}")

    if report.get("schemaVersion") != SCHEMA_VERSION:
        errors.append("Report schemaVersion must be 2.")
    if report.get("status") not in {"pass", "fail", "error"}:
        errors.append("Report status must be pass, fail, or error.")
    if not isinstance(report.get("score"), (int, float)):
        errors.append("Report score must be numeric.")
    if not isinstance(report.get("routes"), list):
        errors.append("Report routes must be an array.")
    if not isinstance(report.get("findings"), list):
        errors.append("Report findings must be an array.")

    for index, finding_item in enumerate(report.get("findings", [])):
        prefix = f"Finding {index + 1}"
        if not isinstance(finding_item, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        for key in ["severity", "message", "estd"]:
            if key not in finding_item:
                errors.append(f"{prefix} missing required field: {key}")
        estd = finding_item.get("estd")
        if not isinstance(estd, dict):
            errors.append(f"{prefix} estd must be an object.")
            continue
        doc_id = estd.get("docId", "")
        section = estd.get("section", "")
        if not re.fullmatch(r"ESTD[0-9]+", str(doc_id)):
            errors.append(f"{prefix} has invalid ESTD docId: {doc_id}")
            continue
        doc_path = doc_path_for(str(doc_id))
        if doc_path is None:
            errors.append(f"{prefix} cites unknown ESTD doc: {doc_id}")
            continue
        if not str(section).strip():
            errors.append(f"{prefix} must cite an exact ESTD section.")
            continue
        if not section_exists(doc_path, str(section)):
            errors.append(f"{prefix} cites missing section {doc_id} {section}.")

    return errors


def report_has_unknown_evidence(report: dict[str, Any]) -> bool:
    if report.get("unknownEvidence") is True:
        return True
    for route in report.get("routes", []):
        if isinstance(route, dict) and route.get("unknownEvidence") is True:
            return True
    for finding_item in report.get("findings", []):
        if isinstance(finding_item, dict) and str(finding_item.get("evidenceStatus", "")).lower() == "unknown":
            return True
    return False


def count_critical_blockers(report: dict[str, Any]) -> int:
    explicit = report.get("criticalBlockers")
    if isinstance(explicit, int):
        return explicit
    count = 0
    for finding_item in report.get("findings", []):
        if not isinstance(finding_item, dict):
            continue
        severity = str(finding_item.get("severity", "")).lower()
        status = str(finding_item.get("status", "open")).lower()
        if severity == "critical" and status != "resolved":
            count += 1
    return count


def merge_reports(
    routes: list[str],
    static_report: dict[str, Any],
    llm_report: dict[str, Any] | None,
    groups: list[dict[str, Any]],
    llm_invoked: bool,
) -> dict[str, Any]:
    static_findings = static_report.get("findings", [])
    llm_findings = llm_report.get("findings", []) if llm_report else []
    static_score = float(static_report.get("score", 0))
    llm_score = float(llm_report.get("score", 100)) if llm_report else 100
    score = min(static_score, llm_score)
    static_failed = static_report.get("status") in {"fail", "error"}
    llm_failed = bool(llm_report and llm_report.get("status") in {"fail", "error"})
    status = "fail" if static_failed or llm_failed else "pass"
    all_findings = [*static_findings, *llm_findings]
    critical_count = sum(
        1
        for item in all_findings
        if str(item.get("severity", "")).lower() == "critical"
        and str(item.get("status", "open")).lower() != "resolved"
    )
    unknown = bool(llm_report and report_has_unknown_evidence(llm_report))
    route_results = []
    for route_id in routes:
        route_results.append(
            {
                "routeId": route_id,
                "validatorId": validator_id_for(route_id),
                "score": score,
                "status": status,
                "unknownEvidence": unknown,
            }
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "tool": "estd-enforcer",
        "status": status,
        "score": score,
        "criticalBlockers": critical_count,
        "unknownEvidence": unknown,
        "llmInvoked": llm_invoked,
        "routes": route_results,
        "validatorGroups": groups,
        "staticResults": static_report.get("results", []),
        "llmResults": llm_report or {
            "invoked": False,
            "status": "not-invoked",
            "findings": [],
            "toolErrors": [],
        },
        "findings": all_findings,
        "exceptions": (llm_report or {}).get("exceptions", []),
        "toolErrors": [
            *static_report.get("toolErrors", []),
            *((llm_report or {}).get("toolErrors", [])),
        ],
    }


def render_markdown(report: dict[str, Any], gate_failures: list[str], tool_errors: list[str]) -> str:
    lines = [
        "# ESTD Standards Gate Report",
        "",
        f"- Status: {report.get('status', 'unknown')}",
        f"- Score: {report.get('score', 'unknown')}",
        f"- LLM invoked: {report.get('llmInvoked', False)}",
        f"- Critical blockers: {count_critical_blockers(report)}",
        f"- Unknown evidence: {report_has_unknown_evidence(report)}",
    ]
    if report.get("notApplicableReason"):
        lines.append(f"- Not applicable: {report.get('notApplicableReason')}")
    lines.extend(["", "## Gate Failures"])
    lines.extend([f"- {failure}" for failure in gate_failures] or ["- none"])
    lines.extend(["", "## Tool Errors"])
    lines.extend([f"- {error}" for error in tool_errors] or ["- none"])
    lines.extend(["", "## Static Results"])
    for result in report.get("staticResults", []):
        lines.append(f"- {result.get('checkId')}: {result.get('status')} - {result.get('message')}")
    if not report.get("staticResults"):
        lines.append("- none")
    lines.extend(["", "## Validator Groups"])
    for group in report.get("validatorGroups", []):
        lines.append(
            f"- {group.get('routeId')} / {group.get('group')}: "
            f"{group.get('coverageSource')} / {group.get('status')}"
        )
    if not report.get("validatorGroups"):
        lines.append("- none")
    lines.extend(["", "## Findings"])
    findings = report.get("findings", [])
    if not findings:
        lines.append("- none")
    for finding_item in findings:
        if not isinstance(finding_item, dict):
            continue
        estd = finding_item.get("estd", {}) if isinstance(finding_item.get("estd"), dict) else {}
        location = finding_item.get("file", "")
        line = finding_item.get("line", 0)
        suffix = f" ({location}:{line})" if location else ""
        lines.append(
            f"- [{finding_item.get('severity', 'unknown')}] {estd.get('docId', 'ESTD?')} "
            f"{estd.get('section', '?')}: {finding_item.get('message', '')}{suffix}"
        )
    lines.append("")
    return "\n".join(lines)


def not_applicable_report(repo: Path, standards_path: str) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "tool": "estd-enforcer",
        "status": "pass",
        "score": 100,
        "criticalBlockers": 0,
        "unknownEvidence": False,
        "llmInvoked": False,
        "notApplicableReason": f"ESTD standards submodule is not configured at {standards_path}.",
        "repo": str(repo),
        "routes": [],
        "validatorGroups": [],
        "staticResults": [],
        "llmResults": {
            "invoked": False,
            "status": "not-applicable",
            "findings": [],
            "toolErrors": [],
        },
        "findings": [],
        "exceptions": [],
        "toolErrors": [],
    }


def error_report(
    message: str,
    static_report: dict[str, Any] | None = None,
    groups: list[dict[str, Any]] | None = None,
    details: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "tool": "estd-enforcer",
        "status": "error",
        "score": 0,
        "criticalBlockers": 0,
        "unknownEvidence": True,
        "llmInvoked": False,
        "routes": [],
        "validatorGroups": groups or [],
        "staticResults": (static_report or {}).get("results", []),
        "llmResults": {
            "invoked": False,
            "status": "error",
            "findings": [],
            "toolErrors": [message],
        },
        "findings": [
            finding(
                "ESTD-TOOL-ERROR",
                "critical",
                "route.common",
                "ESTD1",
                "30",
                "Enforcement and Exceptions",
                "docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md",
                "",
                0,
                message,
                "Fix the enforcer configuration, static adapter, or LLM adapter and rerun the gate.",
            )
        ],
        "exceptions": [],
        "toolErrors": details or [message],
    }
