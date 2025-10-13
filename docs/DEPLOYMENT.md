# Deployment Guide

Production deployment guide for Crawl MCP.

## Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.10+ with pip
- Access to target deployment environment
- SSL certificate (for HTTPS)

## Environment Variables

Create a `.env` file with production values:

```bash
# Server
CRAWL_MCP_HOST=0.0.0.0
CRAWL_MCP_PORT=8012
CRAWL_MCP_WORKERS=4

# Logging
CRAWL_MCP_LOG_LEVEL=INFO
CRAWL_MCP_LOG_FORMAT=json
CRAWL_MCP_LOG_FILE=/var/log/crawl-mcp/app.log

# Crawler
CRAWL_MCP_CRAWLER_TIMEOUT=30
CRAWL_MCP_CRAWLER_MAX_RETRIES=3
CRAWL_MCP_CRAWLER_MAX_CONCURRENT=10

# Security
CRAWL_MCP_RATE_LIMIT_ENABLED=true
CRAWL_MCP_RATE_LIMIT_REQUESTS=100
CRAWL_MCP_BLOCKED_DOMAINS=spam.com,malicious.net

# CORS
CRAWL_MCP_CORS_ENABLED=true
CRAWL_MCP_CORS_ORIGINS=https://yourdomain.com
```

## Docker Deployment (Recommended)

### 1. Build Image

```bash
docker build -t crawl-mcp:latest .
```

### 2. Run Container

```bash
docker run -d \
  --name crawl-mcp \
  -p 8012:8012 \
  --env-file .env \
  --restart unless-stopped \
  crawl-mcp:latest
```

### 3. Using Docker Compose

```bash
docker-compose up -d
```

### 4. Health Check

```bash
curl http://localhost:8012/health
```

## Kubernetes Deployment

See `deploy/kubernetes/` for manifests.

```bash
kubectl apply -f deploy/kubernetes/
```

## Production Best Practices

### 1. Reverse Proxy (Nginx)

```nginx
upstream crawl_mcp {
    server localhost:8012;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://crawl_mcp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Monitoring

Use Prometheus + Grafana:

```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

### 3. Logging

Centralized logging with ELK stack:

```bash
# Forward logs to Elasticsearch
docker run -d \
  --name crawl-mcp \
  --log-driver=fluentd \
  --log-opt fluentd-address=localhost:24224 \
  crawl-mcp:latest
```

### 4. Scaling

Horizontal scaling with load balancer:

```bash
docker-compose up -d --scale crawl-mcp=3
```

### 5. Security

- Use HTTPS only
- Implement API key authentication
- Enable rate limiting
- Regular security audits
- Keep dependencies updated

## Cloud Deployments

### AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <ecr-url>
docker tag crawl-mcp:latest <ecr-url>/crawl-mcp:latest
docker push <ecr-url>/crawl-mcp:latest
```

### Google Cloud Run

```bash
gcloud run deploy crawl-mcp \
  --image gcr.io/<project>/crawl-mcp \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name crawl-mcp \
  --image myregistry.azurecr.io/crawl-mcp:latest \
  --ports 8012
```

## Troubleshooting

### Container won't start
- Check logs: `docker logs crawl-mcp`
- Verify environment variables
- Check port availability

### High memory usage
- Reduce `CRAWL_MCP_CRAWLER_MAX_CONCURRENT`
- Implement job queuing (Redis/Celery)
- Add memory limits to container

### Slow responses
- Check crawler timeout settings
- Monitor server resources
- Implement caching layer

