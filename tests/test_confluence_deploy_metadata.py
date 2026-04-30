from __future__ import annotations

import unittest

from scripts.confluence_deploy.metadata import (
    build_page_property_payload,
    extract_markdown_metadata_fields,
    inject_sync_metadata_block,
    select_source_created_at,
    select_source_modified_at,
)
from scripts.confluence_deploy.models import SYNC_METADATA_PROPERTY_KEY


class ConfluenceMetadataTests(unittest.TestCase):
    def test_extracts_estd_metadata_table(self) -> None:
        markdown = """# ESTD1 - Common Standards

| Field | Value |
|:------|:------|
| Document ID | ESTD1 |
| Version | 5.1 |
| Last Updated | 2026-04-19 |
| Depends On | [ESTD0](./ESTD0.md) |

## Body
"""

        fields = extract_markdown_metadata_fields(markdown)

        self.assertEqual("ESTD1", fields["Document ID"])
        self.assertEqual("5.1", fields["Version"])
        self.assertEqual("2026-04-19", fields["Last Updated"])
        self.assertEqual("ESTD0", fields["Depends On"])

    def test_extracts_estd15_style_bold_metadata_table(self) -> None:
        markdown = """# Technical Approach Document: Feature

| Field | Value |
|:----|:----|
| **Type** | TAD |
| **Status** | Draft |
| **Created** | 2026-04-01 |
| **Last Updated** | 2026-04-02 |
"""

        fields = extract_markdown_metadata_fields(markdown)

        self.assertEqual("TAD", fields["Type"])
        self.assertEqual("Draft", fields["Status"])
        self.assertEqual("2026-04-01", fields["Created"])
        self.assertEqual("2026-04-02", fields["Last Updated"])

    def test_source_dates_fall_back_to_git_when_doc_fields_are_missing(self) -> None:
        fields = {"Last Updated": "2026-04-02"}

        created_at = select_source_created_at(fields, "2026-03-01T12:00:00+00:00")
        modified_at = select_source_modified_at(fields, "2026-04-03T12:00:00+00:00")

        self.assertEqual("2026-03-01T12:00:00+00:00", created_at)
        self.assertEqual("2026-04-02", modified_at)

    def test_builds_create_page_property_payload_without_version(self) -> None:
        payload = build_page_property_payload(
            SYNC_METADATA_PROPERTY_KEY,
            {"schemaVersion": 1},
            None,
        )

        self.assertEqual(
            {"key": SYNC_METADATA_PROPERTY_KEY, "value": {"schemaVersion": 1}},
            payload,
        )

    def test_builds_update_page_property_payload_with_bumped_version(self) -> None:
        existing = {"id": "property-1", "version": {"number": 7}}

        payload = build_page_property_payload(
            SYNC_METADATA_PROPERTY_KEY,
            {"schemaVersion": 1},
            existing,
        )

        self.assertEqual(SYNC_METADATA_PROPERTY_KEY, payload["key"])
        self.assertEqual({"schemaVersion": 1}, payload["value"])
        self.assertEqual(8, payload["version"]["number"])

    def test_sync_metadata_block_replaces_existing_block(self) -> None:
        metadata = {
            "source": {
                "path": "docs/ESTD1.md",
                "createdAt": "2026-03-01",
                "lastModifiedAt": "2026-04-01",
                "sha256": "abc123",
            },
            "confluenceBeforeSync": {
                "createdAt": "2026-02-01T00:00:00.000Z",
                "versionNumber": 3,
            },
            "confluenceAfterSync": {"versionNumber": 4},
            "sync": {"syncedAt": "2026-04-28T10:00:00+00:00"},
        }
        html = (
            "<h1>Title</h1>"
            "<table><tbody><tr><td>A</td></tr></tbody></table>"
            "<p>Body text</p>"
        )

        first = inject_sync_metadata_block(html, metadata)
        second = inject_sync_metadata_block(first, metadata)

        self.assertEqual(1, second.count("ESTD_SYNC_METADATA_START"))
        self.assertEqual(1, second.count("ESTD sync metadata"))
        self.assertIn("docs/ESTD1.md", second)
        self.assertGreater(second.find("ESTD sync metadata"), second.find("Body text"))
        self.assertTrue(second.rstrip().endswith("<!-- ESTD_SYNC_METADATA_END -->"))


if __name__ == "__main__":
    unittest.main()
