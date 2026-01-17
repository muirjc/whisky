<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (MAJOR: Initial constitution ratification)

Modified principles: N/A (initial version)

Added sections:
- Core Principles (5 principles)
- Development Standards
- Quality Gates
- Governance

Removed sections: N/A (initial version)

Templates requiring updates:
- .specify/templates/plan-template.md: ✅ Compatible (Constitution Check section exists)
- .specify/templates/spec-template.md: ✅ Compatible (requirements align)
- .specify/templates/tasks-template.md: ✅ Compatible (phase structure supports TDD)

Follow-up TODOs: None
-->

# Whisky Constitution

## Core Principles

### I. API-First Design

All features MUST be designed as APIs before any UI implementation begins. This ensures:
- Clear separation between business logic and presentation
- Every endpoint is documented with OpenAPI/Swagger specifications
- Backend and frontend can be developed and tested independently
- Third-party integrations are possible from day one

**Rationale**: API-first prevents coupling between UI and business logic, enables
parallel development, and ensures the system is extensible.

### II. Test-Driven Development (NON-NEGOTIABLE)

All new functionality MUST follow the TDD cycle:
1. Write failing tests that define expected behavior
2. Implement minimum code to pass tests
3. Refactor while keeping tests green

Requirements:
- Unit test coverage MUST exceed 80% for new code
- Integration tests MUST cover all API endpoints
- Contract tests MUST validate external service interactions
- No PR may be merged with failing tests

**Rationale**: TDD ensures correctness, provides living documentation, and enables
safe refactoring. Skipping tests creates technical debt that compounds over time.

### III. Type Safety

All Python code MUST use type hints and pass strict type checking:
- All function signatures MUST include type annotations
- mypy (or equivalent) MUST pass with strict mode enabled
- Pydantic models MUST be used for data validation at boundaries
- No use of `Any` type without explicit justification in comments

**Rationale**: Type safety catches errors at development time, improves IDE support,
and serves as inline documentation for expected data shapes.

### IV. Security by Default

Security MUST be built into every feature, not added as an afterthought:
- All user input MUST be validated and sanitized
- Authentication and authorization MUST be enforced on all protected endpoints
- Secrets MUST never be committed to version control
- Dependencies MUST be regularly audited for vulnerabilities
- OWASP Top 10 vulnerabilities MUST be addressed in code review

**Rationale**: Security breaches are costly and damage trust. Building security
into the development process is cheaper than retrofitting it later.

### V. Observability

All production code MUST be observable:
- Structured logging MUST be used (JSON format) with correlation IDs
- Key operations MUST emit metrics (latency, error rates, throughput)
- Errors MUST include sufficient context for debugging without reproducing
- Health check endpoints MUST be implemented for all services

**Rationale**: Systems that cannot be observed cannot be effectively maintained.
Observability enables rapid incident response and informed capacity planning.

## Development Standards

### Code Organization

- Backend follows a layered architecture: `api/` → `services/` → `models/`
- Frontend components are organized by feature, not by type
- Shared code lives in clearly marked `shared/` or `common/` directories
- Configuration is externalized via environment variables

### Dependency Management

- All dependencies MUST be pinned to specific versions
- Dependency updates MUST be reviewed for breaking changes
- Security patches MUST be applied within 48 hours of disclosure
- No dependencies with known critical vulnerabilities may be added

### Documentation

- All public APIs MUST have docstrings
- README MUST include setup instructions that work on a fresh machine
- Architecture decisions MUST be recorded in ADRs (Architecture Decision Records)
- Runbooks MUST exist for all production operations

## Quality Gates

All code changes MUST pass these gates before merging:

| Gate | Requirement | Enforcement |
|------|-------------|-------------|
| Tests | All tests pass | CI pipeline |
| Coverage | ≥80% on changed files | CI pipeline |
| Type Check | mypy strict passes | CI pipeline |
| Lint | No errors (ruff/flake8) | CI pipeline |
| Security | No critical vulnerabilities | Dependency scan |
| Review | At least 1 approval | Branch protection |

## Governance

### Amendment Process

1. Propose amendment via pull request to this file
2. Document rationale and impact on existing code
3. Obtain approval from project maintainers
4. Update dependent templates if principles change
5. Communicate changes to all contributors

### Versioning Policy

This constitution follows semantic versioning:
- **MAJOR**: Removal or redefinition of principles (breaking change)
- **MINOR**: Addition of new principles or significant guidance expansion
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

### Compliance

- All pull requests MUST be reviewed for constitution compliance
- Code review checklists MUST reference applicable principles
- Violations MUST be documented and remediated before merge
- Exceptions require explicit justification and maintainer approval

**Version**: 1.0.0 | **Ratified**: 2026-01-17 | **Last Amended**: 2026-01-17
