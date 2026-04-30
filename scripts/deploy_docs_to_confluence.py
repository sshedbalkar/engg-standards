#!/usr/bin/env python3
"""Purpose:
    Publish ESTD markdown files to Confluence while preserving inline comments
    and document metadata.

Usage:
    python3 scripts/deploy_docs_to_confluence.py [--workspace PATH]

Parameters:
    --workspace:
        Repository workspace. Defaults to GITHUB_WORKSPACE.
    --cloud:
        Atlassian cloud site name. Defaults to scopely.
    --space-key:
        Confluence space key. Defaults to BB.

Environment:
    CONF_USER:
        Atlassian username used by the deploy workflow.
    CONF_TOKEN:
        Atlassian API token used by the deploy workflow.
    CHANGED_FILES:
        Comma-separated changed file list. Empty means publish all.
    GITHUB_WORKSPACE:
        Default workspace path.

Outputs:
    stdout:
        Publish, skip, and archive status.
    stderr:
        Validation and adapter errors.

Side Effects:
    Reads local markdown files, updates Confluence pages, uploads attachments,
    updates page metadata properties, and creates footer archive comments when
    inline comments cannot be reattached.

Return Codes:
    0 - Success.
    1 - Validation failure.
    2 - Dependency, Confluence API, or adapter failure.

Technical Approach:
    Delegates to the modular scripts.confluence_deploy package. The package
    renders Markdown to Confluence storage HTML, preserves inline comments,
    writes source/Confluence metadata, and verifies important writes.

Examples:
    GITHUB_WORKSPACE="$PWD" CONF_USER=user CONF_TOKEN=token \
        python3 scripts/deploy_docs_to_confluence.py
"""

from __future__ import annotations

import sys

try:
    from confluence_deploy.cli import main
except ModuleNotFoundError:
    from scripts.confluence_deploy.cli import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
