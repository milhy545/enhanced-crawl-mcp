"""
Web crawler core logic with retry and error handling.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any

from crawl4ai import AsyncWebCrawler

from app.config import get_settings
from app.core.exceptions import (
    ContentExtractionError,
    CrawlError,
    CrawlRetryExhaustedError,
    CrawlTimeoutError,
)
from app.utils.logging import CrawlerLogger, get_logger
from app.utils.validators import validate_url

# NOTE: Historically we modified sys.path to include a vendored crawl4ai. The
# current project installs crawl4ai as a dependency, so this path injection is
# unnecessary and triggers import-order linters. Keep the code minimal.


logger = get_logger(__name__)
crawler_logger = CrawlerLogger(logger)


class CrawlResult:
    """Container for crawl results."""

    def __init__(
        self,
        url: str,
        markdown: str,
        links: list[str] | None = None,
        images: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        duration_ms: float = 0.0,
        success: bool = True,
        error: str | None = None,
    ):
        self.url = url
        self.markdown = markdown
        self.links = links or []
        self.images = images or []
        self.metadata = metadata or {}
        self.duration_ms = duration_ms
        self.success = success
        self.error = error
        self.crawled_at = datetime.utcnow()


class WebCrawler:
    """Web crawler with retry logic and error handling."""

    def __init__(self):
        self.settings = get_settings()
        self._crawler: AsyncWebCrawler | None = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._crawler = AsyncWebCrawler()
        await self._crawler.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._crawler:
            await self._crawler.__aexit__(exc_type, exc_val, exc_tb)

    async def crawl(
        self,
        url: str,
        request_id: str | None = None,
        timeout: int | None = None,
        include_links: bool = False,
        include_images: bool = False,
        max_retries: int | None = None,
    ) -> CrawlResult:
        """
        Crawl a single URL with retry logic.

        Args:
            url: URL to crawl
            request_id: Request tracking ID
            timeout: Custom timeout in seconds
            include_links: Whether to include extracted links
            include_images: Whether to include extracted images
            max_retries: Maximum retry attempts

        Returns:
            CrawlResult object

        Raises:
            CrawlError: If crawl fails
            CrawlTimeoutError: If timeout occurs
            CrawlRetryExhaustedError: If all retries fail
        """
        if not request_id:
            request_id = str(uuid.uuid4())

        # Validate URL
        validate_url(url)

        # Get timeout and retries from settings if not provided
        timeout = timeout or self.settings.crawler_timeout
        max_retries = max_retries if max_retries is not None else self.settings.crawler_max_retries

        # Start timing
        start_time = datetime.utcnow()

        # Log crawl start
        crawler_logger.log_crawl_start(url, request_id, timeout=timeout)

        # Attempt crawl with retries
        last_error: BaseException | None = None
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    # Log retry
                    crawler_logger.log_retry(url, request_id, attempt, max_retries)
                    # Wait before retry
                    await asyncio.sleep(self.settings.crawler_retry_delay * attempt)

                # Perform crawl
                result = await self._do_crawl(
                    url, timeout=timeout, include_links=include_links, include_images=include_images
                )

                # Calculate duration
                duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
                result.duration_ms = duration_ms

                # Log success
                crawler_logger.log_crawl_success(url, request_id, duration_ms, len(result.markdown))

                return result

            except TimeoutError as e:
                last_error = CrawlTimeoutError(url, timeout)
                if attempt >= max_retries:
                    crawler_logger.log_crawl_failure(url, request_id, str(last_error), exc_info=e)
                    raise last_error from e

            except Exception as e:
                last_error = CrawlError(f"Crawl failed: {str(e)}", url=url)
                if attempt >= max_retries:
                    crawler_logger.log_crawl_failure(url, request_id, str(last_error), exc_info=e)
                    raise last_error from e

        # All retries exhausted
        raise CrawlRetryExhaustedError(url, max_retries + 1)

    async def _do_crawl(
        self, url: str, timeout: int, include_links: bool, include_images: bool
    ) -> CrawlResult:
        """
        Perform the actual crawl operation.

        Args:
            url: URL to crawl
            timeout: Timeout in seconds
            include_links: Whether to extract links
            include_images: Whether to extract images

        Returns:
            CrawlResult object

        Raises:
            ContentExtractionError: If content extraction fails
            asyncio.TimeoutError: If operation times out
        """
        if not self._crawler:
            raise CrawlError("Crawler not initialized. Use async context manager.")

        # Execute crawl with timeout
        try:
            result = await asyncio.wait_for(self._crawler.arun(url), timeout=timeout)
        except TimeoutError:
            raise
        except Exception as e:
            raise CrawlError(f"Crawler execution failed: {str(e)}", url=url) from e

        # Extract markdown
        if not result or not hasattr(result, "markdown"):
            raise ContentExtractionError(url, "No result or markdown attribute")

        markdown = (
            result.markdown.raw_markdown
            if hasattr(result.markdown, "raw_markdown")
            else str(result.markdown)
        )

        if not markdown:
            raise ContentExtractionError(url, "Empty markdown content")

        # Extract links if requested
        links: list[str] = []
        if include_links and hasattr(result, "links"):
            links = (
                result.links.get("internal", []) + result.links.get("external", [])
                if isinstance(result.links, dict)
                else []
            )

        # Extract images if requested
        images: list[str] = []
        if include_images and hasattr(result, "media"):
            if isinstance(result.media, dict) and "images" in result.media:
                images = [img.get("src") for img in result.media["images"] if img.get("src")]

        # Build metadata
        metadata = {}
        if hasattr(result, "metadata"):
            metadata = result.metadata if isinstance(result.metadata, dict) else {}

        return CrawlResult(
            url=url, markdown=markdown, links=links, images=images, metadata=metadata, success=True
        )

    async def crawl_batch(
        self, urls: list[str], request_id: str | None = None, **kwargs
    ) -> list[CrawlResult]:
        """
        Crawl multiple URLs concurrently.

        Args:
            urls: List of URLs to crawl
            request_id: Request tracking ID
            **kwargs: Additional arguments for crawl method

        Returns:
            List of CrawlResult objects
        """
        if not request_id:
            request_id = str(uuid.uuid4())

        # Create tasks
        tasks = []
        for url in urls:
            task = self.crawl(url, request_id=f"{request_id}_{url}", **kwargs)
            tasks.append(task)

        # Execute concurrently with semaphore for rate limiting
        semaphore = asyncio.Semaphore(self.settings.crawler_max_concurrent)

        async def limited_crawl(task):
            async with semaphore:
                try:
                    return await task
                except Exception as e:
                    # Return error result instead of raising
                    logger.error(f"Batch crawl error: {str(e)}", exc_info=e)
                    return CrawlResult(url="unknown", markdown="", success=False, error=str(e))

        results = await asyncio.gather(
            *[limited_crawl(task) for task in tasks], return_exceptions=False
        )

        return results
