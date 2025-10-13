# Architecture

System architecture documentation for Crawl MCP.

## Overview

Crawl MCP is a microservice architecture built on FastAPI, designed for high-performance web crawling with AI/LLM optimization.

## System Components

### 1. API Layer (`app/api/`)

- **Routes** (`routes.py`): HTTP endpoint handlers
- **Dependencies** (`dependencies.py`): Shared dependencies, middleware
- **Middleware**: Request ID, logging, rate limiting

### 2. Core Layer (`app/core/`)

- **Crawler** (`crawler.py`): Web crawling logic with retry
- **Exceptions** (`exceptions.py`): Custom exception classes

### 3. Utils Layer (`app/utils/`)

- **Validators** (`validators.py`): URL validation
- **Logging** (`logging.py`): Structured logging setup

### 4. Configuration (`app/config.py`)

- Environment-based settings
- Pydantic Settings for validation

### 5. Models (`app/models.py`)

- Pydantic models for request/response validation

## Data Flow

```
Client Request
    ↓
Middleware (Request ID, Logging, Rate Limit)
    ↓
Route Handler
    ↓
Validation (Pydantic)
    ↓
Core Business Logic (Crawler)
    ↓
External Service (crawl4ai)
    ↓
Response Formatting
    ↓
Middleware (Logging)
    ↓
Client Response
```

## Key Design Patterns

### 1. Dependency Injection
FastAPI's dependency injection for shared resources

### 2. Repository Pattern
Separation of data access logic

### 3. Strategy Pattern
Different crawling strategies for different content types

### 4. Async/Await
Asynchronous I/O for high performance

### 5. Middleware Pipeline
Request/response processing chain

## Concurrency Model

- **Async I/O**: AsyncWebCrawler for non-blocking operations
- **Semaphore**: Limit concurrent crawl operations
- **Thread Pool**: For CPU-bound operations (if needed)

## Error Handling

1. **Validation Errors**: Pydantic validation at entry point
2. **Business Errors**: Custom exceptions with status codes
3. **Retry Logic**: Exponential backoff for transient failures
4. **Graceful Degradation**: Return partial results when possible

## Security Considerations

- **Input Validation**: Strict URL validation
- **Rate Limiting**: Per-IP request limiting
- **Domain Blocking**: Configurable blocked domains
- **Timeout Protection**: Prevents resource exhaustion

## Scalability

### Horizontal Scaling
- Stateless design allows multiple instances
- Load balancer distributes requests
- Shared storage for job status (future: Redis)

### Vertical Scaling
- Adjust concurrent crawl limit
- Increase worker processes
- Tune timeout values

## Technology Stack

- **Framework**: FastAPI 0.104+
- **ASGI Server**: Uvicorn
- **Crawler**: Crawl4AI
- **Validation**: Pydantic 2.0+
- **Testing**: Pytest
- **Containerization**: Docker

## Future Enhancements

1. **Message Queue**: Redis/RabbitMQ for job processing
2. **Caching**: Redis for crawl result caching
3. **Database**: PostgreSQL for persistent storage
4. **Authentication**: API key or OAuth2
5. **Monitoring**: Prometheus metrics export

