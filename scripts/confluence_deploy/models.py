"""Shared models and constants for Confluence docs deployment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ARCHIVE_KEY_PREFIX = "ESTD-CONFLUENCE-INLINE-COMMENT-ARCHIVE"
DEFAULT_CLOUD = "scopely"
DEFAULT_SPACE_KEY = "BB"
MAX_API_ERROR_CHARS = 1200
MAX_PAGINATION_PAGES = 200
SYNC_METADATA_END = "<!-- ESTD_SYNC_METADATA_END -->"
SYNC_METADATA_PROPERTY_KEY = "estd.documentMetadata"
SYNC_METADATA_SCHEMA_VERSION = 1
SYNC_METADATA_START = "<!-- ESTD_SYNC_METADATA_START -->"

JsonObject = dict[str, Any]


class ConfluenceDeployError(Exception):
    """Expected failure while preparing or publishing Confluence content."""


@dataclass(frozen=True)
class ConfluenceRow:
    content_type: str
    page_to: str
    path: str


@dataclass(frozen=True)
class InlineMarker:
    ref: str
    inner_html: str
    full_html: str


@dataclass(frozen=True)
class InlineComment:
    id: str
    marker_ref: str
    original_selection: str
    body_storage: str
    author_id: str
    created_at: str
    resolution_status: str
    webui: str
    children: tuple["InlineComment", ...] = ()


@dataclass(frozen=True)
class InlinePreservationResult:
    html: str
    preserved: tuple[InlineComment, ...]
    to_archive: tuple[InlineComment, ...]


def extract_storage_value(data: JsonObject) -> str:
    storage = (data.get("body") or {}).get("storage") or {}
    if isinstance(storage, dict):
        return str(storage.get("value") or "")
    return ""

