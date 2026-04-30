from __future__ import annotations

import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts.confluence_deploy.cli import main


class ConfluenceCliTests(unittest.TestCase):
    def test_missing_workspace_returns_validation_failure(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with redirect_stderr(StringIO()):
                exit_code = main([])

        self.assertEqual(1, exit_code)

    def test_valid_inputs_delegate_to_sync(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "CONF_USER": "user",
                "CONF_TOKEN": "token",
                "CHANGED_FILES": "docs/a.md",
            },
            clear=True,
        ):
            with patch("scripts.confluence_deploy.cli.run_sync") as run_sync:
                exit_code = main(["--workspace", str(Path.cwd())])

        self.assertEqual(0, exit_code)
        run_sync.assert_called_once()


if __name__ == "__main__":
    unittest.main()
