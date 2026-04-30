"""ESTD enforcer command-line orchestration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .config import is_submodule_opted_in, load_config
from .constants import EXIT_GATE_FAILED, EXIT_PASS, EXIT_TOOL_ERROR
from .errors import ToolError
from .exceptions import validate_exceptions
from .gate import evaluate_gate
from .git_scope import changed_files, list_repo_files
from .llm import build_llm_request, run_llm
from .reports import (
    error_report,
    merge_reports,
    not_applicable_report,
    render_markdown,
    validate_report_shape,
    write_json,
)
from .routing import build_validator_groups, select_routes, unresolved_groups
from .static_runner import run_static_checks


def validate_command(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    if not repo.exists():
        raise ToolError(f"Repo path not found: {repo}")
    config = load_config(repo, Path(args.config))
    if args.scope:
        config["scope"] = args.scope
    if args.mode:
        config["mode"] = args.mode
    if args.profile:
        config["profile"] = args.profile
    if args.llm_policy:
        config["llmPolicy"] = args.llm_policy

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not is_submodule_opted_in(repo, config):
        report = not_applicable_report(repo, str(config["standardsPath"]))
        write_json(out_dir / "report.json", report)
        (out_dir / "report.md").write_text(render_markdown(report, [], []), encoding="utf-8")
        return EXIT_PASS

    files = (
        list_repo_files(repo, str(config["standardsPath"]))
        if config["scope"] == "full-repo"
        else changed_files(repo, args.base, str(config["standardsPath"]))
    )
    routes = select_routes(files, str(config["profile"]))
    static_report, static_tool_errors = run_static_checks(repo, config, files, routes)
    write_json(out_dir / "static-report.json", static_report)

    groups = build_validator_groups(routes, static_report)
    unresolved = unresolved_groups(groups)
    tool_errors: list[str] = list(static_tool_errors)
    llm_report: dict[str, Any] | None = None
    llm_invoked = False

    if static_tool_errors:
        report = error_report("Required static validation failed to run.", static_report, groups, static_tool_errors)
        write_json(out_dir / "report.json", report)
        (out_dir / "report.md").write_text(render_markdown(report, [], tool_errors), encoding="utf-8")
        return EXIT_TOOL_ERROR

    if unresolved and config["llmPolicy"] == "gaps-only":
        llm_request = build_llm_request(repo, args.base, config, files, routes, static_report, groups)
        (out_dir / "llm-request.md").write_text(llm_request, encoding="utf-8")
        try:
            llm_report = run_llm(llm_request, out_dir, args)
            llm_invoked = True
            write_json(out_dir / "llm-report.json", llm_report)
        except (ToolError, json.JSONDecodeError) as exc:
            report = error_report(str(exc), static_report, groups)
            write_json(out_dir / "report.json", report)
            (out_dir / "report.md").write_text(render_markdown(report, [], [str(exc)]), encoding="utf-8")
            return EXIT_TOOL_ERROR

    report = merge_reports(routes, static_report, llm_report, groups, llm_invoked)
    exception_errors = validate_exceptions(repo, config)
    shape_errors = validate_report_shape(report)
    gate_failures: list[str] = []
    if shape_errors:
        tool_errors.extend(shape_errors)
    else:
        gate_failures = evaluate_gate(report, config, exception_errors, unresolved if not llm_invoked else [])

    write_json(out_dir / "report.json", report)
    (out_dir / "report.md").write_text(render_markdown(report, gate_failures, tool_errors), encoding="utf-8")

    if tool_errors:
        return EXIT_TOOL_ERROR
    if gate_failures and config["mode"] == "blocking":
        return EXIT_GATE_FAILED
    return EXIT_PASS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="estd-enforce")
    parser.add_argument("--version", action="version", version="estd-enforcer 2")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Run the ESTD standards gate")
    validate.add_argument("--repo", default=".", help="Consumer repository root")
    validate.add_argument("--base", default="origin/main", help="Base ref for changed-file scope")
    validate.add_argument("--config", default=".estd/config.yaml", help="Consumer config file")
    validate.add_argument("--out", default="build/estd", help="Output directory")
    validate.add_argument("--scope", choices=["changed-files", "full-repo"], help="Override config scope")
    validate.add_argument("--mode", choices=["blocking", "advisory"], help="Override config mode")
    validate.add_argument("--profile", help="Override config profile")
    validate.add_argument("--llm-policy", choices=["gaps-only", "disabled"], help="Override config LLM policy")
    validate.add_argument(
        "--llm-command",
        help="LLM adapter command. Reads request markdown on stdin and writes report JSON on stdout.",
    )
    validate.add_argument("--report", help="Precomputed LLM report JSON for schema/gate validation")
    validate.set_defaults(func=validate_command)
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ToolError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_TOOL_ERROR
