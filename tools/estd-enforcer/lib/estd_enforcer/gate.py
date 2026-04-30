"""Blocking gate evaluation rules."""

from __future__ import annotations

from typing import Any

from .reports import count_critical_blockers, report_has_unknown_evidence


def evaluate_gate(
    report: dict[str, Any],
    config: dict[str, Any],
    exception_errors: list[str],
    unresolved: list[dict[str, Any]],
) -> list[str]:
    failures: list[str] = []
    min_score = int(config["minScore"])
    score = float(report.get("score", 0))
    if report.get("status") == "error":
        failures.append("Report status is error.")
    if report.get("status") == "fail":
        failures.append("Report status is fail.")
    if score <= min_score:
        failures.append(f"Score {score:g} is not greater than minScore {min_score}.")
    if bool(config.get("failOnCritical", True)) and count_critical_blockers(report) > 0:
        failures.append("Critical blocker findings are present.")
    if unresolved and config["llmPolicy"] == "disabled":
        failures.append("LLM gaps remain but llmPolicy is disabled.")
    if report_has_unknown_evidence(report):
        failures.append("Unknown evidence is present.")
    failures.extend(exception_errors)
    return failures
