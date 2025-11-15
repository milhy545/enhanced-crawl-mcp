# Security Policy

## Supported Versions

We actively maintain and provide security updates for the latest version of Enhanced Crawl MCP.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Requirements

### Build Dependencies

To ensure a secure installation, the following minimum versions are required:

- **pip**: >= 25.3 (fixes CVE-2025-8869 - path traversal vulnerability)
- **setuptools**: >= 78.1.1 (fixes CVE-2025-47273 and CVE-2024-6345 - path traversal and RCE vulnerabilities)

### Installation

Before installing this package, ensure your build tools are up to date:

```bash
pip install --upgrade "pip>=25.3" "setuptools>=78.1.1"
pip install -r requirements.txt
```

Or using the development dependencies:

```bash
pip install --upgrade "pip>=25.3" "setuptools>=78.1.1"
pip install -e ".[dev]"
```

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it by:

1. **Do not** open a public issue
2. Contact the maintainers privately via GitHub Security Advisories
3. Provide detailed information about the vulnerability

We will respond to security reports within 48 hours and work to address confirmed vulnerabilities promptly.

## Security Best Practices

When deploying Enhanced Crawl MCP:

1. **Always use HTTPS** for API endpoints in production
2. **Configure rate limiting** appropriately for your use case
3. **Maintain blocked domains list** to prevent crawling of malicious sites
4. **Keep dependencies updated** regularly
5. **Use environment variables** for sensitive configuration (never commit secrets)
6. **Run security scans** periodically using tools like `pip-audit`:
   ```bash
   pip install pip-audit
   pip-audit
   ```

## Recent Security Updates

### 2025-11-15
- Updated pip from 24.0 to 25.3 (fixes CVE-2025-8869)
- Updated setuptools from 68.1.2 to 80.9.0 (fixes CVE-2025-47273, CVE-2024-6345)
- All tests passing with updated dependencies
- Zero known vulnerabilities in current dependency tree
