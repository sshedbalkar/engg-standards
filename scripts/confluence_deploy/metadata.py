"""Source and Confluence metadata preservation helpers."""

from __future__ import annotations

import hashlib
import html
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .markdown_renderer import parse_html
from .models import (
    ConfluenceDeployError,
    JsonObject,
    SYNC_METADATA_END,
    SYNC_METADATA_PROPERTY_KEY,
    SYNC_METADATA_SCHEMA_VERSION,
    SYNC_METADATA_START,
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_source_metadata(
    *,
    workspace: Path,
    source_path: str,
    file_path: Path,
    markdown_text: str,
) -> JsonObject:
    fields = extract_markdown_metadata_fields(markdown_text)
    git_first_seen_at = git_file_timestamp(
        workspace,
        source_path,
        first_seen=True,
    )
    git_last_modified_at = git_file_timestamp(
        workspace,
        source_path,
        first_seen=False,
    )
    return {
        "path": source_path,
        "title": extract_markdown_title(markdown_text),
        "fields": fields,
        "sha256": hashlib.sha256(file_path.read_bytes()).hexdigest(),
        "createdAt": select_source_created_at(fields, git_first_seen_at),
        "lastModifiedAt": select_source_modified_at(fields, git_last_modified_at),
        "gitFirstSeenAt": git_first_seen_at,
        "gitLastModifiedAt": git_last_modified_at,
    }


def extract_markdown_title(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return clean_markdown_cell(line[2:])
    return ""


def extract_markdown_metadata_fields(markdown_text: str) -> dict[str, str]:
    lines = markdown_text.splitlines()
    for index, line in enumerate(lines[:-1]):
        header = [clean_markdown_cell(cell) for cell in split_markdown_table_row(line)]
        if len(header) < 2 or [item.lower() for item in header[:2]] != ["field", "value"]:
            continue
        if not is_markdown_separator_row(lines[index + 1]):
            continue
        fields: dict[str, str] = {}
        for row in lines[index + 2:]:
            cells = split_markdown_table_row(row)
            if len(cells) < 2:
                break
            key = clean_markdown_cell(cells[0])
            value = clean_markdown_cell(cells[1])
            if key:
                fields[key] = value
        return fields
    return {}


def split_markdown_table_row(row: str) -> list[str]:
    stripped = row.strip()
    if not stripped.startswith("|"):
        return []
    stripped = stripped.strip("|")
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in stripped:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    cells.append("".join(current).strip())
    return cells


def is_markdown_separator_row(row: str) -> bool:
    cells = split_markdown_table_row(row)
    if len(cells) < 2:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells[:2])


def clean_markdown_cell(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"^#+\s*", "", cleaned)
    cleaned = re.sub(r"</?[^>]+>", "", cleaned)
    cleaned = re.sub(r"[*_`]+", "", cleaned)
    return html.unescape(cleaned).strip()


def select_source_created_at(fields: dict[str, str], git_first_seen_at: str) -> str:
    return metadata_field(fields, "Created") or git_first_seen_at


def select_source_modified_at(fields: dict[str, str], git_last_modified_at: str) -> str:
    return (
        metadata_field(fields, "Last Updated")
        or metadata_field(fields, "Last Modified")
        or git_last_modified_at
    )


def metadata_field(fields: dict[str, str], *names: str) -> str:
    normalized_names = {normalize_metadata_key(name) for name in names}
    for key, value in fields.items():
        if normalize_metadata_key(key) in normalized_names:
            return value
    return ""


def normalize_metadata_key(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).lower()


def git_file_timestamp(
    workspace: Path,
    source_path: str,
    *,
    first_seen: bool,
) -> str:
    args = ["git", "-C", str(workspace), "log"]
    if first_seen:
        args.extend(["--follow", "--format=%aI", "--reverse"])
    else:
        args.extend(["-1", "--format=%aI"])
    args.extend(["--", source_path])
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    if completed.returncode != 0:
        return ""
    return first_non_empty_line(completed.stdout)


def first_non_empty_line(value: str) -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def extract_page_metadata(page: JsonObject) -> JsonObject:
    version = page.get("version") or {}
    return {
        "id": str(page.get("id") or ""),
        "status": str(page.get("status") or ""),
        "title": str(page.get("title") or ""),
        "spaceId": str(page.get("spaceId") or ""),
        "parentId": str(page.get("parentId") or ""),
        "authorId": str(page.get("authorId") or ""),
        "ownerId": str(page.get("ownerId") or ""),
        "lastOwnerId": str(page.get("lastOwnerId") or ""),
        "createdAt": str(page.get("createdAt") or ""),
        "versionNumber": int_or_none(version.get("number")),
        "versionCreatedAt": str(version.get("createdAt") or ""),
        "versionAuthorId": str(version.get("authorId") or ""),
        "versionMessage": str(version.get("message") or ""),
    }


def int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def expected_page_metadata_after_update(
    before_metadata: JsonObject,
    current_page: JsonObject,
    sync_timestamp: str,
) -> JsonObject:
    expected = dict(before_metadata)
    expected["versionNumber"] = current_page["version"]["number"] + 1
    expected["versionCreatedAt"] = sync_timestamp
    expected["versionMessage"] = "Automated ESTD docs sync"
    return expected


def build_document_metadata_payload(
    source_metadata: JsonObject,
    before_metadata: JsonObject,
    after_metadata: JsonObject,
    sync_timestamp: str,
) -> JsonObject:
    return {
        "schemaVersion": SYNC_METADATA_SCHEMA_VERSION,
        "source": source_metadata,
        "confluenceBeforeSync": before_metadata,
        "confluenceAfterSync": after_metadata,
        "sync": {
            "syncedAt": sync_timestamp,
            "tool": "scripts/deploy_docs_to_confluence.py",
            "propertyKey": SYNC_METADATA_PROPERTY_KEY,
        },
    }


def build_page_property_payload(
    key: str,
    value: JsonObject,
    existing: JsonObject | None,
) -> JsonObject:
    payload = {"key": key, "value": value}
    if existing:
        version = existing.get("version") or {}
        payload["version"] = {
            "number": int(version.get("number") or 0) + 1,
            "message": "Automated ESTD metadata sync",
        }
    return payload


def inject_sync_metadata_block(storage_html: str, metadata: JsonObject) -> str:
    cleaned_html = remove_sync_metadata_block(storage_html)
    block = build_visible_sync_metadata_block(metadata)
    soup = parse_html(cleaned_html)
    container = soup.body or soup
    container.append(parse_html(block))
    return str(soup)


def remove_sync_metadata_block(storage_html: str) -> str:
    pattern = re.compile(
        rf"{re.escape(SYNC_METADATA_START)}.*?{re.escape(SYNC_METADATA_END)}",
        re.DOTALL,
    )
    return pattern.sub("", storage_html)


def build_visible_sync_metadata_block(metadata: JsonObject) -> str:
    source = metadata.get("source") or {}
    before = metadata.get("confluenceBeforeSync") or {}
    after = metadata.get("confluenceAfterSync") or {}
    sync = metadata.get("sync") or {}
    rows = [
        ("Source path", str(source.get("path") or "")),
        ("Source created at", str(source.get("createdAt") or "")),
        ("Source last modified at", str(source.get("lastModifiedAt") or "")),
        ("Source SHA-256", str(source.get("sha256") or "")),
        ("Confluence page created at", str(before.get("createdAt") or "")),
        ("Previous Confluence version", str(before.get("versionNumber") or "")),
        ("Current Confluence version", str(after.get("versionNumber") or "")),
        ("Sync timestamp", str(sync.get("syncedAt") or "")),
    ]
    return (
        SYNC_METADATA_START
        + "\n"
        "<p><strong>ESTD sync metadata</strong></p>"
        "<table><tbody>"
        + "".join(table_row(label, value) for label, value in rows)
        + "</tbody></table>"
        + "\n"
        + SYNC_METADATA_END
    )


def table_row(label: str, value: str) -> str:
    return (
        "<tr>"
        f"<th>{html.escape(label)}</th>"
        f"<td>{html.escape(value or '(empty)')}</td>"
        "</tr>"
    )


def verify_metadata_property(
    client: Any,
    page_id: str,
    expected_metadata: JsonObject,
) -> None:
    property_model = client.get_page_property(page_id, SYNC_METADATA_PROPERTY_KEY)
    if not property_model:
        raise ConfluenceDeployError(
            f"Confluence page {page_id} is missing {SYNC_METADATA_PROPERTY_KEY}"
        )
    value = property_model.get("value")
    prop_id = str(property_model.get("id") or "")
    if not isinstance(value, dict) and prop_id:
        property_model = client.get_page_property_by_id(page_id, prop_id)
        value = property_model.get("value")
    if not isinstance(value, dict):
        raise ConfluenceDeployError(
            f"Confluence page {page_id} metadata property has no JSON value"
        )
    expected_sync = (expected_metadata.get("sync") or {}).get("syncedAt")
    actual_sync = (value.get("sync") or {}).get("syncedAt")
    expected_hash = (expected_metadata.get("source") or {}).get("sha256")
    actual_hash = (value.get("source") or {}).get("sha256")
    if actual_sync != expected_sync or actual_hash != expected_hash:
        raise ConfluenceDeployError(
            f"Confluence page {page_id} metadata property verification failed"
        )
