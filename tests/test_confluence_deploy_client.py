from __future__ import annotations

import unittest

from scripts.confluence_deploy.client import format_adapter_error_text


class ConfluenceClientTests(unittest.TestCase):
    def test_adapter_error_text_is_redacted_and_bounded(self) -> None:
        raw_text = f"token=secret-value {'x' * 2000}"

        formatted = format_adapter_error_text(raw_text)

        self.assertIn("token=[REDACTED]", formatted)
        self.assertNotIn("secret-value", formatted)
        self.assertLessEqual(len(formatted), 1214)


if __name__ == "__main__":
    unittest.main()

