"""Common built-in deterministic checks."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from estd_enforcer.models import finding, static_result
from estd_enforcer.routing import validator_path_for


def is_text_file(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\0" not in chunk


def run_builtin_check(
    check_id: str,
    repo: Path,
    config: dict[str, Any],
    files: list[str],
    routes: list[str],
) -> dict[str, Any]:
    if check_id == "static.common.config":
        return static_result(check_id, "pass", "Config contract is parseable.", "route.common")

    if check_id == "static.common.route-coverage":
        missing = [route for route in routes if validator_path_for(route) is None]
        if not missing:
            return static_result(check_id, "pass", "All selected routes have validator specs.", "route.common")
        findings = [
            finding(
                "ESTD-STATIC-ROUTE-COVERAGE",
                "critical",
                "route.common",
                "ESTD1",
                "30",
                "Enforcement and Exceptions",
                "docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md",
                "",
                0,
                "Selected routes are missing validator specs: " + ", ".join(missing),
                "Add route-bound validator specs before enabling the gate.",
            )
        ]
        return static_result(check_id, "fail", "Route coverage is incomplete.", "route.common", "critical", findings)

    if check_id == "static.common.folder-structure":
        bad_prefixes = ("build/", "node_modules/", ".next/", "Library/", "Temp/")
        findings = []
        for file_path in files:
            if file_path.startswith(bad_prefixes):
                findings.append(
                    finding(
                        "ESTD-STATIC-FOLDER-STRUCTURE",
                        "medium",
                        "route.common",
                        "ESTD18",
                        "2.1",
                        "Separation of Concerns at the Folder Level",
                        "docs/ESTD18_-_Codebase_Folder_Structure_Standards.md",
                        file_path,
                        1,
                        "Generated or dependency output is in the validation scope.",
                        "Exclude generated outputs and dependency folders from source-controlled changes.",
                    )
                )
        status = "fail" if findings else "pass"
        return static_result(
            check_id,
            status,
            "Folder structure static scan completed.",
            "route.common",
            "medium",
            findings,
        )

    if check_id == "static.common.secrets":
        secret_patterns = [
            re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
            re.compile(
                r"(?i)\b(aws_secret_access_key|secret_access_key|api[_-]?key|client[_-]?secret)\b"
                r"\s*[:=]\s*['\"]?[A-Za-z0-9/+=_-]{16,}"
            ),
            re.compile(r"(?i)\b(password|passwd|pwd)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
        ]
        findings = []
        standards_prefix = str(config["standardsPath"]).strip("/") + "/"
        for file_path in files:
            if file_path.startswith(standards_prefix):
                continue
            full_path = repo / file_path
            if not full_path.exists() or not full_path.is_file() or not is_text_file(full_path):
                continue
            try:
                lines = full_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for line_number, line in enumerate(lines, 1):
                if any(pattern.search(line) for pattern in secret_patterns):
                    findings.append(
                        finding(
                            "ESTD-STATIC-SECRET",
                            "critical",
                            "route.common",
                            "ESTD1",
                            "19",
                            "Secrets Management",
                            "docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md",
                            file_path,
                            line_number,
                            "Potential secret or credential material found in source.",
                            "Remove the secret, rotate it if real, and use the approved secrets store.",
                        )
                    )
        status = "fail" if findings else "pass"
        return static_result(check_id, status, "Secret scan completed.", "route.common", "critical", findings)

    if check_id == "static.common.report-consistency":
        return static_result(check_id, "pass", "Report consistency is enforced during merge.", "route.common")

    return static_result(check_id, "not-applicable", "Built-in check is not implemented.", "route.common")
