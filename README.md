# pyla-linter

A collection of Python linting tools designed to be used with flake8.

## Features

### Length Checker Plugin

A flake8 plugin that enforces configurable line limits for classes and functions, excluding docstrings and comments from the count.

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

The length checker integrates with flake8 as a plugin. Run it using:

```bash
# Check all Python files in current directory with our plugin
flake8 --select=EL

# Check specific files or directories
flake8 --select=EL src/
flake8 --select=EL myfile.py

# Use with all flake8 checks
flake8

# Use only our length checker plugin
flake8 --select=EL001,EL002
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

You can also configure via command line arguments using flake8's standard option system:

```bash
# Use with flake8 ignore/select options
flake8 --select=EL001  # Only check function length
flake8 --select=EL002  # Only check class length
flake8 --ignore=EL001  # Ignore function length violations
```

#### Error Codes

The length checker uses the following error codes:

- **EL001**: Function exceeds maximum line limit
- **EL002**: Class exceeds maximum line limit

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

**Function that would trigger EL001:**

```python
def long_function():  # Line 1
    """This is a docstring (not counted)."""
    
    # This is a comment (not counted)
    
    x = 1  # Line 2
    y = 2  # Line 3
    # ... more code lines
    return x + y  # Line 41 (exceeds default limit of 40)
```

**Class that would trigger EL002:**

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

The length checker works seamlessly with other flake8 plugins:

```bash
# Run with multiple checks (flake8 automatically includes all installed plugins)
flake8

# Run only our length checker with other specific checks
flake8 --select=E,F,EL

# Include in existing CI/CD pipelines
poetry run flake8 src/
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