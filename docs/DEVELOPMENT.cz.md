# Development Guide

Guide for developers contributing to Crawl MCP.

## Setup

```bash
git clone <repository-url>
cd crawl-mcp
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Project Structure

```
crawl-mcp/
├── app/              # Application code
│   ├── api/         # API routes
│   ├── core/        # Business logic
│   ├── utils/       # Utilities
│   └── main.py      # FastAPI app
├── tests/           # Test suite
└── docs/            # Documentation
```

## Code Style

- **Python**: PEP 8
- **Line length**: 100 characters
- **Formatter**: Black
- **Import sorting**: isort
- **Linter**: Ruff
- **Type checking**: MyPy

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific tests
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Watch mode
pytest-watch
```

## Pre-commit Hooks

Automatically run before each commit:

- trailing whitespace removal
- end-of-file fixing
- YAML/JSON validation
- Black formatting
- isort import sorting
- Ruff linting
- MyPy type checking

```bash
# Run manually
pre-commit run --all-files
```

## Development Workflow

1. Create feature branch
2. Write code and tests
3. Run tests locally
4. Commit (pre-commit hooks run)
5. Push and create PR
6. CI runs (tests, linting, security)
7. Review and merge

## Adding New Features

### 1. Create models (if needed)
```python
# app/models.py
class NewRequest(BaseModel):
    field: str
```

### 2. Add route
```python
# app/api/routes.py
@router.post("/new-endpoint")
async def new_endpoint(request: NewRequest):
    ...
```

### 3. Write tests
```python
# tests/unit/test_new_feature.py
def test_new_feature():
    ...
```

### 4. Update documentation
- Add to API_REFERENCE.md
- Update README.md if needed

## Debugging

```bash
# Run with debug logging
CRAWL_MCP_LOG_LEVEL=DEBUG python -m uvicorn app.main:app --reload

# Python debugger
import pdb; pdb.set_trace()

# Or use breakpoint()
breakpoint()
```

## Common Tasks

### Add dependency
```bash
pip install <package>
pip freeze > requirements.txt
```

### Run linting
```bash
ruff check app/
black --check app/
isort --check app/
mypy app/
```

### Format code
```bash
black app/ tests/
isort app/ tests/
```

### Security audit
```bash
bandit -r app/
safety check
```

