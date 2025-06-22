# Feature Implementation Plan: Convert Length Linter from Pylama to Flake8 Plugin

_Generated: 2025-06-22_
_Based on Feature Specification: [./20250622-convert-length-linter-pylama-to-flake8-feature.md](./20250622-convert-length-linter-pylama-to-flake8-feature.md)_

## Architecture Overview

The implementation will convert the existing pylama-based length linter to a flake8 plugin while preserving all current functionality. The core architecture involves changing only the plugin interface layer while maintaining the existing AST visitor, line counter, and configuration modules.

### System Architecture

```mermaid
graph TD
    A[flake8 Command] --> B[Plugin Discovery]
    B --> C[Length Checker Plugin]
    C --> D[Configuration Loader]
    C --> E[AST Visitor]
    E --> F[Line Counter]
    F --> G[Error Reporter]
    G --> H[flake8 Output]
    
    D --> I[pyproject.toml]
    I --> J[tool.pyla-linters]
    
    subgraph "Preserved Modules"
        D
        E
        F
    end
    
    subgraph "Modified Module"
        C
        G
    end
```

### Plugin Integration Flow

```mermaid
sequenceDiagram
    participant F as flake8
    participant P as LengthChecker Plugin
    participant C as Configuration
    participant A as AST Visitor
    participant L as Line Counter
    
    F->>P: run(lines)
    P->>C: load_config()
    C->>P: return config
    P->>A: visit_tree(ast)
    A->>L: count_lines(element)
    L->>A: return line_count
    A->>P: return violations
    P->>F: yield (line, col, msg, type)
```

## Technology Stack

### Core Technologies

- **Language/Runtime:** Python 3.12
- **Plugin Framework:** flake8 plugin architecture
- **AST Processing:** Python built-in `ast` module
- **Configuration:** pyproject.toml via `tomli` library
- **Dependency Management:** Poetry

### Libraries & Dependencies

- **Runtime Dependencies:**
  - `flake8 >= 3.8.0` (new requirement)
  - `pyla-logger ^1.0.0` (preserved)
  - `tomli` (for pyproject.toml parsing)
- **Development Dependencies:**
  - `pytest` (testing framework)
  - `pytest-mock` (test mocking)
  - `black` (code formatting)
  - `isort` (import sorting)
  - `pyright` (type checking)

### Patterns & Approaches

- **Architectural Patterns:** Plugin architecture with dependency injection
- **Design Patterns:** Visitor pattern for AST traversal, Strategy pattern for line counting
- **Development Practices:** Test-driven development, configuration-driven behavior
- **Plugin Interface:** flake8 checker protocol implementation

### External Integrations

- **flake8 Framework:** Plugin discovery and execution
- **pyproject.toml:** Configuration file parsing
- **AST Module:** Python source code analysis

## Relevant Files

- `src/linters/length_checker/plugin.py` - Main plugin implementation (major changes)
- `src/linters/length_checker/ast_visitor.py` - AST visitor (minimal changes)
- `src/linters/length_checker/line_counter.py` - Line counting logic (no changes)
- `src/linters/length_checker/config.py` - Configuration management (no changes)
- `src/linters/length_checker/__init__.py` - Package exports (minor changes)
- `pyproject.toml` - Project configuration and entry points (changes required)
- `src/tests/linters/length_checker/test_length_checker.py` - Test suite (major changes)

## Implementation Notes

- Tests should be adapted to work with flake8 plugin testing patterns using pytest
- Use `poetry run pytest` to run the test suite
- Follow existing project file naming and directory structure conventions
- After completing each subtask, run formatting and linting tools: `poetry run poe format` and `poetry run poe lint`
- Run type checking with `poetry run pyright` after code changes
- After completing a parent task, stop and wait for user confirmation before proceeding

## Implementation Tasks

- [x] 1.0 Research and Setup flake8 Plugin Architecture

  - [x] 1.1 Research flake8 plugin development patterns and best practices
  - [x] 1.2 Update pyproject.toml to add flake8 dependency and configure entry points
  - [x] 1.3 Create basic flake8 plugin structure and verify plugin discovery
  - [x] 1.4 Run initial integration test to ensure flake8 can discover the plugin

  ### Files modified with description of changes

  - `pyproject.toml` - Added flake8 ^7.0.0 and tomli ^2.0.0 dependencies, replaced pylama entry point with flake8.extension entry point (EL1)
  - `src/linters/length_checker/plugin.py` - Converted from pylama interface to flake8 interface: updated constructor to accept AST tree and filename, replaced run() method to yield flake8 error tuples, changed error codes from LA101/LA102 to EL001/EL002, updated option handling methods
  - `poetry.lock` - Updated lock file with new dependencies

- [ ] 2.0 Convert Plugin Interface from Pylama to Flake8

  - [ ] 2.1 Modify plugin.py to implement flake8 checker interface instead of pylama
  - [ ] 2.2 Update error reporting to use flake8 error tuple format (line, col, message, type)
  - [ ] 2.3 Change error codes from LA101/LA102 to EL001/EL002 format
  - [ ] 2.4 Ensure plugin integrates with flake8's file processing workflow
  - [ ] 2.5 Write and run tests for the new plugin interface

  ### Files modified with description of changes

  - (to be filled in after task completion)

- [ ] 3.0 Validate Configuration and Core Functionality

  - [ ] 3.1 Verify configuration loading from [tool.pyla-linters] section works correctly
  - [ ] 3.2 Test AST visitor and line counter modules work with new plugin interface
  - [ ] 3.3 Validate function and class length checking produces identical results
  - [ ] 3.4 Ensure decorator handling and nested element support is preserved
  - [ ] 3.5 Write integration tests for end-to-end functionality

  ### Files modified with description of changes

  - (to be filled in after task completion)

- [ ] 4.0 Migrate and Adapt Test Suite

  - [ ] 4.1 Update test mocks and fixtures for flake8 plugin testing patterns
  - [ ] 4.2 Adapt existing test cases to work with flake8 error format
  - [ ] 4.3 Update test assertions to validate EL001/EL002 error codes
  - [ ] 4.4 Ensure all 75 existing tests pass with identical behavior
  - [ ] 4.5 Add new tests for flake8-specific integration scenarios
  - [ ] 4.6 Run full test suite and fix any failing tests

  ### Files modified with description of changes

  - (to be filled in after task completion)

- [ ] 5.0 Final Integration and Cleanup

  - [ ] 5.1 Remove pylama-related dependencies and configurations
  - [ ] 5.2 Update package exports and entry points for flake8 plugin
  - [ ] 5.3 Run comprehensive integration tests with real flake8 command
  - [ ] 5.4 Verify plugin works correctly with standard flake8 CLI options
  - [ ] 5.5 Run all quality checks (formatting, linting, type checking, tests)
  - [ ] 5.6 Create simple usage example to demonstrate flake8 integration

  ### Files modified with description of changes

  - (to be filled in after task completion)