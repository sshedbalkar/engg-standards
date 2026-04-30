from __future__ import annotations

import unittest
from contextlib import redirect_stdout
from io import StringIO

from scripts.confluence_deploy.models import ConfluenceRow
from scripts.confluence_deploy.publisher import select_rows_to_publish


class ConfluencePublisherTests(unittest.TestCase):
    def test_select_rows_to_publish_reports_skipped_rows(self) -> None:
        rows = [
            ConfluenceRow("content", "1", "docs/a.md"),
            ConfluenceRow("content", "2", "docs/b.md"),
        ]

        with redirect_stdout(StringIO()) as output:
            selected = select_rows_to_publish(rows, {"docs/a.md"}, False)

        self.assertEqual([rows[0]], selected)
        self.assertIn("Skipping unchanged file: docs/b.md", output.getvalue())


if __name__ == "__main__":
    unittest.main()
