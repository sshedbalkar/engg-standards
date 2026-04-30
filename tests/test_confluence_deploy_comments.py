from __future__ import annotations

import unittest
from contextlib import redirect_stdout
from io import StringIO

from scripts.confluence_deploy.comments import (
    apply_inline_comment_markers,
    build_archive_footer_body,
    build_archive_key,
    create_missing_archive_comments,
    extract_archive_keys_from_footer_comments,
    extract_inline_markers,
)
from scripts.confluence_deploy.models import InlineComment


def inline_comment(
    comment_id: str,
    marker_ref: str,
    selection: str,
    *,
    body: str = "<p>Needs review.</p>",
    author_id: str = "account-1",
    created_at: str = "2026-04-27T10:00:00.000Z",
    children: tuple[InlineComment, ...] = (),
) -> InlineComment:
    return InlineComment(
        id=comment_id,
        marker_ref=marker_ref,
        original_selection=selection,
        body_storage=body,
        author_id=author_id,
        created_at=created_at,
        resolution_status="open",
        webui="/wiki/comment",
        children=children,
    )


class FakeConfluenceClient:
    def __init__(self) -> None:
        self.created: list[tuple[str, str]] = []

    def create_footer_comment(self, page_id: str, storage_body: str) -> dict[str, str]:
        self.created.append((page_id, storage_body))
        return {"id": str(len(self.created))}


class InlineCommentPreservationTests(unittest.TestCase):
    def test_extract_inline_comment_markers(self) -> None:
        storage = (
            '<p>A <ac:inline-comment-marker ac:ref="ref-1">'
            "selected text"
            "</ac:inline-comment-marker> B</p>"
        )

        markers = extract_inline_markers(storage)

        self.assertEqual(["ref-1"], sorted(markers))
        self.assertEqual("selected text", markers["ref-1"].inner_html)

    def test_preserves_comment_by_reinserting_exact_existing_marker_body(self) -> None:
        current_storage = (
            "<p>Keep "
            '<ac:inline-comment-marker ac:ref="ref-1">critical text</ac:inline-comment-marker>'
            " here.</p>"
        )
        generated = "<p>Keep critical text here.</p>"
        comment = inline_comment("comment-1", "ref-1", "critical text")

        result = apply_inline_comment_markers(generated, current_storage, [comment])

        expected_marker = (
            '<ac:inline-comment-marker ac:ref="ref-1">'
            "critical text"
            "</ac:inline-comment-marker>"
        )
        self.assertIn(expected_marker, result.html)
        self.assertEqual((comment,), result.preserved)
        self.assertEqual((), result.to_archive)

    def test_preserves_comment_by_unique_original_selection_fallback(self) -> None:
        generated = "<p>Keep unique selection here.</p>"
        comment = inline_comment("comment-1", "ref-1", "unique selection")

        result = apply_inline_comment_markers(generated, "<p>No marker left.</p>", [comment])

        expected_marker = (
            '<ac:inline-comment-marker ac:ref="ref-1">'
            "unique selection"
            "</ac:inline-comment-marker>"
        )
        self.assertIn(expected_marker, result.html)
        self.assertEqual((comment,), result.preserved)
        self.assertEqual((), result.to_archive)

    def test_archives_comment_when_selection_is_ambiguous(self) -> None:
        generated = "<p>Repeat this.</p><p>Repeat this.</p>"
        comment = inline_comment("comment-1", "ref-1", "Repeat this.")

        result = apply_inline_comment_markers(generated, "<p>No marker left.</p>", [comment])

        self.assertEqual(generated, result.html)
        self.assertEqual((), result.preserved)
        self.assertEqual((comment,), result.to_archive)

    def test_archives_comment_when_selection_is_deleted(self) -> None:
        generated = "<p>The paragraph changed.</p>"
        comment = inline_comment("comment-1", "ref-1", "Deleted text")

        result = apply_inline_comment_markers(generated, "<p>No marker left.</p>", [comment])

        self.assertEqual(generated, result.html)
        self.assertEqual((), result.preserved)
        self.assertEqual((comment,), result.to_archive)

    def test_builds_archive_body_with_original_metadata_and_thread(self) -> None:
        reply = inline_comment(
            "reply-1",
            "",
            "",
            body="<p>Reply body.</p>",
            author_id="account-2",
            created_at="2026-04-27T11:00:00.000Z",
        )
        comment = inline_comment(
            "comment-1",
            "ref-1",
            "Original selected text",
            body="<p>Root body.</p>",
            children=(reply,),
        )
        author_names = {"account-1": "Author One", "account-2": "Author Two"}

        body = build_archive_footer_body("123", comment, author_names)

        self.assertIn(build_archive_key("123", comment), body)
        self.assertIn("Author One (account-1)", body)
        self.assertIn("Author Two (account-2)", body)
        self.assertIn("Original selected text", body)
        self.assertIn("<p>Root body.</p>", body)
        self.assertIn("<p>Reply body.</p>", body)

    def test_archive_creation_is_idempotent_by_archive_key(self) -> None:
        client = FakeConfluenceClient()
        comment = inline_comment("comment-1", "ref-1", "Deleted text")
        existing_body = build_archive_footer_body("123", comment, {"account-1": "Author One"})
        existing_footer_comments = [
            {"body": {"storage": {"value": existing_body}}},
        ]

        with redirect_stdout(StringIO()):
            created_count = create_missing_archive_comments(
                client,
                "123",
                (comment,),
                existing_footer_comments,
                {"account-1": "Author One"},
            )

        self.assertEqual(0, created_count)
        self.assertEqual([], client.created)
        self.assertEqual(
            {build_archive_key("123", comment)},
            extract_archive_keys_from_footer_comments(existing_footer_comments),
        )


if __name__ == "__main__":
    unittest.main()

