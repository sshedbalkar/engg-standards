"""Route selection and validator group coverage."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .estd_refs import validator_id_for
from .constants import PROFILE_TO_ROUTE, ROUTE_ORDER, VALIDATORS_ROOT
from .errors import ToolError
from .standard_types import classify_path


def validator_path_for(route_id: str) -> Path | None:
    route_name = route_id.removeprefix("route.")
    candidate = VALIDATORS_ROOT / f"{route_name}-validator.md"
    return candidate if candidate.exists() else None


def select_routes(files: list[str], profile: str) -> list[str]:
    profile_key = profile.removeprefix("route.")
    if profile != "auto":
        forced = profile if profile.startswith("route.") else PROFILE_TO_ROUTE.get(profile_key)
        if not forced:
            raise ToolError(f"Unknown profile '{profile}'.")
        return [forced]

    selected: set[str] = set()
    for file_path in files:
        selected.update(classify_path(file_path))

    if not selected and files:
        selected.add("route.common")
    return [route for route in ROUTE_ORDER if route in selected]


def parse_static_coverage(validator_path: Path | None) -> list[dict[str, Any]]:
    if validator_path is None:
        return []
    content = validator_path.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, Any]] = []
    in_section = False
    for line in content:
        if line.strip() == "## Static Coverage":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] == "Group":
            continue
        static_ids = [
            item.strip().strip("`")
            for item in cells[1].split(",")
            if item.strip() and item.strip().lower() != "none"
        ]
        gap = cells[2]
        rows.append({"group": cells[0], "staticCheckIds": static_ids, "llmGap": gap})
    return rows


def build_validator_groups(routes: list[str], static_report: dict[str, Any]) -> list[dict[str, Any]]:
    static_results = {str(result["checkId"]): result for result in static_report.get("results", [])}
    groups: list[dict[str, Any]] = []
    for route_id in routes:
        validator_path = validator_path_for(route_id)
        coverage_rows = parse_static_coverage(validator_path)
        if not coverage_rows:
            groups.append(
                {
                    "routeId": route_id,
                    "validatorId": validator_id_for(route_id),
                    "group": "Unmapped validator coverage",
                    "coverageSource": "llm",
                    "staticCheckIds": [],
                    "llmGap": "No Static Coverage table is defined.",
                    "status": "unresolved",
                }
            )
            continue
        for row in coverage_rows:
            check_ids = row["staticCheckIds"]
            statuses = [static_results[check_id]["status"] for check_id in check_ids if check_id in static_results]
            has_static_failure = any(status in {"fail", "error"} for status in statuses)
            has_static_skip = any(status == "skipped" for status in statuses)
            has_llm_gap = row["llmGap"].lower() not in {"none", "no", "n/a", "not applicable"}
            if not check_ids:
                coverage_source = "llm"
            elif has_llm_gap or has_static_skip:
                coverage_source = "mixed"
            else:
                coverage_source = "static"
            if has_static_failure:
                status = "fail"
            elif coverage_source == "static":
                status = "pass"
            else:
                status = "unresolved"
            groups.append(
                {
                    "routeId": route_id,
                    "validatorId": validator_id_for(route_id),
                    "group": row["group"],
                    "coverageSource": coverage_source,
                    "staticCheckIds": check_ids,
                    "llmGap": row["llmGap"],
                    "status": status,
                }
            )
    return groups


def unresolved_groups(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [group for group in groups if group.get("status") == "unresolved"]
