# pyla-linter

A collection of Python linting tools designed to be used with Pylama.

## Features

### Length Checker Plugin

A Pylama plugin that enforces configurable line limits for classes and functions, excluding docstrings and comments from the count.

#### Installation

Install using Poetry:

```bash
poetry add pyla-linter
```

Or using pip:

```bash
pip install pyla-linter
```

#### Usage

The length checker integrates with Pylama as a plugin. Run it using:

```bash
# Check all Python files in current directory
pylama

# Check specific files or directories
pylama src/
pylama myfile.py

# Use with specific linters only
pylama --linters=length_checker
```

#### Configuration

Configure the length checker in your `pyproject.toml` file:

```toml
[tool.pyla-linters]
# Maximum lines for functions (default: 40)
max_function_length = 40

# Maximum lines for classes (default: 200)
max_class_length = 200
```

You can also configure via command line arguments:

```bash
# Set custom limits
pylama --max-function-length=30 --max-class-length=150
```

#### Error Codes

The length checker uses the following error codes:

- **LA101**: Function exceeds maximum line limit
- **LA102**: Class exceeds maximum line limit

#### Line Counting Logic

The plugin counts only actual code lines, excluding:

- Empty lines
- Comment lines (starting with `#`)
- Docstrings (string literals at the beginning of functions/classes)
- Lines with only whitespace

For nested structures:
- Nested functions/classes count toward their parent's line total
- Decorators are included in the count for the decorated element

#### Examples

**Function that would trigger LA101:**

```python
def long_function():  # Line 1
    """This is a docstring (not counted)."""
    
    # This is a comment (not counted)
    
    x = 1  # Line 2
    y = 2  # Line 3
    # ... more code lines
    return x + y  # Line 41 (exceeds default limit of 40)
```

**Class that would trigger LA102:**

```python
class LargeClass:  # Line 1
    """Class docstring (not counted)."""
    
    def method1(self):  # Line 2
        pass  # Line 3
    
    # ... many more methods
    
    def method_N(self):  # Line 201 (exceeds default limit of 200)
        pass  # Line 202
```

#### Integration with Existing Workflow

The length checker works seamlessly with other Pylama linters:

```bash
# Run with multiple linters
pylama --linters=pyflakes,pycodestyle,length_checker

# Include in existing CI/CD pipelines
poetry run pylama src/
```

## Development

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd pyla-linter

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linting and formatting
poetry run poe autolint
```

### Quality Checks

Before submitting changes, ensure all quality checks pass:

```bash
# Format code
poetry run poe format

# Run linting
poetry run poe lint

# Type checking
poetry run pyright

# Run tests
poetry run pytest
```

## License

[License information would go here]