# Crawl MCP

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance FastAPI-based microservice for web crawling optimized for AI and LLM consumption. Converts web pages into clean, structured Markdown perfect for RAG systems, AI agents, and data pipelines.

## Features

✨ **Core Capabilities**
- 🌐 Single URL crawling with markdown conversion
- 📦 Batch URL crawling with concurrent processing
- 🔗 Link and image extraction
- ⚡ Async/await architecture for high performance
- 🔄 Automatic retry logic with exponential backoff
- 📊 Real-time job status tracking

🛡️ **Reliability & Security**
- ⏱️ Configurable timeouts and rate limiting
- 🚫 Domain blocking and URL validation
- 🔒 Scheme validation (http/https only)
- 📝 Structured logging (JSON/text formats)
- 🎯 Request ID tracking

🚀 **Developer Experience**
- 📖 Auto-generated OpenAPI documentation
- 🐳 Docker & Docker Compose support
- 🧪 Comprehensive test suite (80%+ coverage)
- 🔧 Environment-based configuration
- 🎨 Pre-commit hooks and code quality tools

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip and virtualenv

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd crawl-mcp
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional)**
```bash
cp .env.example .env
# Edit .env with your preferences
```

5. **Run the server**
```bash
# Option 1: Direct
python -m uvicorn app.main:app --host 0.0.0.0 --port 8012

# Option 2: Using script
./run_crawler.sh

# Option 3: Using tmux (recommended for persistent sessions)
./start_crawl_mcp_tmux.sh
```

The API will be available at `http://localhost:8012`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t crawl-mcp .
docker run -p 8012:8012 crawl-mcp
```

## Usage

### Basic Crawl

```bash
curl -X POST http://localhost:8012/api/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Advanced Crawl with Options

```bash
curl -X POST http://localhost:8012/api/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "include_links": true,
    "include_images": true,
    "timeout": 30
  }'
```

### Batch Crawling

```bash
curl -X POST http://localhost:8012/api/v1/crawl/batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example.com",
      "https://example.org"
    ],
    "include_links": true
  }'
```

### Check Job Status

```bash
curl http://localhost:8012/api/v1/crawl/status/{job_id}
```

### Validate URL

```bash
curl -X POST http://localhost:8012/api/v1/crawl/validate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Server Statistics

```bash
curl http://localhost:8012/api/v1/stats
```

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8012/docs`
- **ReDoc**: `http://localhost:8012/redoc`
- **OpenAPI JSON**: `http://localhost:8012/openapi.json`

For detailed API reference, see [API_REFERENCE.md](API_REFERENCE.md)

## Configuration

The application can be configured via environment variables. See `.env.example` for all available options.

### Key Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `CRAWL_MCP_HOST` | `0.0.0.0` | Server host |
| `CRAWL_MCP_PORT` | `8012` | Server port |
| `CRAWL_MCP_LOG_LEVEL` | `INFO` | Logging level |
| `CRAWL_MCP_CRAWLER_TIMEOUT` | `30` | Crawler timeout (seconds) |
| `CRAWL_MCP_CRAWLER_MAX_RETRIES` | `3` | Maximum retry attempts |
| `CRAWL_MCP_RATE_LIMIT_REQUESTS` | `100` | Requests per minute limit |
| `CRAWL_MCP_BLOCKED_DOMAINS` | `` | Comma-separated blocked domains |

## Development

### Setup Development Environment

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code
black app/ tests/
isort app/ tests/

# Lint
ruff check app/
mypy app/
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# E2E tests
pytest tests/e2e/

# With coverage report
pytest --cov=app --cov-report=term-missing
```

## Project Structure

```
crawl-mcp/
├── app/                    # Application code
│   ├── api/               # API routes and dependencies
│   ├── core/              # Core business logic
│   ├── utils/             # Utilities (logging, validators)
│   ├── config.py          # Configuration
│   ├── models.py          # Pydantic models
│   └── main.py            # FastAPI app
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── .github/workflows/     # CI/CD workflows
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose config
├── pyproject.toml         # Project metadata
└── requirements.txt       # Python dependencies
```

## Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md)

## Deployment

For production deployment guide, see [DEPLOYMENT.md](DEPLOYMENT.md)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Crawl4AI](https://github.com/unclecode/crawl4ai)
- Inspired by the need for AI-friendly web content extraction

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/crawl-mcp/issues)
- 💬 [Discussions](https://github.com/yourusername/crawl-mcp/discussions)

---

Made with ❤️ for the AI/LLM community

