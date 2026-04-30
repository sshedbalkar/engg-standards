"""Console output helpers for Confluence deployment."""

from __future__ import annotations

import sys


def warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)
