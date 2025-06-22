"""Main plugin class implementing pylama interface."""

from typing import List, Optional, Tuple

from .config import LengthCheckerConfig


class LengthCheckerPlugin:
    """Pylama plugin for checking function and class length."""

    name = "length_checker"
    # Enable the plugin by default
    enable = True

    def __init__(self):
        """Initialize the plugin."""
        self.config = LengthCheckerConfig()
        self._errors: List[Tuple[int, int, str]] = []

    def run(
        self, path: str, code: Optional[str] = None, params: Optional[dict] = None, **meta
    ) -> List[Tuple[int, int, str]]:
        """Run the length checker on a file.

        Args:
            path: Path to the file being checked
            code: File content (if None, will read from path)
            params: Additional parameters from pylama
            **meta: Additional metadata

        Returns:
            List of errors as (line, column, message) tuples
        """
        self._errors = []

        # Load configuration from pyproject.toml
        self.config = LengthCheckerConfig.from_pyproject_toml()

        if code is None:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception:
                return []

        # For now, just return empty list - AST parsing will be implemented in task 2.0
        # This allows the plugin to be loaded and tested with pylama
        return self._errors
