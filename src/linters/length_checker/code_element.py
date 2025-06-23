"""Represents a code element (class or function) with its location and nested elements."""

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .line_counter import LineCounter


class CodeElement:
    """Represents a code element (class or function) with its location and nested elements."""

    def __init__(self, name: str, node_type: str, start_line: int, end_line: int):
        self.name = name
        self.node_type = node_type  # "class" or "function"
        self.start_line = start_line
        self.end_line = end_line
        self.nested_elements: List["CodeElement"] = []

    @property
    def total_lines(self) -> int:
        """Total lines including nested elements."""
        return self.end_line - self.start_line + 1

    def get_effective_lines(self, line_counter: "LineCounter") -> int:
        """Get effective code lines excluding docstrings and comments."""
        return line_counter.count_element_lines(self, "")

    def __repr__(self) -> str:
        return f"CodeElement({self.name}, {self.node_type}, {self.start_line}-{self.end_line})"
