"""
Application configuration module.

Handles environment variables and application settings.
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application settings
    app_name: str = Field(default="Crawl MCP", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    app_description: str = Field(
        default="A microservice for crawling web pages for AI context.",
        description="Application description",
    )

    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")  # nosec B104
    port: int = Field(default=8012, description="Server port")
    workers: int = Field(default=1, description="Number of worker processes")
    reload: bool = Field(default=False, description="Enable auto-reload in development")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")
    log_file: str | None = Field(default="logs/app.log", description="Log file path")

    # Crawler settings
    crawler_timeout: int = Field(default=30, description="Default crawler timeout in seconds")
    crawler_max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    crawler_retry_delay: int = Field(default=1, description="Delay between retries in seconds")
    crawler_user_agent: str | None = Field(default=None, description="Custom user agent")
    crawler_max_concurrent: int = Field(default=5, description="Maximum concurrent crawl requests")

    # API settings
    api_prefix: str = Field(default="/api/v1", description="API route prefix")
    cors_enabled: bool = Field(default=True, description="Enable CORS")
    cors_origins: list[str] = Field(default=["*"], description="Allowed CORS origins")
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_requests: int = Field(default=100, description="Max requests per minute")

    # Security settings
    allowed_schemes: list[str] = Field(
        default=["http", "https"], description="Allowed URL schemes for crawling"
    )
    blocked_domains: list[str] = Field(default=[], description="Domains blocked from crawling")

    # Job/Task settings
    job_cleanup_interval: int = Field(
        default=3600, description="Interval in seconds for cleaning up old jobs"
    )
    job_max_age: int = Field(
        default=86400, description="Maximum age of completed jobs in seconds (24 hours)"
    )

    # Paths
    project_root: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent, description="Project root directory"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed_levels:
            raise ValueError(f"Log level must be one of {allowed_levels}")
        return v_upper

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("blocked_domains", mode="before")
    @classmethod
    def parse_blocked_domains(cls, v):
        """Parse blocked domains from string or list."""
        if isinstance(v, str):
            return [domain.strip() for domain in v.split(",")]
        return v

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, env_prefix="CRAWL_MCP_"
    )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get application settings instance.

    Returns:
        Settings: The application settings singleton
    """
    return settings
