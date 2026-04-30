"""Confluence inline comment preservation and archive helpers."""

from __future__ import annotations

import hashlib
import html
import re
from dataclasses import replace
from typing import Any

from .models import (
    ARCHIVE_KEY_PREFIX,
    InlineComment,
    InlineMarker,
    InlinePreservationResult,
    JsonObject,
    extract_storage_value,
)


def api_comment_to_inline_comment(data: JsonObject) -> InlineComment:
    properties = data.get("properties") or {}
    version = data.get("version") or {}
    links = data.get("_links") or {}
    return InlineComment(
        id=str(data.get("id") or ""),
        marker_ref=str(properties.get("inlineMarkerRef") or ""),
        original_selection=str(properties.get("inlineOriginalSelection") or ""),
        body_storage=extract_storage_value(data),
        author_id=str(version.get("authorId") or data.get("authorId") or ""),
        created_at=str(version.get("createdAt") or data.get("createdAt") or ""),
        resolution_status=str(data.get("resolutionStatus") or ""),
        webui=str(links.get("webui") or ""),
    )


def extract_inline_markers(storage_html: str) -> dict[str, InlineMarker]:
    markers: dict[str, InlineMarker] = {}
    pattern = re.compile(
        r"<ac:inline-comment-marker\b(?P<attrs>[^>]*)>"
        r"(?P<body>.*?)"
        r"</ac:inline-comment-marker>",
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(storage_html):
        ref = extract_marker_ref(match.group("attrs"))
        if not ref:
            continue
        markers[ref] = InlineMarker(
            ref=ref,
            inner_html=match.group("body"),
            full_html=match.group(0),
        )
    return markers


def extract_marker_ref(attributes: str) -> str:
    match = re.search(r'\bac:ref\s*=\s*["\']([^"\']+)["\']', attributes)
    return html.unescape(match.group(1)) if match else ""


def extract_marker_refs(storage_html: str) -> set[str]:
    return set(extract_inline_markers(storage_html).keys())


def apply_inline_comment_markers(
    generated_html: str,
    current_storage_html: str,
    comments: list[InlineComment],
) -> InlinePreservationResult:
    existing_markers = extract_inline_markers(current_storage_html)
    preserved: list[InlineComment] = []
    to_archive: list[InlineComment] = []
    output_html = generated_html

    for comment in sorted(comments, key=lambda item: (item.marker_ref, item.id)):
        if not comment.marker_ref:
            to_archive.append(comment)
            continue
        if comment.marker_ref in extract_marker_refs(output_html):
            preserved.append(comment)
            continue

        marker = existing_markers.get(comment.marker_ref)
        targets = []
        if marker and marker.inner_html:
            targets.append(marker.inner_html)
        targets.extend(selection_candidates(comment.original_selection))

        updated_html, inserted = insert_first_unique_marker(
            output_html,
            comment.marker_ref,
            targets,
        )
        if inserted:
            output_html = updated_html
            preserved.append(comment)
        else:
            to_archive.append(comment)

    return InlinePreservationResult(
        html=output_html,
        preserved=tuple(preserved),
        to_archive=tuple(to_archive),
    )


def selection_candidates(selection: str) -> list[str]:
    stripped = selection.strip()
    if not stripped:
        return []

    collapsed = re.sub(r"\s+", " ", stripped)
    candidates = [
        stripped,
        html.escape(stripped, quote=False),
        collapsed,
        html.escape(collapsed, quote=False),
    ]
    unique_candidates: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in unique_candidates:
            unique_candidates.append(candidate)
    return unique_candidates


def insert_first_unique_marker(
    storage_html: str,
    marker_ref: str,
    targets: list[str],
) -> tuple[str, bool]:
    for target in targets:
        if storage_html.count(target) != 1:
            continue
        wrapped = (
            f'<ac:inline-comment-marker ac:ref="{html.escape(marker_ref, quote=True)}">'
            f"{target}"
            "</ac:inline-comment-marker>"
        )
        return storage_html.replace(target, wrapped, 1), True
    return storage_html, False


def build_archive_key(page_id: str, comment: InlineComment) -> str:
    material = "\0".join([str(page_id), comment.id, comment.marker_ref])
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"{ARCHIVE_KEY_PREFIX}:{digest}"


def extract_archive_keys_from_footer_comments(
    footer_comments: list[JsonObject],
) -> set[str]:
    keys: set[str] = set()
    pattern = re.compile(rf"{re.escape(ARCHIVE_KEY_PREFIX)}:[a-f0-9]{{64}}")
    for comment in footer_comments:
        body = extract_storage_value(comment)
        keys.update(pattern.findall(body))
    return keys


def build_archive_footer_body(
    page_id: str,
    comment: InlineComment,
    author_names: dict[str, str],
) -> str:
    archive_key = build_archive_key(page_id, comment)
    selected_text = comment.original_selection or marker_text_fallback(comment)
    parts = [
        "<p><strong>ESTD archived inline comment</strong></p>",
        f"<p><strong>Archive key:</strong> <code>{html.escape(archive_key)}</code></p>",
        "<p><strong>Reason:</strong> The original inline selection was changed, "
        "deleted, or not unique during automated markdown sync.</p>",
        "<table>",
        "<tbody>",
        table_row("Original comment ID", comment.id),
        table_row("Original marker ref", comment.marker_ref),
        table_row("Original author", format_author(comment.author_id, author_names)),
        table_row("Original created at", comment.created_at),
        table_row("Resolution status", comment.resolution_status or "unknown"),
        table_row("Original web URL", comment.webui),
        "</tbody>",
        "</table>",
        "<p><strong>Original selected text</strong></p>",
        f"<blockquote><p>{html.escape(selected_text) or '(empty)'}</p></blockquote>",
        "<p><strong>Archived thread</strong></p>",
        format_archived_comment(comment, author_names),
    ]

    for child in comment.children:
        parts.append(format_archived_comment(child, author_names, label="Reply"))

    return "".join(parts)


def table_row(label: str, value: str) -> str:
    return (
        "<tr>"
        f"<th>{html.escape(label)}</th>"
        f"<td>{html.escape(value or '(empty)')}</td>"
        "</tr>"
    )


def format_archived_comment(
    comment: InlineComment,
    author_names: dict[str, str],
    *,
    label: str = "Comment",
) -> str:
    body = comment.body_storage or "<p>(empty)</p>"
    return (
        "<div>"
        f"<p><strong>{html.escape(label)} {html.escape(comment.id)}</strong></p>"
        "<ul>"
        f"<li>Author: {html.escape(format_author(comment.author_id, author_names))}</li>"
        f"<li>Created at: {html.escape(comment.created_at or '(empty)')}</li>"
        "</ul>"
        "<blockquote>"
        f"{body}"
        "</blockquote>"
        "</div>"
    )


def format_author(author_id: str, author_names: dict[str, str]) -> str:
    if not author_id:
        return "unknown"
    display_name = author_names.get(author_id)
    if not display_name or display_name == author_id:
        return author_id
    return f"{display_name} ({author_id})"


def marker_text_fallback(comment: InlineComment) -> str:
    text = re.sub(r"<[^>]+>", "", comment.body_storage)
    return html.unescape(text).strip()


def hydrate_comments_with_children(
    client: Any,
    comments: tuple[InlineComment, ...],
) -> tuple[InlineComment, ...]:
    hydrated: list[InlineComment] = []
    for comment in comments:
        child_models = client.get_inline_comment_children(comment.id)
        children = tuple(api_comment_to_inline_comment(child) for child in child_models)
        hydrated.append(replace(comment, children=children))
    return tuple(hydrated)


def collect_author_ids(comments: tuple[InlineComment, ...]) -> list[str]:
    author_ids: set[str] = set()
    for comment in comments:
        if comment.author_id:
            author_ids.add(comment.author_id)
        for child in comment.children:
            if child.author_id:
                author_ids.add(child.author_id)
    return sorted(author_ids)


def create_missing_archive_comments(
    client: Any,
    page_id: str,
    comments: tuple[InlineComment, ...],
    existing_footer_comments: list[JsonObject],
    author_names: dict[str, str],
) -> int:
    existing_keys = extract_archive_keys_from_footer_comments(existing_footer_comments)
    created_count = 0
    for comment in comments:
        archive_key = build_archive_key(page_id, comment)
        if archive_key in existing_keys:
            print(f"Archive already exists for inline comment {comment.id}")
            continue
        client.create_footer_comment(
            page_id,
            build_archive_footer_body(page_id, comment, author_names),
        )
        existing_keys.add(archive_key)
        created_count += 1
        print(f"Archived inline comment {comment.id} to page footer")
    return created_count
