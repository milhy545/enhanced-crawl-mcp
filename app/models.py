"""
Pydantic models for API requests and responses.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JobStatus(str, Enum):
    """Job status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CrawlRequest(BaseModel):
    """Request model for single URL crawling."""

    url: str = Field(..., description="URL to crawl", min_length=1)
    include_links: bool = Field(default=False, description="Include extracted links in response")
    include_images: bool = Field(default=False, description="Include extracted images in response")
    max_depth: int = Field(default=1, description="Maximum crawl depth", ge=1, le=5)
    timeout: int | None = Field(default=None, description="Custom timeout in seconds", ge=5, le=300)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Basic URL validation."""
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty")
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://example.com",
                "include_links": True,
                "include_images": False,
                "max_depth": 1,
                "timeout": 30,
            }
        }
    )


class BatchCrawlRequest(BaseModel):
    """Request model for batch URL crawling."""

    urls: list[str] = Field(..., description="List of URLs to crawl", min_length=1, max_length=100)
    include_links: bool = Field(default=False, description="Include extracted links in response")
    include_images: bool = Field(default=False, description="Include extracted images in response")
    timeout: int | None = Field(
        default=None, description="Custom timeout in seconds per URL", ge=5, le=300
    )

    @field_validator("urls")
    @classmethod
    def validate_urls(cls, v: list[str]) -> list[str]:
        """Validate all URLs."""
        validated_urls = []
        for url in v:
            url = url.strip()
            if not url:
                continue
            if not url.startswith(("http://", "https://")):
                raise ValueError(f"URL must start with http:// or https://: {url}")
            validated_urls.append(url)

        if not validated_urls:
            raise ValueError("At least one valid URL is required")

        return validated_urls

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "urls": ["https://example.com", "https://example.org"],
                "include_links": True,
                "include_images": False,
                "timeout": 30,
            }
        }
    )


class URLValidationRequest(BaseModel):
    """Request model for URL validation."""

    url: str = Field(..., description="URL to validate", min_length=1)

    model_config = ConfigDict(json_schema_extra={"example": {"url": "https://example.com"}})


class CrawlResponse(BaseModel):
    """Response model for crawl operations."""

    status: str = Field(..., description="Operation status")
    url: str = Field(..., description="Crawled URL")
    markdown: str = Field(..., description="Extracted markdown content")
    links: list[str] | None = Field(default=None, description="Extracted links")
    images: list[str] | None = Field(default=None, description="Extracted image URLs")
    metadata: dict[str, Any] | None = Field(default=None, description="Additional metadata")
    crawled_at: datetime = Field(default_factory=datetime.utcnow, description="Crawl timestamp")

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()},
        json_schema_extra={
            "example": {
                "status": "success",
                "url": "https://example.com",
                "markdown": "# Example Domain\n\nThis domain is for use in...",
                "links": ["https://example.com/about"],
                "images": ["https://example.com/logo.png"],
                "metadata": {"title": "Example Domain"},
                "crawled_at": "2024-01-01T12:00:00",
            }
        },
    )


class BatchCrawlResponse(BaseModel):
    """Response model for batch crawl operations."""

    job_id: str = Field(..., description="Batch job identifier")
    status: JobStatus = Field(..., description="Job status")
    total_urls: int = Field(..., description="Total number of URLs")
    completed: int = Field(default=0, description="Number of completed crawls")
    failed: int = Field(default=0, description="Number of failed crawls")
    results: list[CrawlResponse] | None = Field(
        default=None, description="Crawl results if completed"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_id": "batch_123456",
                "status": "in_progress",
                "total_urls": 10,
                "completed": 5,
                "failed": 0,
                "results": None,
            }
        }
    )


class JobStatusResponse(BaseModel):
    """Response model for job status queries."""

    job_id: str = Field(..., description="Job identifier")
    status: JobStatus = Field(..., description="Current job status")
    created_at: datetime = Field(..., description="Job creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    total_urls: int = Field(..., description="Total number of URLs")
    completed: int = Field(..., description="Number of completed URLs")
    failed: int = Field(..., description="Number of failed URLs")
    progress: float = Field(..., description="Progress percentage", ge=0.0, le=100.0)
    error_message: str | None = Field(default=None, description="Error message if failed")

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()},
        json_schema_extra={
            "example": {
                "job_id": "batch_123456",
                "status": "in_progress",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:05:00",
                "total_urls": 10,
                "completed": 7,
                "failed": 1,
                "progress": 70.0,
                "error_message": None,
            }
        },
    )


class URLValidationResponse(BaseModel):
    """Response model for URL validation."""

    url: str = Field(..., description="Validated URL")
    is_valid: bool = Field(..., description="Whether URL is valid")
    scheme: str | None = Field(default=None, description="URL scheme")
    domain: str | None = Field(default=None, description="URL domain")
    is_blocked: bool = Field(default=False, description="Whether domain is blocked")
    error_message: str | None = Field(default=None, description="Validation error message")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://example.com",
                "is_valid": True,
                "scheme": "https",
                "domain": "example.com",
                "is_blocked": False,
                "error_message": None,
            }
        }
    )


class ServerStatsResponse(BaseModel):
    """Response model for server statistics."""

    uptime_seconds: float = Field(..., description="Server uptime in seconds")
    total_requests: int = Field(..., description="Total number of requests processed")
    successful_crawls: int = Field(..., description="Number of successful crawls")
    failed_crawls: int = Field(..., description="Number of failed crawls")
    active_jobs: int = Field(..., description="Number of active jobs")
    avg_response_time: float = Field(..., description="Average response time in seconds")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "uptime_seconds": 86400.5,
                "total_requests": 1500,
                "successful_crawls": 1400,
                "failed_crawls": 100,
                "active_jobs": 5,
                "avg_response_time": 2.5,
            }
        }
    )


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: dict[str, Any] | None = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()},
        json_schema_extra={
            "example": {
                "error": "ValidationError",
                "message": "Invalid URL format",
                "details": {"url": "invalid-url", "reason": "Missing scheme"},
                "timestamp": "2024-01-01T12:00:00",
            }
        },
    )


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(default="ok", description="Health status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()},
        json_schema_extra={
            "example": {"status": "ok", "version": "1.0.0", "timestamp": "2024-01-01T12:00:00"}
        },
    )
