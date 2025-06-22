"""Logic for counting lines excluding docstrings and comments."""

import ast
from typing import List, Sequence, Set

from .ast_visitor import CodeElement


class LineCounter:
    """Counts actual code lines, excluding docstrings and comments."""

    def __init__(self, source_lines: Sequence[str]):
        self.source_lines = source_lines
        self._comment_lines = self._find_comment_lines()
        self._docstring_lines = set()

    def count_element_lines(self, element: CodeElement, source_code: str) -> int:
        """Count lines for a code element, excluding docstrings and comments.

        Args:
            element: The code element to count lines for
            source_code: The full source code of the file

        Returns:
            Number of actual code lines (excluding docstrings and comments)
        """
        # Find docstring lines for this element
        self._find_docstring_lines(element, source_code)

        # Count lines between start and end, excluding comments and docstrings
        actual_lines = 0
        for line_num in range(element.start_line, element.end_line + 1):
            if self._is_code_line(line_num):
                actual_lines += 1

        return actual_lines

    def _find_comment_lines(self) -> Set[int]:
        """Find all lines that are comments or contain only comments."""
        comment_lines = set()

        for i, line in enumerate(self.source_lines, 1):
            stripped = line.strip()
            # Check if line is a comment or starts with comment after whitespace
            if stripped.startswith("#") or (not stripped):
                comment_lines.add(i)
            else:
                # Check for inline comments - but only if they're the only content
                # We want to keep lines with code + comments as they contain actual code
                pass

        return comment_lines

    def _find_docstring_lines(self, element: CodeElement, source_code: str) -> None:
        """Find docstring lines for a specific code element."""
        try:
            # Parse the source to find docstrings
            tree = ast.parse(source_code)
            docstring_finder = DocstringFinder()
            docstring_finder.visit(tree)

            # Find docstrings that belong to this element
            for start_line, end_line in docstring_finder.docstring_ranges:
                if start_line >= element.start_line and end_line <= element.end_line:
                    for line_num in range(start_line, end_line + 1):
                        self._docstring_lines.add(line_num)

        except (SyntaxError, ValueError):
            # If parsing fails, don't exclude any docstring lines
            pass

    def _is_code_line(self, line_num: int) -> bool:
        """Check if a line number represents actual code."""
        # Line is code if it's not a comment line and not a docstring line
        if line_num in self._comment_lines or line_num in self._docstring_lines:
            return False

        # Also check if the line is just whitespace
        if line_num <= len(self.source_lines):
            line_content = self.source_lines[line_num - 1].strip()
            return bool(line_content)

        return False


class DocstringFinder(ast.NodeVisitor):
    """AST visitor to find docstring locations."""

    def __init__(self):
        self.docstring_ranges: List[tuple[int, int]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition and check for docstring."""
        self._check_for_docstring(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition and check for docstring."""
        self._check_for_docstring(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition and check for docstring."""
        self._check_for_docstring(node)
        self.generic_visit(node)

    def visit_Module(self, node: ast.Module) -> None:
        """Visit module and check for module-level docstring."""
        self._check_for_docstring(node)
        self.generic_visit(node)

    def _check_for_docstring(self, node) -> None:
        """Check if a node has a docstring and record its location."""
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            docstring_node = node.body[0]
            start_line = docstring_node.lineno
            end_line = docstring_node.end_lineno or start_line
            self.docstring_ranges.append((start_line, end_line))
