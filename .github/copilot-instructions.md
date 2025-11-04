# Copilot Instructions for iracing-client

## Project Overview
This is a Python client library for working with the iRacing Data API. The library provides communication and error handling for the iRacing Data API, allowing developers to interact with iRacing's racing simulation platform programmatically.

## Architecture
- **Authentication**: Uses SHA256 hashing with Base64 encoding for secure password transmission
- **Data Objects**: Abstract base class pattern (`IRacingDataObject`) for different iRacing data categories
- **HTTP Session Management**: Maintains authenticated sessions with automatic token refresh
- **Error Handling**: Custom exceptions for authentication and request failures

### Key Components
- `src/iracing_client/auth.py`: Authentication and login functionality
- `src/iracing_client/data/common.py`: Base classes and common request handling
- `src/iracing_client/data/constants.py`: iRacing constants (categories, divisions, event types)
- `src/iracing_client/data/member.py`: Member profile and data
- `src/iracing_client/data/league.py`: League directory and information

## Development Setup

### Prerequisites
- Python 3.10 or higher
- Poetry for dependency management

### Installation
```bash
poetry install
```

### Environment Variables (for Integration Tests)
Create a `.env` file in the project root:
```bash
IRACING_USERNAME=<your email address>
IRACING_PASSWORD=<your iRacing password>
IRACING_MEMBER_ID=<your iRacing Member Id>
```

## Code Standards

### Formatting
- Use **black** for code formatting (max line length: 88 characters)
- Run: `poetry run black src/`

### Linting
- Use **pylint** for linting (minimum score: 9.0)
- Configuration in `pyproject.toml`: `[tool.pylint.format]`
- Run: `poetry run pylint --fail-under=9 src/`

### Type Hints
- Use type hints for function parameters and return values
- Example: `def login(username: str, password: str) -> requests.Session:`

### Docstrings
- Use triple-quoted docstrings for modules, classes, and functions
- Keep them concise and descriptive

## Testing

### Test-Driven Development (TDD)
- **All new feature development must begin with a failing test**
- Write the test first, then implement the feature to make the test pass
- Follow the Red-Green-Refactor cycle:
  1. **Red**: Write a failing test that defines the desired behavior
  2. **Green**: Write the minimum code to make the test pass
  3. **Refactor**: Improve the code while keeping tests passing

### Unit Tests
- Located in `tests/unit/`
- Mock interactions with iRacing Data API
- Can be executed offline
- Run: `poetry run pytest tests/unit/`

### Integration Tests
- Located in `tests/integration/`
- Connect to live iRacing services
- Require valid credentials in `.env` file
- Run: `poetry run pytest tests/integration/`

### Coverage
- Use pytest-cov for coverage reporting
- Run with coverage: `poetry run pytest --cov=iracing_client --cov-report term tests/`

## Build and CI/CD

### GitHub Actions Workflows
1. **Test Suite** (`.github/workflows/test-suite.yaml`):
   - Runs on: push to main, pull requests
   - Steps: Install dependencies → Lint → Unit tests → Integration tests → SonarCloud scan → CodeCov upload
   - Quality gates: Pylint score ≥ 9.0, SonarCloud quality gate

2. **Release** (`.github/workflows/release.yaml`):
   - Triggered manually or on tags
   - Builds and publishes to PyPI

### Custom Actions
- `.github/actions/poetry-initialize-action`: Sets up Poetry environment with specified Python version

## Common Development Tasks

### Adding New Data Classes
1. Inherit from `IRacingDataObject` in `src/iracing_client/data/common.py`
2. Implement the `clear_cache()` abstract method
3. Add request methods following the pattern in existing classes
4. Use `self.send()` for authenticated requests
5. Handle errors with `IRacingRequestException`

### Making API Requests
- Base URL: `https://members-ng.iracing.com/data/`
- Timeout: 10.0 seconds (defined as `REQUEST_TIMEOUT`)
- Follow the link pattern: Some responses return a `link` field for the actual data

### Error Handling
- `AuthenticationException`: Raised during login failures
- `IRacingRequestException`: Raised for failed API requests
- Always handle timeout and connection errors

## Important Notes

### Security
- Never commit credentials to version control
- Use `.env` file for local development (already in `.gitignore`)
- Password encoding uses SHA256 + Base64 as per iRacing specification

### API Best Practices
- Don't re-authenticate with each request
- Session cookies are automatically refreshed
- Respect the authtoken lifecycle
- Use the existing session for all subsequent requests

### Dependencies
- Core: `requests` for HTTP communication
- Dev: `pytest`, `pytest-cov`, `pylint`, `black`, `coverage`
- Package management: `poetry-core`

## Code Review Checklist
- [ ] New features have tests written first (TDD approach)
- [ ] Code is formatted with black
- [ ] Pylint score is ≥ 9.0
- [ ] Type hints are used appropriately
- [ ] Docstrings are present and clear
- [ ] Unit tests cover new functionality
- [ ] No credentials in code
- [ ] Error handling follows existing patterns
- [ ] Code follows the abstract base class pattern where applicable
