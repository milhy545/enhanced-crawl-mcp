# Changelog

All notable changes to the Crawl MCP project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added
- Initial release of Crawl MCP microservice
- FastAPI-based REST API for web crawling
- Single URL crawling with markdown conversion
- Batch URL crawling with concurrent processing
- Link and image extraction capabilities
- Automatic retry logic with exponential backoff
- Job status tracking for batch operations
- URL validation endpoint
- Server statistics endpoint
- Configurable environment-based settings
- Docker and Docker Compose support
- Comprehensive test suite (80%+ coverage)
- Complete API documentation (Swagger/ReDoc)
- Deployment guides and documentation
- Czech and English documentation
- Pre-commit hooks and CI/CD workflows
- Security features (rate limiting, domain blocking)
- Structured logging (JSON/text formats)
- Request ID tracking
- CORS support
- Pydantic V2 models with validation

### Core Features
- **API Endpoints**:
  - `POST /api/v1/crawl` - Single URL crawling
  - `POST /api/v1/crawl/batch` - Batch URL crawling
  - `GET /api/v1/crawl/status/{job_id}` - Job status check
  - `POST /api/v1/crawl/validate` - URL validation
  - `GET /api/v1/stats` - Server statistics
  - `GET /health` - Health check
  
- **Configuration Options**:
  - Configurable timeouts and retry attempts
  - Rate limiting (requests per minute)
  - Domain blocking
  - CORS origins
  - Concurrent crawl limits
  - Logging levels and formats

- **Developer Tools**:
  - pytest test suite
  - Black code formatting
  - isort import sorting
  - Ruff linting
  - MyPy type checking
  - Pre-commit hooks
  - GitHub Actions CI/CD

### Documentation
- README.md (EN) - Quick start and overview
- README.cz.md (CZ) - Czech version
- API_REFERENCE.md - Complete API documentation
- DEPLOYMENT.md - Production deployment guide
- DEVELOPMENT.md - Developer guide
- ARCHITECTURE.md - System architecture
- Czech versions of all documentation

### Infrastructure
- Docker containerization
- Docker Compose configuration
- GitHub Actions workflows for testing and deployment
- Multi-stage Docker builds
- Health checks and monitoring support

### Security
- Input validation and sanitization
- URL scheme validation (http/https only)
- Domain blocking mechanism
- Rate limiting per IP
- Request timeout protection
- Structured error responses

### Testing
- Unit tests for all modules
- Integration tests for API endpoints
- End-to-end workflow tests
- Edge case and stress tests
- 80%+ code coverage
- Mocked external dependencies

## [Unreleased]

### Planned
- Redis integration for job queue
- PostgreSQL for persistent storage
- API key authentication
- Webhook notifications for batch jobs
- Result caching
- Prometheus metrics export
- Enhanced monitoring and alerting
- GraphQL API support
- WebSocket support for real-time updates

---

## Version History

- **1.0.0** (2024-01-01) - Initial stable release

