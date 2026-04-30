"""Shared ESTD enforcer exceptions."""

from __future__ import annotations


class ToolError(Exception):
    """Configuration, retrieval, LLM, schema, or adapter failure."""
