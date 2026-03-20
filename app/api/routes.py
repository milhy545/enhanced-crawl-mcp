"""
API route handlers.
"""

import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request

from app import __version__
from app.api.dependencies import (
    get_job,
    get_stats,
    increment_crawl_failure,
    increment_crawl_success,
    store_job,
    update_job,
)
from app.core.crawler import WebCrawler
from app.core.exceptions import (
    BlockedDomainError,
    CrawlMCPException,
    JobNotFoundError,
    URLValidationError,
)
from app.models import (
    BatchCrawlRequest,
    BatchCrawlResponse,
    CrawlRequest,
    CrawlResponse,
    HealthResponse,
    JobStatus,
    JobStatusResponse,
    ServerStatsResponse,
    URLValidationRequest,
    URLValidationResponse,
)
from app.utils.logging import get_logger
from app.utils.validators import validate_url

logger = get_logger(__name__)

# Create router with prefix
router = APIRouter()


@router.get("/", response_model=dict)
async def root():
    """Root endpoint with welcome message."""
    return {
        "message": "Crawl MCP is running.",
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", version=__version__, timestamp=datetime.utcnow())


@router.get("/stats", response_model=ServerStatsResponse)
async def get_server_stats():
    """Get server statistics."""
    stats = get_stats()
    return ServerStatsResponse(**stats)


@router.post("/crawl", response_model=CrawlResponse)
async def crawl_url(request: CrawlRequest, http_request: Request):
    """
    Crawl a single URL and return markdown content.

    - **url**: URL to crawl (required)
    - **include_links**: Include extracted links in response
    - **include_images**: Include extracted images in response
    - **max_depth**: Maximum crawl depth (1-5)
    - **timeout**: Custom timeout in seconds (5-300)
    """
    request_id = getattr(http_request.state, "request_id", str(uuid.uuid4()))

    try:
        async with WebCrawler() as crawler:
            result = await crawler.crawl(
                url=request.url,
                request_id=request_id,
                timeout=request.timeout,
                include_links=request.include_links,
                include_images=request.include_images,
            )

        increment_crawl_success()

        return CrawlResponse(
            status="success",
            url=result.url,
            markdown=result.markdown,
            links=result.links if request.include_links else None,
            images=result.images if request.include_images else None,
            metadata=result.metadata,
            crawled_at=result.crawled_at,
        )

    except CrawlMCPException as e:
        increment_crawl_failure()
        raise HTTPException(
            status_code=e.status_code,
            detail={"error": e.__class__.__name__, "message": e.message, "details": e.details},
        ) from e
    except Exception as e:
        increment_crawl_failure()
        logger.error(f"Unexpected error in crawl: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500, detail={"error": "InternalServerError", "message": str(e)}
        ) from e


@router.post("/crawl/batch", response_model=BatchCrawlResponse)
async def crawl_batch(request: BatchCrawlRequest, http_request: Request):
    """
    Crawl multiple URLs in batch.

    Returns a job ID that can be used to check status.

    - **urls**: List of URLs to crawl (1-100 URLs)
    - **include_links**: Include extracted links
    - **include_images**: Include extracted images
    - **timeout**: Custom timeout per URL
    """
    request_id = getattr(http_request.state, "request_id", str(uuid.uuid4()))
    job_id = f"batch_{uuid.uuid4().hex[:12]}"

    # Create job record
    job_data = {
        "job_id": job_id,
        "status": JobStatus.PENDING,
        "urls": request.urls,
        "total_urls": len(request.urls),
        "completed": 0,
        "failed": 0,
        "results": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    store_job(job_id, job_data)

    # Start batch crawl (fire and forget for now - in production use Celery/background tasks)
    try:
        update_job(job_id, {"status": JobStatus.IN_PROGRESS})

        async with WebCrawler() as crawler:
            results = await crawler.crawl_batch(
                urls=request.urls,
                request_id=request_id,
                timeout=request.timeout,
                include_links=request.include_links,
                include_images=request.include_images,
            )

        # Process results
        crawl_responses = []
        successful = 0
        failed = 0

        for result in results:
            if result.success:
                successful += 1
                increment_crawl_success()
                crawl_responses.append(
                    CrawlResponse(
                        status="success",
                        url=result.url,
                        markdown=result.markdown,
                        links=result.links if request.include_links else None,
                        images=result.images if request.include_images else None,
                        metadata=result.metadata,
                        crawled_at=result.crawled_at,
                    )
                )
            else:
                failed += 1
                increment_crawl_failure()

        # Update job
        update_job(
            job_id,
            {
                "status": JobStatus.COMPLETED,
                "completed": successful,
                "failed": failed,
                "results": [r.model_dump(mode="json") for r in crawl_responses],
                "updated_at": datetime.utcnow(),
            },
        )

        return BatchCrawlResponse(
            job_id=job_id,
            status=JobStatus.COMPLETED,
            total_urls=len(request.urls),
            completed=successful,
            failed=failed,
            results=crawl_responses,
        )

    except Exception as e:
        logger.error(f"Batch crawl error: {str(e)}", exc_info=e)
        update_job(
            job_id,
            {"status": JobStatus.FAILED, "error_message": str(e), "updated_at": datetime.utcnow()},
        )
        return BatchCrawlResponse(
            job_id=job_id,
            status=JobStatus.FAILED,
            total_urls=len(request.urls),
            completed=0,
            failed=len(request.urls),
            results=[],
        )


@router.get("/crawl/status/{job_id}", response_model=JobStatusResponse)
async def get_crawl_status(job_id: str):
    """
    Get status of a batch crawl job.

    - **job_id**: Job identifier returned from batch crawl
    """
    job = get_job(job_id)

    if not job:
        raise JobNotFoundError(job_id)

    progress = (job["completed"] / job["total_urls"] * 100) if job["total_urls"] > 0 else 0.0

    return JobStatusResponse(
        job_id=job["job_id"],
        status=job["status"],
        created_at=job["created_at"],
        updated_at=job["updated_at"],
        total_urls=job["total_urls"],
        completed=job["completed"],
        failed=job["failed"],
        progress=progress,
        error_message=job.get("error_message"),
    )


@router.post("/crawl/validate", response_model=URLValidationResponse)
async def validate_url_endpoint(request: URLValidationRequest):
    """
    Validate a URL before crawling.

    - **url**: URL to validate
    """
    try:
        scheme, domain = validate_url(request.url)

        return URLValidationResponse(
            url=request.url,
            is_valid=True,
            scheme=scheme,
            domain=domain,
            is_blocked=False,
            error_message=None,
        )

    except BlockedDomainError as e:
        return URLValidationResponse(
            url=request.url,
            is_valid=False,
            scheme=None,
            domain=e.details.get("domain"),
            is_blocked=True,
            error_message=e.message,
        )

    except URLValidationError as e:
        return URLValidationResponse(
            url=request.url,
            is_valid=False,
            scheme=None,
            domain=None,
            is_blocked=False,
            error_message=e.message,
        )
    except Exception as e:
        return URLValidationResponse(
            url=request.url,
            is_valid=False,
            scheme=None,
            domain=None,
            is_blocked=False,
            error_message=f"Validation error: {str(e)}",
        )
