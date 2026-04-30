"""LLM gap request construction and adapter execution."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any

from .estd_refs import doc_path_for, extract_validator_docs
from .constants import (
    REPORT_SCHEMA,
    ROUTE_MAP,
    SCHEMA_VERSION,
    STANDARDS_ROOT,
    VALIDATORS_ROOT,
)
from .errors import ToolError
from .routing import validator_path_for, unresolved_groups


def build_llm_request(
    repo: Path,
    base: str,
    config: dict[str, Any],
    files: list[str],
    routes: list[str],
    static_report: dict[str, Any],
    groups: list[dict[str, Any]],
) -> str:
    route_lines = []
    doc_ids: set[str] = set()
    for route_id in routes:
        validator_path = validator_path_for(route_id)
        validator_ref = validator_path.relative_to(STANDARDS_ROOT).as_posix() if validator_path else "none"
        route_docs = extract_validator_docs(validator_path)
        doc_ids.update(route_docs)
        docs_ref = ", ".join(route_docs) if route_docs else "route map only"
        route_lines.append(f"- {route_id}: validator={validator_ref}; docs={docs_ref}")

    doc_lines = []
    for doc_id in sorted(doc_ids, key=lambda item: int(item[4:])):
        doc_path = doc_path_for(doc_id)
        if doc_path:
            doc_lines.append(f"- {doc_id}: {doc_path.relative_to(STANDARDS_ROOT).as_posix()}")

    group_lines = [
        f"- {group['routeId']} / {group['group']}: {group['llmGap']}"
        for group in unresolved_groups(groups)
    ]
    static_finding_lines = [
        f"- {finding_item['id']}: {finding_item['message']}"
        for finding_item in static_report.get("findings", [])
    ]
    changed_lines = [f"- {file_path}" for file_path in files[:500]]
    if len(files) > 500:
        changed_lines.append(f"- ... {len(files) - 500} more files omitted from request preview")

    return "\n".join(
        [
            "# ESTD Enforcer LLM Gap Review Request",
            "",
            "## Contract",
            "- Static validators are authoritative for deterministic checks.",
            "- Do not override static failures or approved static passes.",
            "- Evaluate only unresolved validator groups listed below.",
            "- Retrieve exact ESTD sections from docs/ before emitting findings.",
            "- Output JSON only, conforming to tools/estd-enforcer/schema/report.schema.json.",
            "",
            "## Consumer Repo",
            f"- repo: {repo}",
            f"- base: {base}",
            f"- mode: {config['mode']}",
            f"- scope: {config['scope']}",
            f"- minScore: {config['minScore']}",
            f"- failOnCritical: {config['failOnCritical']}",
            "",
            "## Standards Inputs",
            f"- routing map: {ROUTE_MAP.relative_to(STANDARDS_ROOT).as_posix()}",
            f"- validator README: {(VALIDATORS_ROOT / 'README.md').relative_to(STANDARDS_ROOT).as_posix()}",
            f"- report schema: {REPORT_SCHEMA.relative_to(STANDARDS_ROOT).as_posix()}",
            "",
            "## Selected Routes",
            *(route_lines or ["- none"]),
            "",
            "## Source ESTD Docs To Retrieve",
            *(doc_lines or ["- none"]),
            "",
            "## Unresolved Validator Groups",
            *(group_lines or ["- none"]),
            "",
            "## Static Findings Already Authoritative",
            *(static_finding_lines or ["- none"]),
            "",
            "## Files In Scope",
            *(changed_lines or ["- none"]),
            "",
        ]
    )


def normalize_llm_report(report: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(report)
    if normalized.get("schemaVersion") == 1:
        normalized["schemaVersion"] = SCHEMA_VERSION
    normalized.setdefault("tool", "estd-enforcer-llm")
    normalized.setdefault("criticalBlockers", 0)
    normalized.setdefault("unknownEvidence", False)
    normalized.setdefault("routes", [])
    normalized.setdefault("findings", [])
    normalized.setdefault("exceptions", [])
    normalized.setdefault("toolErrors", [])
    normalized.setdefault("llmInvoked", True)
    return normalized


def run_llm(request: str, out_dir: Path, args: argparse.Namespace) -> dict[str, Any]:
    report_override = args.report or os.environ.get("ESTD_LLM_REPORT")
    if report_override:
        report_path = Path(report_override)
        if not report_path.exists():
            raise ToolError(f"Report override not found: {report_path}")
        return normalize_llm_report(json.loads(report_path.read_text(encoding="utf-8")))

    llm_command = args.llm_command or os.environ.get("ESTD_LLM_COMMAND")
    if not llm_command:
        raise ToolError("No LLM adapter configured. Set ESTD_LLM_COMMAND, provide --report, or resolve static gaps.")

    command = shlex.split(llm_command)
    result = subprocess.run(
        command,
        input=request,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(out_dir),
        check=False,
    )
    if result.returncode != 0:
        raise ToolError(f"LLM adapter failed with exit {result.returncode}: {result.stderr.strip()}")
    try:
        return normalize_llm_report(json.loads(result.stdout))
    except json.JSONDecodeError as exc:
        raise ToolError(f"LLM adapter did not return valid JSON: {exc}") from exc
