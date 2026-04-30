"""Command-line interface for Confluence docs deployment."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .models import ConfluenceDeployError, DEFAULT_CLOUD, DEFAULT_SPACE_KEY
from .publisher import run_sync


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="deploy_docs_to_confluence")
    parser.add_argument("--workspace", default=os.getenv("GITHUB_WORKSPACE", ""))
    parser.add_argument("--cloud", default=DEFAULT_CLOUD)
    parser.add_argument("--space-key", default=DEFAULT_SPACE_KEY)
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    workspace = Path(args.workspace).resolve() if args.workspace else None
    user = os.getenv("CONF_USER", "")
    token = os.getenv("CONF_TOKEN", "")

    if not workspace:
        print("ERROR: GITHUB_WORKSPACE or --workspace is required", file=sys.stderr)
        return 1
    if not workspace.is_dir():
        print(f"ERROR: workspace does not exist: {workspace}", file=sys.stderr)
        return 1
    if not user:
        print("ERROR: CONF_USER is required", file=sys.stderr)
        return 1
    if not token:
        print("ERROR: CONF_TOKEN is required", file=sys.stderr)
        return 1

    try:
        run_sync(
            workspace=workspace,
            cloud=args.cloud,
            space_key=args.space_key,
            user=user,
            token=token,
            changed_files_env=os.getenv("CHANGED_FILES", ""),
        )
    except ConfluenceDeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0
