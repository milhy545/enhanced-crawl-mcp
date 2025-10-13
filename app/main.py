"""
Crawl MCP - FastAPI Application

A microservice for web crawling optimized for AI/LLM consumption.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.api.dependencies import LoggingMiddleware, RateLimitMiddleware, RequestIDMiddleware
from app.api.routes import router
from app.config import get_settings
from app.core.exceptions import CrawlMCPException
from app.models import ErrorResponse
from app.utils.logging import get_logger, setup_logging

# Initialize settings and logging
settings = get_settings()
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{__version__}")
    logger.info(f"Log level: {settings.log_level}")
    logger.info(f"CORS enabled: {settings.cors_enabled}")
    logger.info(f"Rate limiting enabled: {settings.rate_limit_enabled}")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add custom middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.rate_limit_requests)


# Exception handlers
@app.exception_handler(CrawlMCPException)
async def crawl_mcp_exception_handler(request, exc: CrawlMCPException):
    """Handle custom Crawl MCP exceptions."""
    error_response = ErrorResponse(
        error=exc.__class__.__name__, message=exc.message, details=exc.details
    )
    return JSONResponse(status_code=exc.status_code, content=error_response.dict())


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    """Handle unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
    error_response = ErrorResponse(
        error="InternalServerError",
        message="An unexpected error occurred",
        details={"error": str(exc)},
    )
    return JSONResponse(status_code=500, content=error_response.dict())


# Include API routes
app.include_router(router, prefix=settings.api_prefix, tags=["crawl"])
app.include_router(
    router, prefix="", tags=["root"]
)  # Also serve at root for backward compatibility


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        workers=settings.workers,
        log_level=settings.log_level.lower(),
    )
