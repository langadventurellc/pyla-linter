"""Comprehensive unit tests for the length checker plugin."""

from src.linters.length_checker.ast_visitor import ASTVisitor, CodeElement
from src.linters.length_checker.config import LengthCheckerConfig
from src.linters.length_checker.line_counter import LineCounter
from src.linters.length_checker.plugin import LengthCheckerPlugin


class TestASTVisitor:
    """Test the AST visitor functionality."""

    def test_simple_function_detection(self):
        """Test detection of a simple function."""
        code = """def simple_function():
    return 42"""

        visitor = ASTVisitor()
        import ast

        tree = ast.parse(code)
        visitor.visit(tree)

        elements = visitor.get_all_elements()
        assert len(elements) == 1
        assert elements[0].name == "simple_function"
        assert elements[0].node_type == "function"
        assert elements[0].start_line == 1
        assert elements[0].end_line == 2

    def test_simple_class_detection(self):
        """Test detection of a simple class."""
        code = """class SimpleClass:
    def method(self):
        pass"""

        visitor = ASTVisitor()
        import ast

        tree = ast.parse(code)
        visitor.visit(tree)

        elements = visitor.get_all_elements()
        assert len(elements) == 2  # class and method

        class_element = next(e for e in elements if e.node_type == "class")
        method_element = next(e for e in elements if e.node_type == "function")

        assert class_element.name == "SimpleClass"
        assert method_element.name == "method"

    def test_nested_class_function_detection(self):
        """Test detection of nested classes and functions."""
        code = """class OuterClass:
    def outer_method(self):
        def inner_function():
            pass
        return inner_function

    class InnerClass:
        def inner_method(self):
            pass"""

        visitor = ASTVisitor()
        import ast

        tree = ast.parse(code)
        visitor.visit(tree)

        elements = visitor.get_all_elements()
        # Should find: OuterClass, outer_method, inner_function, InnerClass, inner_method
        assert len(elements) == 5

    def test_async_function_detection(self):
        """Test detection of async functions."""
        code = """async def async_function():
    await something()"""

        visitor = ASTVisitor()
        import ast

        tree = ast.parse(code)
        visitor.visit(tree)

        elements = visitor.get_all_elements()
        assert len(elements) == 1
        assert elements[0].name == "async_function"
        assert elements[0].node_type == "function"


class TestLineCounter:
    """Test the line counting functionality."""

    def test_simple_line_counting(self):
        """Test basic line counting without comments or docstrings."""
        code = """def simple_function():
    x = 1
    y = 2
    return x + y"""

        lines = code.splitlines()
        counter = LineCounter(lines)

        element = CodeElement("simple_function", "function", 1, 4)
        actual_lines = counter.count_element_lines(element, code)

        # Should count all 4 lines as they're all code
        assert actual_lines == 4

    def test_line_counting_with_comments(self):
        """Test line counting excluding comment lines."""
        code = """def function_with_comments():
    # This is a comment
    x = 1  # inline comment but line has code
    # Another comment
    return x"""

        lines = code.splitlines()
        counter = LineCounter(lines)

        element = CodeElement("function_with_comments", "function", 1, 5)
        actual_lines = counter.count_element_lines(element, code)

        # Should count 3 lines (function def, x=1 line, return) - excluding comment-only lines
        assert actual_lines == 3

    def test_line_counting_with_docstring(self):
        """Test line counting excluding docstring lines."""
        code = '''def function_with_docstring():
    """This is a docstring.

    It spans multiple lines.
    """
    x = 1
    return x'''

        lines = code.splitlines()
        counter = LineCounter(lines)

        element = CodeElement("function_with_docstring", "function", 1, 7)
        actual_lines = counter.count_element_lines(element, code)

        # Should count 3 lines (function def, x=1, return) - excluding docstring
        assert actual_lines == 3

    def test_line_counting_with_empty_lines(self):
        """Test line counting excluding empty lines."""
        code = """def function_with_empty_lines():

    x = 1

    y = 2

    return x + y"""

        lines = code.splitlines()
        counter = LineCounter(lines)

        element = CodeElement("function_with_empty_lines", "function", 1, 8)
        actual_lines = counter.count_element_lines(element, code)

        # Should count 4 lines (function def, x=1, y=2, return) - excluding empty lines
        assert actual_lines == 4

    def test_class_line_counting(self):
        """Test line counting for classes."""
        code = '''class TestClass:
    """Class docstring."""

    def __init__(self):
        self.x = 1

    # Comment in class
    def method(self):
        """Method docstring."""
        return self.x'''

        lines = code.splitlines()
        counter = LineCounter(lines)

        element = CodeElement("TestClass", "class", 1, 10)
        actual_lines = counter.count_element_lines(element, code)

        # Should count actual code lines, excluding docstrings, comments, and empty lines
        assert actual_lines == 5  # class def, __init__ def, self.x=1, method def, return


class TestLengthCheckerPlugin:
    """Test the main plugin functionality."""

    def test_plugin_initialization(self):
        """Test plugin initializes correctly."""
        plugin = LengthCheckerPlugin()
        assert plugin.name == "length_checker"
        assert plugin.enable is True

    def test_no_violations_under_limit(self):
        """Test that code under limits produces no violations."""
        code = """def short_function():
    return 42

class ShortClass:
    def method(self):
        return True"""

        plugin = LengthCheckerPlugin()
        # Set high limits to ensure no violations
        config = LengthCheckerConfig(max_function_length=50, max_class_length=50)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        assert len(errors) == 0

    def test_function_violation_detection(self):
        """Test detection of function length violations."""
        code = """def long_function():
    line1 = 1
    line2 = 2
    line3 = 3
    line4 = 4
    line5 = 5
    return line1 + line2 + line3 + line4 + line5"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=3, max_class_length=50)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        assert len(errors) == 1
        assert "LA102" in errors[0][2]
        assert "long_function" in errors[0][2]

    def test_class_violation_detection(self):
        """Test detection of class length violations."""
        code = """class LongClass:
    def method1(self):
        return 1

    def method2(self):
        return 2

    def method3(self):
        return 3"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=50, max_class_length=5)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        assert len(errors) == 1
        assert "LA101" in errors[0][2]
        assert "LongClass" in errors[0][2]

    def test_multiple_violations(self):
        """Test detection of multiple violations."""
        code = """class LongClass:
    def long_method1(self):
        line1 = 1
        line2 = 2
        line3 = 3
        return line1 + line2 + line3

    def long_method2(self):
        line1 = 1
        line2 = 2
        line3 = 3
        return line1 + line2 + line3"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=3, max_class_length=8)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        # Should have 3 violations: 1 class + 2 functions
        assert len(errors) == 3

    def test_syntax_error_handling(self):
        """Test that syntax errors are handled gracefully."""
        code = """def broken_function(
    # Missing closing parenthesis
    return 42"""

        plugin = LengthCheckerPlugin()
        errors = plugin.run("test.py", code)
        # Should return empty list, not crash
        assert errors == []

    def test_docstring_exclusion_in_violations(self):
        """Test that docstrings are properly excluded from violation counts."""
        code = '''def function_with_long_docstring():
    """This is a very long docstring.

    It spans many lines to test that these lines
    are not counted toward the function length limit.

    This should not trigger a violation even though
    the total line count is high.
    """
    return 42'''

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=3)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        # Should have no violations because docstring lines are excluded
        assert len(errors) == 0

    def test_nested_function_counting(self):
        """Test that nested functions are counted separately."""
        code = """def outer_function():
    def inner_function():
        line1 = 1
        line2 = 2
        line3 = 3
        line4 = 4
        return line1 + line2 + line3 + line4
    return inner_function()"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=4, max_class_length=50)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        # Both functions should violate (outer: 8 lines, inner: 6 lines > 4 limit)
        assert len(errors) == 2
        error_messages = [error[2] for error in errors]
        assert any("outer_function" in msg for msg in error_messages)
        assert any("inner_function" in msg for msg in error_messages)


class TestErrorReporting:
    """Test comprehensive error reporting functionality."""

    def test_error_message_format_function(self):
        """Test that function error messages follow correct format."""
        code = """def long_function():
    line1 = 1
    line2 = 2
    line3 = 3
    return line1 + line2 + line3"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=3)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        assert len(errors) == 1

        line, column, message = errors[0]
        assert line == 1  # Error reported on function definition line
        assert column == 0  # Column should be 0
        assert message.startswith("LA102")
        assert "long_function" in message
        assert "5 lines long" in message
        assert "exceeds maximum of 3" in message

    def test_error_message_format_class(self):
        """Test that class error messages follow correct format."""
        code = """class LongClass:
    def method1(self):
        return 1
    def method2(self):
        return 2
    def method3(self):
        return 3"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_class_length=5)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        assert len(errors) == 1

        line, column, message = errors[0]
        assert line == 1  # Error reported on class definition line
        assert column == 0  # Column should be 0
        assert message.startswith("LA101")
        assert "LongClass" in message
        assert "7 lines long" in message
        assert "exceeds maximum of 5" in message

    def test_error_codes_are_unique(self):
        """Test that class and function violations have different error codes."""
        code = """class TooLongClass:
    def too_long_function(self):
        line1 = 1
        line2 = 2
        line3 = 3
        line4 = 4
        return line1 + line2 + line3 + line4"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=3, max_class_length=5)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        assert len(errors) == 2

        error_codes = [error[2][:5] for error in errors]
        assert "LA101" in error_codes  # Class error
        assert "LA102" in error_codes  # Function error

    def test_error_line_positioning(self):
        """Test that errors are reported on correct line numbers."""
        code = """# First line comment

class FirstClass:
    def method1(self):
        return 1
    def method2(self):
        return 2

def first_function():
    line1 = 1
    line2 = 2
    line3 = 3

class SecondClass:
    def method1(self):
        return 1
    def method2(self):
        return 2
    def method3(self):
        return 3"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=2, max_class_length=3)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        # Should have violations for first_function, FirstClass, and SecondClass
        assert len(errors) == 3

        # Check that line numbers are correct
        error_lines = [error[0] for error in errors]
        assert 3 in error_lines  # FirstClass starts at line 3
        assert 9 in error_lines  # first_function starts at line 9
        assert 14 in error_lines  # SecondClass starts at line 14

    def test_configuration_threshold_exact_match(self):
        """Test behavior when code length exactly matches configured limits."""
        code = """def exact_limit_function():
    line1 = 1
    line2 = 2
    return line1 + line2"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=4)  # Exactly 4 lines
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        # Should have no violations when exactly at limit
        assert len(errors) == 0

    def test_configuration_threshold_one_over_limit(self):
        """Test behavior when code length is one line over configured limits."""
        code = """def one_over_limit_function():
    line1 = 1
    line2 = 2
    line3 = 3
    return line1 + line2 + line3"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=4)  # 5 lines > 4 limit
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        # Should have exactly 1 violation
        assert len(errors) == 1
        assert "5 lines long, exceeds maximum of 4" in errors[0][2]

    def test_multiple_error_ordering(self):
        """Test that multiple errors are reported in source code order."""
        code = """def first_function():
    line1 = 1
    line2 = 2
    line3 = 3
    return line1 + line2 + line3

def second_function():
    line1 = 1
    line2 = 2
    line3 = 3
    return line1 + line2 + line3"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=3)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        assert len(errors) == 2

        # Errors should be in source order
        assert errors[0][0] < errors[1][0]  # First error line < second error line
        assert "first_function" in errors[0][2]
        assert "second_function" in errors[1][2]

    def test_error_message_includes_actual_and_max_lengths(self):
        """Test that error messages include both actual and maximum lengths."""
        code = """def test_function():
    line1 = 1
    line2 = 2
    line3 = 3
    line4 = 4
    line5 = 5
    line6 = 6
    return line1 + line2 + line3 + line4 + line5 + line6"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=5)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        assert len(errors) == 1

        message = errors[0][2]
        assert "8 lines long" in message  # Actual length
        assert "exceeds maximum of 5" in message  # Configured limit

    def test_error_reporting_with_file_reading(self):
        """Test error reporting when plugin reads file from disk."""
        import os
        import tempfile

        code = """def file_function():
    line1 = 1
    line2 = 2
    line3 = 3
    return line1 + line2 + line3"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            plugin = LengthCheckerPlugin()
            config = LengthCheckerConfig(max_function_length=3)
            plugin.set_config(config)

            # Test with code=None to force file reading
            errors = plugin.run(temp_path, code=None)
            assert len(errors) == 1
            assert "LA102" in errors[0][2]
            assert "file_function" in errors[0][2]
        finally:
            os.unlink(temp_path)

    def test_error_reporting_resilience_to_invalid_files(self):
        """Test that error reporting handles invalid files gracefully."""
        plugin = LengthCheckerPlugin()

        # Test with non-existent file
        errors = plugin.run("/nonexistent/file.py", code=None)
        assert errors == []

        # Test with invalid code that would cause processing errors
        invalid_code = """def broken_function(
    # This is broken syntax
    return 42"""

        errors = plugin.run("test.py", invalid_code)
        assert errors == []  # Should handle gracefully, not crash


class TestEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_lambda_functions_not_counted(self):
        """Test that lambda functions are not counted as regular functions."""
        code = """def regular_function():
    lambda_func = lambda x: x * 2
    return lambda_func(5)"""

        visitor = ASTVisitor()
        import ast

        tree = ast.parse(code)
        visitor.visit(tree)

        elements = visitor.get_all_elements()
        # Should only find the regular function, not the lambda
        assert len(elements) == 1
        assert elements[0].name == "regular_function"

    def test_empty_class(self):
        """Test handling of empty class."""
        code = """class EmptyClass:
    pass"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_class_length=1)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        # Should have 1 violation (2 lines > 1 limit)
        assert len(errors) == 1

    def test_empty_function(self):
        """Test handling of empty function."""
        code = """def empty_function():
    pass"""

        plugin = LengthCheckerPlugin()
        config = LengthCheckerConfig(max_function_length=1)
        plugin.set_config(config)

        errors = plugin.run("test.py", code)
        # Should have 1 violation (2 lines > 1 limit)
        assert len(errors) == 1

    def test_decorator_handling(self):
        """Test that decorators are included in function line count."""
        code = """@decorator1
@decorator2
def decorated_function():
    return 42"""

        visitor = ASTVisitor()
        import ast

        tree = ast.parse(code)
        visitor.visit(tree)

        elements = visitor.get_all_elements()
        assert len(elements) == 1
        # Decorators should be included in the line range
        assert elements[0].start_line == 1  # Starts at first decorator
        assert elements[0].end_line == 4
