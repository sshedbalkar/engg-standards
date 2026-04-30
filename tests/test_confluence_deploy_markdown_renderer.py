from __future__ import annotations

import unittest

from scripts.confluence_deploy.markdown_renderer import rewrite_links, to_github_anchor


class MarkdownRendererTests(unittest.TestCase):
    def test_to_github_anchor_matches_existing_behavior(self) -> None:
        self.assertEqual(
            "api-reference-rest-vs-graphql",
            to_github_anchor("API Reference: REST vs GraphQL"),
        )

    def test_rewrites_markdown_links_to_confluence_urls(self) -> None:
        rendered = '<p><a href="./ESTD1.md#section">ESTD1</a></p>'

        rewritten = rewrite_links(
            rendered,
            {"ESTD1.md": "https://example.atlassian.net/wiki/pages/1"},
            "https://example.atlassian.net/wiki/pages/current",
        )

        self.assertIn("https://example.atlassian.net/wiki/pages/1#section", rewritten)


if __name__ == "__main__":
    unittest.main()

