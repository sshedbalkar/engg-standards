"""Static check registry and command adapter execution."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .constants import SCHEMA_VERSION, STATIC_REGISTRY_PATH
from .errors import ToolError
from .models import finding, static_result
from .standard_types.common import run_builtin_check


def load_static_registry() -> dict[str, dict[str, Any]]:
    if not STATIC_REGISTRY_PATH.exists():
        raise ToolError(f"Static check registry missing: {STATIC_REGISTRY_PATH}")
    data = json.loads(STATIC_REGISTRY_PATH.read_text(encoding="utf-8"))
    checks = data.get("checks", [])
    if not isinstance(checks, list):
        raise ToolError("Static check registry must contain a checks array.")
    return {str(check["id"]): check for check in checks}


def registry_checks_for_routes(
    registry: dict[str, dict[str, Any]],
    routes: list[str],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for check in registry.values():
        check_routes = set(check.get("routes", []))
        if "route.common" in check_routes or check_routes.intersection(routes):
            selected.append(check)
    return selected


def has_any_file(repo: Path, patterns: list[str]) -> bool:
    for pattern in patterns:
        if list(repo.glob(pattern)):
            return True
    return False


def command_available(repo: Path, command_spec: dict[str, Any]) -> bool:
    local_path = command_spec.get("localPath")
    if local_path and (repo / str(local_path)).exists():
        return True
    executable = command_spec.get("executable")
    return bool(executable and shutil.which(str(executable)))


def command_is_applicable(repo: Path, files: list[str], command_spec: dict[str, Any]) -> bool:
    file_patterns = command_spec.get("filePatterns", [])
    if file_patterns and has_any_file(repo, [str(pattern) for pattern in file_patterns]):
        return True
    suffixes = tuple(str(item) for item in command_spec.get("fileSuffixes", []))
    return bool(suffixes and any(file_path.endswith(suffixes) for file_path in files))


def resolve_command(repo: Path, command_spec: dict[str, Any]) -> list[str]:
    local_path = command_spec.get("localPath")
    if local_path and (repo / str(local_path)).exists():
        return [str(repo / str(local_path)), *[str(arg) for arg in command_spec.get("args", [])]]
    executable = str(command_spec.get("executable", ""))
    return [executable, *[str(arg) for arg in command_spec.get("args", [])]]


def run_command_check(
    check: dict[str, Any],
    repo: Path,
    files: list[str],
    required_checks: set[str],
) -> tuple[dict[str, Any], str | None]:
    check_id = str(check["id"])
    command_spec = check.get("command", {})
    route_id = str(check.get("primaryRoute", "route.common"))
    if not command_is_applicable(repo, files, command_spec):
        return static_result(check_id, "not-applicable", "No matching files for command adapter.", route_id), None
    if not command_available(repo, command_spec):
        message = (
            "Required static tool is unavailable."
            if check_id in required_checks
            else "Optional static tool is unavailable; LLM gap remains."
        )
        status = "error" if check_id in required_checks else "skipped"
        return static_result(check_id, status, message, route_id), message if check_id in required_checks else None

    command = resolve_command(repo, command_spec)
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(repo),
        check=False,
        timeout=int(command_spec.get("timeoutSeconds", 120)),
    )
    if result.returncode == 0:
        return static_result(
            check_id,
            "pass",
            "Command static check passed.",
            route_id,
            command=" ".join(command),
        ), None

    doc = check.get("estd", {})
    static_finding = finding(
        "ESTD-" + check_id.upper().replace(".", "-"),
        str(check.get("severity", "high")),
        route_id,
        str(doc.get("docId", "ESTD1")),
        str(doc.get("section", "30")),
        str(doc.get("title", "Enforcement and Exceptions")),
        str(doc.get("path", "docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md")),
        "",
        0,
        f"Static command failed: {' '.join(command)}",
        (result.stderr.strip() or result.stdout.strip() or "Fix the static tool findings and rerun the gate.")[:1000],
    )
    return static_result(
        check_id,
        "fail",
        "Command static check failed.",
        route_id,
        str(check.get("severity", "high")),
        [static_finding],
        " ".join(command),
    ), None


def run_static_checks(
    repo: Path,
    config: dict[str, Any],
    files: list[str],
    routes: list[str],
) -> tuple[dict[str, Any], list[str]]:
    registry = load_static_registry()
    required_checks = set(str(item) for item in config.get("requiredStaticTools", []))
    selected_checks = registry_checks_for_routes(registry, routes)
    results: list[dict[str, Any]] = []
    tool_errors: list[str] = []

    for check in selected_checks:
        check_id = str(check["id"])
        if check.get("kind") == "built-in":
            results.append(run_builtin_check(check_id, repo, config, files, routes))
        else:
            result, error = run_command_check(check, repo, files, required_checks)
            results.append(result)
            if error:
                tool_errors.append(f"{check_id}: {error}")

    for required_check in sorted(required_checks):
        if required_check not in registry:
            tool_errors.append(f"{required_check}: required static check is not registered.")
        elif required_check not in {str(result["checkId"]) for result in results}:
            tool_errors.append(f"{required_check}: required static check did not run for selected routes.")

    findings = [item for result in results for item in result.get("findings", [])]
    failing = [result for result in results if result.get("status") == "fail"]
    errors = [result for result in results if result.get("status") == "error"]
    applicable = [result for result in results if result.get("status") not in {"not-applicable", "skipped"}]
    passed = [result for result in applicable if result.get("status") == "pass"]
    static_score = 100 if not applicable else round(len(passed) / len(applicable) * 100, 2)
    status = "error" if errors or tool_errors else ("fail" if failing else "pass")
    report = {
        "schemaVersion": SCHEMA_VERSION,
        "tool": "estd-enforcer-static",
        "status": status,
        "score": static_score,
        "routes": routes,
        "files": files,
        "results": results,
        "findings": findings,
        "toolErrors": tool_errors,
    }
    return report, tool_errors
