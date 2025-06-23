# Feature Implementation Plan: Add Warnings to Length Linter

_Generated: 2025-06-22_
_Based on Feature Specification: [20250622-add-warnings-to-length-linter-feature.md](./20250622-add-warnings-to-length-linter-feature.md)_

## Architecture Overview

The length linter currently implements a single-tier violation system where functions/classes exceeding configured limits generate errors (EL001/EL002). This implementation will modify the core plugin logic to support a two-tier system:

- **Warning Tier**: Violations at configured threshold (WL001/WL002)  
- **Error Tier**: Violations at 2x configured threshold (EL001/EL002)

The implementation preserves all existing architecture components (AST visitor, line counter, configuration system) while extending the violation detection and message generation logic.

### System Architecture

```mermaid
graph TD
    A[LengthCheckerPlugin] --> B[LengthCheckerConfig]
    A --> C[ASTVisitor]
    A --> D[LineCounter]
    
    C --> E[CodeElement Detection]
    D --> F[Line Counting]
    
    E --> G[Violation Detection Logic]
    F --> G
    B --> G
    
    G --> H{Length Check}
    H -->|> 2x threshold| I[Create Error EL001/EL002]
    H -->|> 1x threshold| J[Create Warning WL001/WL002]
    H -->|<= threshold| K[No Violation]
    
    I --> L[Flake8 Output]
    J --> L
```

### Data Flow

```mermaid
sequenceDiagram
    participant Plugin as LengthCheckerPlugin
    participant Config as LengthCheckerConfig
    participant Visitor as ASTVisitor
    participant Counter as LineCounter
    participant Check as ViolationChecker
    
    Plugin->>Config: Load thresholds
    Plugin->>Visitor: Find functions/classes
    Plugin->>Counter: Count effective lines
    Plugin->>Check: Check violations(element, lines, config)
    
    Check->>Check: if lines > 2x threshold
    Check-->>Plugin: Error (EL001/EL002)
    Check->>Check: else if lines > 1x threshold  
    Check-->>Plugin: Warning (WL001/WL002)
    Check-->>Plugin: No violation
    
    Plugin->>Plugin: Format message
    Plugin-->>Flake8: Violation tuple (line, col, message, code)
```

## Technology Stack

### Core Technologies
- **Language/Runtime:** Python 3.12
- **Framework:** Flake8 plugin system
- **Configuration:** pyproject.toml with tomllib/tomli parsing

### Libraries & Dependencies
- **AST Processing:** Built-in ast module
- **Configuration:** tomllib (Python 3.11+) / tomli (compatibility)
- **Testing:** pytest with pytest-mock
- **Code Quality:** black, isort, pylama, pyright

### Patterns & Approaches
- **Plugin Pattern:** Flake8 extension interface
- **Visitor Pattern:** AST traversal for code element detection
- **Strategy Pattern:** Line counting with comment/docstring exclusion
- **Configuration Pattern:** Hierarchical config loading (defaults → file → CLI)

### External Integrations
- **Flake8:** Plugin registration and violation reporting
- **Pylama:** Compatible linting pipeline integration
- **Poetry:** Build system and dependency management

## Relevant Files

- `src/linters/length_checker/plugin.py` - Main plugin class requiring two-tier violation logic
- `src/linters/length_checker/config.py` - Configuration system (no changes needed)
- `src/linters/length_checker/ast_visitor.py` - AST visitor (no changes needed)
- `src/linters/length_checker/line_counter.py` - Line counting logic (no changes needed)
- `src/tests/linters/length_checker/test_length_checker.py` - Main test suite requiring warning test coverage
- `pyproject.toml` - Plugin registration and project configuration (no changes needed)

## Implementation Notes

- Tests should be added directly to the existing test file following current patterns
- Use `poetry run pytest` for running tests  
- Run quality tools after each task: `poetry run poe autolint` and `poetry run pyright`
- Warning codes (WL001/WL002) must follow flake8 conventions for compatibility
- Error codes (EL001/EL002) remain unchanged for backward compatibility
- Message format changes apply to both warnings and errors consistently

## Implementation Tasks

- [ ] 1.0 Update Plugin Violation Detection Logic

  - [ ] 1.1 Modify `_check_element_violations` method to implement two-tier threshold checking
  - [ ] 1.2 Update method to generate both warnings and errors based on length thresholds
  - [ ] 1.3 Ensure violations are yielded in correct order (warnings before errors for same element)
  - [ ] 1.4 Test the updated violation detection logic with existing test helper functions

  ### Files modified with description of changes

  - (to be filled in after task completion)

- [ ] 2.0 Update Message Generation Methods

  - [ ] 2.1 Update `_create_function_violation` method to use new message format with threshold type
  - [ ] 2.2 Update `_create_class_violation` method to use new message format with threshold type
  - [ ] 2.3 Add new `_create_function_warning` method for WL001 warning generation
  - [ ] 2.4 Add new `_create_class_warning` method for WL002 warning generation
  - [ ] 2.5 Ensure all messages include "recommend refactoring" as specified in requirements

  ### Files modified with description of changes

  - (to be filled in after task completion)

- [ ] 3.0 Add Comprehensive Test Coverage

  - [ ] 3.1 Add tests for warning generation at 1x threshold for functions and classes
  - [ ] 3.2 Add tests for error generation at 2x threshold for functions and classes  
  - [ ] 3.3 Add tests for no violations when under 1x threshold
  - [ ] 3.4 Add tests for correct message format including all required elements
  - [ ] 3.5 Add tests for warning codes WL001 and WL002 generation
  - [ ] 3.6 Add tests for mixed scenarios (warnings and errors in same file)
  - [ ] 3.7 Add tests ensuring existing functionality remains unchanged
  - [ ] 3.8 Add edge case tests (exactly at thresholds, exactly at 2x thresholds)

  ### Files modified with description of changes

  - (to be filled in after task completion)

- [ ] 4.0 Quality Verification and Integration Testing

  - [ ] 4.1 Run all existing tests to ensure no regressions
  - [ ] 4.2 Run code formatting tools (black, isort) and fix any issues
  - [ ] 4.3 Run linting (pylama) and address any violations  
  - [ ] 4.4 Run type checking (pyright) and fix any type issues
  - [ ] 4.5 Test flake8 integration manually with sample code files
  - [ ] 4.6 Verify configuration compatibility with existing pyproject.toml settings
  - [ ] 4.7 Test command-line option compatibility (--length-max-function, --length-max-class)

  ### Files modified with description of changes

  - (to be filled in after task completion)