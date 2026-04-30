"""High-level Confluence publishing workflow."""

from __future__ import annotations

import csv
import importlib.util
import os
from pathlib import Path

from .client import ConfluenceClient
from .comments import (
    api_comment_to_inline_comment,
    apply_inline_comment_markers,
    collect_author_ids,
    create_missing_archive_comments,
    extract_marker_refs,
    hydrate_comments_with_children,
)
from .markdown_renderer import render_markdown_storage
from .metadata import (
    build_document_metadata_payload,
    build_source_metadata,
    expected_page_metadata_after_update,
    extract_page_metadata,
    inject_sync_metadata_block,
    utc_now_iso,
    verify_metadata_property,
)
from .models import (
    ConfluenceDeployError,
    ConfluenceRow,
    InlineComment,
    JsonObject,
    SYNC_METADATA_PROPERTY_KEY,
    extract_storage_value,
)
from .output import warn


def load_confluence_rows(csv_path: Path) -> list[ConfluenceRow]:
    if not csv_path.is_file():
        raise ConfluenceDeployError(f"Confluence mapping CSV not found: {csv_path}")

    rows: list[ConfluenceRow] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        for raw in reader:
            content_type = (raw.get("type") or "").strip()
            page_to = (raw.get("page_to") or "").strip()
            path = (raw.get("path") or "").strip()
            if not content_type or not page_to or not path:
                raise ConfluenceDeployError(f"Invalid Confluence mapping row: {raw}")
            rows.append(
                ConfluenceRow(
                    content_type=content_type,
                    page_to=page_to,
                    path=path,
                )
            )
    return rows


def parse_changed_files(changed_env: str) -> tuple[set[str], bool]:
    changed_files = {item.strip() for item in changed_env.split(",") if item.strip()}
    return changed_files, not changed_files


def select_rows_to_publish(
    rows: list[ConfluenceRow],
    changed_files: set[str],
    publish_all: bool,
) -> list[ConfluenceRow]:
    selected_rows: list[ConfluenceRow] = []
    for row in rows:
        if not publish_all and row.path not in changed_files:
            print(f"Skipping unchanged file: {row.path}")
            continue
        selected_rows.append(row)
    return selected_rows


def validate_runtime_dependencies(rows: list[ConfluenceRow]) -> None:
    required_modules = {"requests": "requests"}
    if any(row.content_type == "content" for row in rows):
        required_modules["markdown"] = "markdown"
        required_modules["bs4"] = "beautifulsoup4"
    if any(row.content_type == "image" for row in rows):
        required_modules["atlassian"] = "atlassian-python-api"

    missing_packages = [
        package_name
        for module_name, package_name in sorted(required_modules.items())
        if importlib.util.find_spec(module_name) is None
    ]
    if missing_packages:
        raise ConfluenceDeployError(
            "Missing dependencies: "
            f"{', '.join(missing_packages)}. Install workflow dependencies first."
        )


def open_markdown_file(file_path: Path) -> str:
    if not file_path.is_file():
        raise ConfluenceDeployError(f"Markdown file not found: {file_path}")
    return file_path.read_text(encoding="utf-8")


def build_page_update_payload(
    page_id: str,
    current_page: JsonObject,
    storage_html: str,
) -> JsonObject:
    return {
        "id": str(page_id),
        "status": "current",
        "title": current_page["title"],
        "version": {
            "number": current_page["version"]["number"] + 1,
            "message": "Automated ESTD docs sync",
        },
        "body": {"representation": "storage", "value": storage_html},
    }


def get_page_storage(page: JsonObject) -> str:
    return extract_storage_value(page)


def canonical_page_url(
    page: JsonObject,
    *,
    cloud: str,
    space_key: str,
    page_id: str,
) -> str:
    base = page.get("_links", {}).get("base", f"https://{cloud}.atlassian.net/wiki")
    webui = page.get("_links", {}).get("webui", f"/spaces/{space_key}/pages/{page_id}")
    return base + webui


def build_confluence_url_maps(
    client: ConfluenceClient,
    rows: list[ConfluenceRow],
    *,
    cloud: str,
    space_key: str,
) -> tuple[dict[str, str], dict[str, str]]:
    filename_to_page_url: dict[str, str] = {}
    page_id_to_url: dict[str, str] = {}

    for row in rows:
        if row.content_type != "content":
            continue
        try:
            page = client.get_page(row.page_to)
        except ConfluenceDeployError as exc:
            warn(f"could not fetch canonical URL for page {row.page_to}: {exc}")
            continue
        canonical = canonical_page_url(
            page,
            cloud=cloud,
            space_key=space_key,
            page_id=row.page_to,
        )
        page_id_to_url[row.page_to] = canonical
        filename_to_page_url[os.path.basename(row.path)] = canonical

    return filename_to_page_url, page_id_to_url


def upload_confluence_content(
    client: ConfluenceClient,
    workspace: Path,
    file_path: Path,
    source_path: str,
    page_id: str,
    filename_to_page_url: dict[str, str],
    page_id_to_url: dict[str, str],
    *,
    cloud: str,
    space_key: str,
) -> None:
    current_page = client.get_page(page_id, body_format="storage")
    current_storage = get_page_storage(current_page)
    before_metadata = extract_page_metadata(current_page)
    current_page_url = page_id_to_url.get(
        str(page_id),
        f"https://{cloud}.atlassian.net/wiki/spaces/{space_key}/pages/{page_id}",
    )

    markdown_text = open_markdown_file(file_path)
    source_metadata = build_source_metadata(
        workspace=workspace,
        source_path=source_path,
        file_path=file_path,
        markdown_text=markdown_text,
    )
    sync_timestamp = utc_now_iso()
    expected_after_metadata = expected_page_metadata_after_update(
        before_metadata,
        current_page,
        sync_timestamp,
    )
    visible_metadata = build_document_metadata_payload(
        source_metadata,
        before_metadata,
        expected_after_metadata,
        sync_timestamp,
    )
    generated_html = render_markdown_storage(
        markdown_text,
        filename_to_page_url,
        current_page_url,
    )
    generated_html = inject_sync_metadata_block(generated_html, visible_metadata)
    root_comment_models = client.list_page_inline_comments(page_id)
    root_comments = [api_comment_to_inline_comment(item) for item in root_comment_models]
    preservation = apply_inline_comment_markers(generated_html, current_storage, root_comments)
    comments_to_archive = hydrate_comments_with_children(client, preservation.to_archive)
    author_names = {}
    try:
        author_names = client.get_users_bulk(collect_author_ids(comments_to_archive))
    except ConfluenceDeployError as exc:
        warn(f"could not resolve Confluence user names: {exc}")

    footer_count_before = len(client.list_page_footer_comments(page_id))
    payload = build_page_update_payload(page_id, current_page, preservation.html)
    updated = client.update_page(page_id, payload)
    after_metadata = extract_page_metadata(updated)
    preserved_metadata = build_document_metadata_payload(
        source_metadata,
        before_metadata,
        after_metadata,
        sync_timestamp,
    )
    client.upsert_page_property(
        page_id,
        SYNC_METADATA_PROPERTY_KEY,
        preserved_metadata,
    )
    verify_metadata_property(client, page_id, preserved_metadata)
    updated_link = canonical_page_url(
        updated,
        cloud=cloud,
        space_key=space_key,
        page_id=page_id,
    )

    post_update_footer_comments = client.list_page_footer_comments(page_id)
    create_missing_archive_comments(
        client,
        page_id,
        comments_to_archive,
        post_update_footer_comments,
        author_names,
    )
    verify_upload(
        client,
        page_id,
        preserved_comments=preservation.preserved,
        footer_count_before=footer_count_before,
    )
    print(f"Uploaded content successfully to page {updated_link}")


def verify_upload(
    client: ConfluenceClient,
    page_id: str,
    *,
    preserved_comments: tuple[InlineComment, ...],
    footer_count_before: int,
) -> None:
    current_page = client.get_page(page_id, body_format="storage")
    current_refs = extract_marker_refs(get_page_storage(current_page))
    missing_refs = sorted(
        comment.marker_ref
        for comment in preserved_comments
        if comment.marker_ref and comment.marker_ref not in current_refs
    )
    if missing_refs:
        raise ConfluenceDeployError(
            f"Confluence page {page_id} lost preserved inline markers: {missing_refs}"
        )

    footer_count_after = len(client.list_page_footer_comments(page_id))
    if footer_count_after < footer_count_before:
        raise ConfluenceDeployError(
            f"Confluence page {page_id} footer comments decreased: "
            f"{footer_count_before} -> {footer_count_after}"
        )


def upload_confluence_image(
    image_path: Path,
    page_id: str,
    *,
    cloud: str,
    user: str,
    token: str,
) -> None:
    if not image_path.is_file():
        raise ConfluenceDeployError(f"Image file not found: {image_path}")
    try:
        from atlassian import Confluence
    except ImportError as exc:
        raise ConfluenceDeployError(
            "Missing dependency: atlassian-python-api. Install workflow dependencies first."
        ) from exc

    confluence = Confluence(
        url=f"https://{cloud}.atlassian.net",
        username=user,
        password=token,
    )
    confluence.attach_file(
        str(image_path),
        name=None,
        content_type=None,
        page_id=page_id,
        title=None,
        space=None,
        comment=None,
    )
    print("Uploaded image to Confluence")


def run_sync(
    *,
    workspace: Path,
    cloud: str,
    space_key: str,
    user: str,
    token: str,
    changed_files_env: str,
) -> None:
    rows = load_confluence_rows(workspace / "docs" / "docs_for_confluence.csv")
    changed_files, publish_all = parse_changed_files(changed_files_env)
    rows_to_publish = select_rows_to_publish(rows, changed_files, publish_all)
    validate_runtime_dependencies(rows_to_publish)

    client = ConfluenceClient(cloud, user, token)
    filename_to_page_url, page_id_to_url = build_confluence_url_maps(
        client,
        rows,
        cloud=cloud,
        space_key=space_key,
    )

    for row in rows_to_publish:
        if row.content_type == "content":
            client.set_page_width(row.page_to)
            upload_confluence_content(
                client,
                workspace,
                workspace / row.path,
                row.path,
                row.page_to,
                filename_to_page_url,
                page_id_to_url,
                cloud=cloud,
                space_key=space_key,
            )
        elif row.content_type == "image":
            upload_confluence_image(
                workspace / row.path,
                row.page_to,
                cloud=cloud,
                user=user,
                token=token,
            )
        else:
            warn(f"unsupported content type skipped: {row.content_type}")
