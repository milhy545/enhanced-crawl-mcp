"""
Unit tests for configuration module.
"""

import pytest
from pydantic import ValidationError

from app.config import Settings, get_settings


class TestSettings:
    """Test Settings class."""

    def test_default_settings(self):
        """Test default settings values."""
        # Unset env vars to test defaults
        import os
        from unittest.mock import patch

        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()

            assert settings.app_name == "Crawl MCP"
            assert settings.host == "0.0.0.0"
            assert settings.port == 8012
            assert settings.log_level == "INFO"
            assert settings.crawler_timeout == 30
            assert settings.crawler_max_retries == 3

    def test_log_level_validation(self):
        """Test log level validation."""
        # Valid log level
        settings = Settings(log_level="DEBUG")
        assert settings.log_level == "DEBUG"

        # Case insensitive
        settings = Settings(log_level="info")
        assert settings.log_level == "INFO"

        # Invalid log level
        with pytest.raises(ValidationError):
            Settings(log_level="INVALID")

    def test_cors_origins_parsing(self):
        """Test CORS origins parsing from string."""
        # String parsing
        settings = Settings(cors_origins="http://localhost:3000,http://example.com")
        assert settings.cors_origins == ["http://localhost:3000", "http://example.com"]

        # List input
        settings = Settings(cors_origins=["http://localhost:3000"])
        assert settings.cors_origins == ["http://localhost:3000"]

    def test_blocked_domains_parsing(self):
        """Test blocked domains parsing from string."""
        # String parsing
        settings = Settings(blocked_domains="spam.com,malicious.net")
        assert settings.blocked_domains == ["spam.com", "malicious.net"]

        # List input
        settings = Settings(blocked_domains=["spam.com"])
        assert settings.blocked_domains == ["spam.com"]

    def test_allowed_schemes_parsing(self):
        """Test allowed schemes parsing from string."""
        settings = Settings(allowed_schemes="https")
        assert settings.allowed_schemes == ["https"]

        settings = Settings(allowed_schemes="http, https")
        assert settings.allowed_schemes == ["http", "https"]

    def test_get_settings(self):
        """Test get_settings function."""
        settings = get_settings()
        assert isinstance(settings, Settings)

        # Should return same instance
        settings2 = get_settings()
        assert settings is settings2
