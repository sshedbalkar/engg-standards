#!/usr/bin/env python3

"""Purpose:
    Run the ESTD enforcer CLI entrypoint.

Usage:
    tools/estd-enforcer/lib/estd_enforce.py <command> [options]

Parameters:
    <command> [options]:
        Forwarded to estd_enforcer.cli.main.

Outputs:
    stdout:
        CLI command output.
    stderr:
        CLI errors.

Side Effects:
    Delegates all side effects to the selected CLI command.

Return Codes:
    0 - Success, advisory pass, or not applicable.
    1 - Standards gate failed.
    2 - Tool, config, dependency, schema, or adapter error.

Technical Approach:
    Keep this wrapper import-safe, delegate to the package CLI, and preserve
    argv handling for both direct execution and shell wrapper execution.

Examples:
    tools/estd-enforcer/lib/estd_enforce.py validate --repo .
"""

from __future__ import annotations

import sys

from estd_enforcer.cli import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
