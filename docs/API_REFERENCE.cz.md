# API Reference

Complete API documentation for Crawl MCP.

## Base URL

```
http://localhost:8012/api/v1
```

## Authentication

Currently, the API does not require authentication. For production deployments, consider adding API key authentication or OAuth2.

## Rate Limiting

- Default: 100 requests per minute per IP
- Configurable via `CRAWL_MCP_RATE_LIMIT_REQUESTS`
- When exceeded: HTTP 429 (Too Many Requests)

## Common Headers

### Request Headers
```
Content-Type: application/json
```

### Response Headers
```
Content-Type: application/json
X-Request-ID: <unique-request-id>
```

## Endpoints

### Health Check

#### `GET /health`

Check if the service is running.

**Response: 200 OK**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### Server Statistics

#### `GET /stats`

Get server statistics and metrics.

**Response: 200 OK**
```json
{
  "uptime_seconds": 86400.5,
  "total_requests": 1500,
  "successful_crawls": 1400,
  "failed_crawls": 100,
  "active_jobs": 5,
  "avg_response_time": 2.5
}
```

---

### Single URL Crawl

#### `POST /crawl`

Crawl a single URL and return markdown content.

**Request Body**
```json
{
  "url": "https://example.com",
  "include_links": false,
  "include_images": false,
  "max_depth": 1,
  "timeout": 30
}
```

**Parameters**
- `url` (string, required): URL to crawl
- `include_links` (boolean, optional): Include extracted links. Default: `false`
- `include_images` (boolean, optional): Include extracted images. Default: `false`
- `max_depth` (integer, optional): Maximum crawl depth (1-5). Default: `1`
- `timeout` (integer, optional): Custom timeout in seconds (5-300). Default: `30`

**Response: 200 OK**
```json
{
  "status": "success",
  "url": "https://example.com",
  "markdown": "# Example Domain\n\nThis domain is for use in...",
  "links": ["https://example.com/about"],
  "images": ["https://example.com/logo.png"],
  "metadata": {
    "title": "Example Domain",
    "description": "Example domain for documentation"
  },
  "crawled_at": "2024-01-01T12:00:00"
}
```

**Error Responses**

- `400 Bad Request`: Invalid URL or parameters
- `422 Validation Error`: Request validation failed
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Crawl failed

---

### Batch URL Crawl

#### `POST /crawl/batch`

Crawl multiple URLs concurrently.

**Request Body**
```json
{
  "urls": [
    "https://example.com",
    "https://example.org"
  ],
  "include_links": false,
  "include_images": false,
  "timeout": 30
}
```

**Parameters**
- `urls` (array[string], required): List of URLs to crawl (1-100 URLs)
- `include_links` (boolean, optional): Include extracted links. Default: `false`
- `include_images` (boolean, optional): Include extracted images. Default: `false`
- `timeout` (integer, optional): Timeout per URL in seconds (5-300). Default: `30`

**Response: 200 OK**
```json
{
  "job_id": "batch_abc123def456",
  "status": "completed",
  "total_urls": 2,
  "completed": 2,
  "failed": 0,
  "results": [
    {
      "status": "success",
      "url": "https://example.com",
      "markdown": "# Example Domain...",
      "links": null,
      "images": null,
      "metadata": {},
      "crawled_at": "2024-01-01T12:00:00"
    },
    {
      "status": "success",
      "url": "https://example.org",
      "markdown": "# Example Organization...",
      "links": null,
      "images": null,
      "metadata": {},
      "crawled_at": "2024-01-01T12:00:01"
    }
  ]
}
```

---

### Check Job Status

#### `GET /crawl/status/{job_id}`

Get the status of a batch crawl job.

**Path Parameters**
- `job_id` (string, required): Job identifier from batch crawl

**Response: 200 OK**
```json
{
  "job_id": "batch_abc123def456",
  "status": "in_progress",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:05:00",
  "total_urls": 10,
  "completed": 7,
  "failed": 1,
  "progress": 70.0,
  "error_message": null
}
```

**Job Statuses**
- `pending`: Job is queued
- `in_progress`: Job is being processed
- `completed`: Job finished successfully
- `failed`: Job failed
- `cancelled`: Job was cancelled

**Error Responses**

- `404 Not Found`: Job ID not found

---

### Validate URL

#### `POST /crawl/validate`

Validate a URL before crawling.

**Request Body**
```json
{
  "url": "https://example.com"
}
```

**Response: 200 OK (Valid URL)**
```json
{
  "url": "https://example.com",
  "is_valid": true,
  "scheme": "https",
  "domain": "example.com",
  "is_blocked": false,
  "error_message": null
}
```

**Response: 200 OK (Invalid URL)**
```json
{
  "url": "ftp://example.com",
  "is_valid": false,
  "scheme": null,
  "domain": null,
  "is_blocked": false,
  "error_message": "Scheme 'ftp' not allowed. Allowed schemes: http, https"
}
```

**Response: 200 OK (Blocked Domain)**
```json
{
  "url": "https://blocked.com",
  "is_valid": false,
  "scheme": "https",
  "domain": "blocked.com",
  "is_blocked": true,
  "error_message": "Domain blocked.com is blocked from crawling"
}
```

---

## Error Responses

All error responses follow this structure:

```json
{
  "error": "ErrorType",
  "message": "Human readable error message",
  "details": {
    "field": "additional context"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Common Error Types

- `ValidationError`: Input validation failed
- `URLValidationError`: URL format is invalid
- `BlockedDomainError`: Domain is blocked
- `CrawlTimeoutError`: Crawl operation timed out
- `RateLimitError`: Rate limit exceeded
- `JobNotFoundError`: Job ID not found
- `InternalServerError`: Unexpected server error

## Examples

### Python

```python
import requests

# Single crawl
response = requests.post(
    "http://localhost:8012/api/v1/crawl",
    json={
        "url": "https://example.com",
        "include_links": True
    }
)
data = response.json()
print(data["markdown"])

# Batch crawl
response = requests.post(
    "http://localhost:8012/api/v1/crawl/batch",
    json={
        "urls": [
            "https://example.com",
            "https://example.org"
        ]
    }
)
job = response.json()
job_id = job["job_id"]

# Check status
response = requests.get(
    f"http://localhost:8012/api/v1/crawl/status/{job_id}"
)
status = response.json()
print(f"Progress: {status['progress']}%")
```

### JavaScript/TypeScript

```javascript
// Single crawl
const response = await fetch('http://localhost:8012/api/v1/crawl', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://example.com',
    include_links: true
  })
});
const data = await response.json();
console.log(data.markdown);

// Batch crawl
const batchResponse = await fetch('http://localhost:8012/api/v1/crawl/batch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    urls: ['https://example.com', 'https://example.org']
  })
});
const job = await batchResponse.json();

// Check status
const statusResponse = await fetch(
  `http://localhost:8012/api/v1/crawl/status/${job.job_id}`
);
const status = await statusResponse.json();
console.log(`Progress: ${status.progress}%`);
```

### cURL

```bash
# Single crawl
curl -X POST http://localhost:8012/api/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","include_links":true}'

# Batch crawl
curl -X POST http://localhost:8012/api/v1/crawl/batch \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://example.com","https://example.org"]}'

# Check status
curl http://localhost:8012/api/v1/crawl/status/batch_abc123
```

## Versioning

The API uses URL versioning. Current version: `v1`

Future versions will be available at `/api/v2`, `/api/v3`, etc.

## Best Practices

1. **Always validate URLs** before crawling to avoid unnecessary errors
2. **Use batch crawling** for multiple URLs to improve performance
3. **Implement retry logic** on the client side for failed requests
4. **Monitor rate limits** and implement backoff strategies
5. **Store job IDs** for batch operations to check status later
6. **Set appropriate timeouts** based on expected page load times
7. **Handle errors gracefully** and log error details for debugging

