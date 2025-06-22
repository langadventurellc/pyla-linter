# Feature Implementation Plan: Class and Function Length Linting

_Generated: 2025-06-22_
_Based on Feature Specification: /Users/zach/code/pyla-linter/.tasks/20250622/20250622-class-function-length-linting-feature.md_

## Architecture Overview

This implementation integrates a length-checking linter directly into the pyla-linter package as a custom pylama plugin. The plugin uses Python's AST module to analyze source files and enforce configurable line limits for classes and functions, excluding docstrings and comments from the count.

### System Architecture

```mermaid
graph TB
    subgraph "pyla-linter Package"
        A[pylama CLI] --> B[Plugin Registry]
        B --> C[Length Checker Plugin]
        C --> D[AST Parser]
        C --> E[Line Counter]
        C --> F[Violation Reporter]
        G[Configuration Loader] --> C
    end
    
    H[Python Source Files] --> A
    I[pyproject.toml] --> G
    F --> J[Error Output]
    
    style C fill:#f9f,stroke:#333,stroke-width:2px
```

### Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Pylama
    participant LengthChecker
    participant ASTParser
    participant Config
    
    User->>Pylama: Run linting
    Pylama->>Config: Load configuration
    Config->>LengthChecker: Provide limits
    Pylama->>LengthChecker: Process file
    LengthChecker->>ASTParser: Parse source
    ASTParser->>LengthChecker: Return AST
    LengthChecker->>LengthChecker: Count lines
    LengthChecker->>LengthChecker: Check violations
    LengthChecker->>Pylama: Return errors
    Pylama->>User: Display results
```

## Technology Stack

### Core Technologies

- **Language/Runtime:** Python 3.12+
- **Framework:** pylama 8.4.1+ (linting framework)
- **Parser:** Python AST (Abstract Syntax Tree) module

### Libraries & Dependencies

- **Backend/API:** Built-in Python ast module for parsing
- **Testing:** pytest (following project conventions)
- **Utilities:** pyla-logger for structured logging

### Patterns & Approaches

- **Architectural Patterns:** Plugin architecture, Visitor pattern for AST traversal
- **Design Patterns:** Strategy pattern for line counting logic
- **Development Practices:** TDD, modular design with single responsibility

### External Integrations

- **Tools:** Integrates with pylama via entry points mechanism
- **Configuration:** Reads from pyproject.toml under `[tool.pyla-linters]`

## Relevant Files

- `src/linters/__init__.py` - Update to expose the new linter module
- `src/linters/length_checker/__init__.py` - Package initialization for the length checker
- `src/linters/length_checker/plugin.py` - Main plugin class implementing pylama interface
- `src/linters/length_checker/ast_visitor.py` - AST visitor for analyzing code structure
- `src/linters/length_checker/line_counter.py` - Logic for counting lines excluding docstrings/comments
- `src/linters/length_checker/config.py` - Configuration handling for the plugin
- `src/tests/linters/length_checker/test_length_checker.py` - Comprehensive unit tests
- `pyproject.toml` - Update with plugin entry point and example configuration

## Implementation Notes

- Tests should be placed in `src/tests/` following the existing project structure
- Use `poetry run pytest` for running tests
- Follow the existing code style (black, isort) and quality standards
- Run `poetry run poe autolint` after each task to ensure code quality
- After completing each subtask, mark it complete and document files modified
- After completing a parent task, stop and wait for user confirmation to proceed

## Implementation Tasks

- [x] 1.0 Set up plugin structure and configuration

  - [x] 1.1 Create length_checker package structure under src/linters/
  - [x] 1.2 Implement configuration loader for [tool.pyla-linters] section
  - [x] 1.3 Add plugin entry point to pyproject.toml
  - [x] 1.4 Create basic plugin class with pylama interface

  ### Files modified with description of changes

  - `src/linters/__init__.py` - Created package initialization file for linters module
  - `src/linters/length_checker/__init__.py` - Created package initialization with plugin export
  - `src/linters/length_checker/plugin.py` - Implemented basic LengthCheckerPlugin class with pylama interface
  - `src/linters/length_checker/ast_visitor.py` - Created placeholder file for AST visitor (to be implemented in task 2.0)
  - `src/linters/length_checker/line_counter.py` - Created placeholder file for line counting logic (to be implemented in task 2.0)
  - `src/linters/length_checker/config.py` - Implemented LengthCheckerConfig class with pyproject.toml loading
  - `pyproject.toml` - Added plugin entry point under [tool.poetry.plugins."pylama.linter"] and example configuration under [tool.pyla-linters]

- [x] 2.0 Implement AST parsing and line counting logic

  - [x] 2.1 Create AST visitor to traverse Python code structure
  - [x] 2.2 Implement line counting that excludes docstrings and comments
  - [x] 2.3 Handle nested classes/functions counting toward parent totals
  - [x] 2.4 Write unit tests for various code patterns

  ### Files modified with description of changes

  - `src/linters/length_checker/ast_visitor.py` - Implemented comprehensive AST visitor with CodeElement class to track code structures, including decorator support for accurate line range detection
  - `src/linters/length_checker/line_counter.py` - Implemented sophisticated line counting logic that excludes docstrings, comments, and empty lines while accurately counting actual code lines
  - `src/linters/length_checker/plugin.py` - Enhanced plugin with complete AST analysis integration, configuration management, violation detection, and refactored for reduced complexity
  - `src/tests/linters/length_checker/test_length_checker.py` - Added comprehensive unit tests covering AST parsing, line counting, plugin functionality, edge cases, and various code patterns (21 test methods, all passing)
  - `src/tests/__init__.py` - Created test package initialization file
  - `src/tests/linters/__init__.py` - Created linters test package initialization file  
  - `src/tests/linters/length_checker/__init__.py` - Created length checker test package initialization file

- [ ] 3.0 Implement violation detection and reporting

  - [ ] 3.1 Create violation checker comparing counts to configured limits
  - [ ] 3.2 Implement error formatter with LA101/LA102 codes
  - [ ] 3.3 Integrate with pylama's error reporting mechanism
  - [ ] 3.4 Write tests for error reporting functionality

  ### Files modified with description of changes

  - (to be filled in after task completion)

- [ ] 4.0 Add comprehensive test coverage

  - [ ] 4.1 Test edge cases (empty classes, lambda functions, decorators)
  - [ ] 4.2 Test configuration loading and defaults
  - [ ] 4.3 Test file/directory exclusion patterns
  - [ ] 4.4 Add integration test with pylama CLI

  ### Files modified with description of changes

  - (to be filled in after task completion)

- [ ] 5.0 Documentation and final integration

  - [ ] 5.1 Update README with usage instructions
  - [ ] 5.2 Add example configuration to pyproject.toml
  - [ ] 5.3 Verify plugin works with existing pylama workflow
  - [ ] 5.4 Run final quality checks (format, lint, type check)

  ### Files modified with description of changes

  - (to be filled in after task completion)