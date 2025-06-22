"""Main plugin class implementing pylama interface."""

import ast
from typing import Dict, List, Optional

from .ast_visitor import ASTVisitor
from .config import LengthCheckerConfig
from .line_counter import LineCounter


class LengthCheckerPlugin:
    """Pylama plugin for checking function and class length."""

    name = "length_checker"
    # Enable the plugin by default
    enable = True

    def __init__(self):
        """Initialize the plugin."""
        self.config = LengthCheckerConfig()
        self._errors: List[Dict] = []
        self._config_loaded = False
        self._manual_config = False

    @classmethod
    def add_args(cls, parser):
        """Add command line arguments for the plugin."""
        # Add plugin-specific command line arguments if needed
        parser.add_argument(
            "--length-max-function",
            type=int,
            help="Maximum allowed function length (overrides config file)",
        )
        parser.add_argument(
            "--length-max-class",
            type=int,
            help="Maximum allowed class length (overrides config file)",
        )

    def allow(self, path: str) -> bool:
        """Check if this plugin should process the given file path."""
        # Only process Python files
        return path.endswith((".py", ".pyi"))

    def set_config(self, config: LengthCheckerConfig) -> None:
        """Set configuration manually (prevents loading from pyproject.toml)."""
        self.config = config
        self._manual_config = True

    def run(
        self, path: str, code: Optional[str] = None, params: Optional[dict] = None, **meta
    ) -> List[Dict]:
        """Run the length checker on a file.

        Args:
            path: Path to the file being checked
            code: File content (if None, will read from path)
            params: Additional parameters from pylama
            **meta: Additional metadata

        Returns:
            List of error dictionaries for pylama
        """
        self._errors = []
        self._load_config_if_needed()

        # Override config with command line arguments if provided
        if params:
            self._apply_command_line_params(params)

        code = self._get_file_content(path, code)
        if code is None:
            return []

        try:
            self._analyze_code(code)
        except (SyntaxError, Exception):
            # Skip files with syntax errors or other processing issues
            pass

        return self._errors

    def _apply_command_line_params(self, params: dict) -> None:
        """Apply command line parameters to override config."""
        if "length_max_function" in params and params["length_max_function"] is not None:
            self.config.max_function_length = params["length_max_function"]
        if "length_max_class" in params and params["length_max_class"] is not None:
            self.config.max_class_length = params["length_max_class"]

    def _load_config_if_needed(self) -> None:
        """Load configuration from pyproject.toml if not manually configured."""
        if not self._config_loaded and not self._manual_config:
            self.config = LengthCheckerConfig.from_pyproject_toml()
            self._config_loaded = True

    def _get_file_content(self, path: str, code: Optional[str]) -> Optional[str]:
        """Get file content, reading from path if code is None."""
        if code is not None:
            return code

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def _analyze_code(self, code: str) -> None:
        """Parse and analyze code for length violations."""
        tree = ast.parse(code)
        visitor = ASTVisitor()
        visitor.visit(tree)

        source_lines = code.splitlines()
        line_counter = LineCounter(source_lines)

        for element in visitor.get_all_elements():
            self._check_element_violations(element, line_counter, code)

    def _check_element_violations(self, element, line_counter, code: str) -> None:
        """Check a single element for length violations."""
        effective_lines = line_counter.count_element_lines(element, code)

        if element.node_type == "class" and effective_lines > self.config.max_class_length:
            self._add_class_violation(element, effective_lines)
        elif element.node_type == "function" and effective_lines > self.config.max_function_length:
            self._add_function_violation(element, effective_lines)

    def _add_class_violation(self, element, effective_lines: int) -> None:
        """Add a class length violation."""
        error_dict = {
            "lnum": element.start_line,
            "col": 0,
            "text": f"LA101 Class '{element.name}' is {effective_lines} lines long, "
            f"exceeds maximum of {self.config.max_class_length}",
            "type": "LA101",
        }
        self._errors.append(error_dict)

    def _add_function_violation(self, element, effective_lines: int) -> None:
        """Add a function length violation."""
        error_dict = {
            "lnum": element.start_line,
            "col": 0,
            "text": f"LA102 Function '{element.name}' is {effective_lines} lines long, "
            f"exceeds maximum of {self.config.max_function_length}",
            "type": "LA102",
        }
        self._errors.append(error_dict)
