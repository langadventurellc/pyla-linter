"""Multiple public items per file linter for pyla-linter.

This module provides a flake8 plugin for checking that files have only one public item.
"""

from .plugin import MultiplePublicItemsPlugin

__all__ = ["MultiplePublicItemsPlugin"]
