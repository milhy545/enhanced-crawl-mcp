# Installation Guide - Enhanced Crawl MCP

Kompletní průvodce instalací a spuštěním Enhanced Crawl MCP serveru.

## 📋 Požadavky

- **Python**: 3.10, 3.11 nebo 3.12
- **pip**: >= 25.3 (kvůli bezpečnosti)
- **setuptools**: >= 78.1.1 (kvůli bezpečnosti)
- **Git** (pro instalaci z repository)

## 🚀 Rychlá instalace

### 1. Klonování repository

```bash
git clone https://github.com/milhy545/enhanced-crawl-mcp.git
cd enhanced-crawl-mcp
```

### 2. Vytvoření virtuálního prostředí (DOPORUČENO!)

```bash
# Vytvoření virtual environment
python -m venv venv

# Aktivace (Linux/Mac)
source venv/bin/activate

# Aktivace (Windows)
venv\Scripts\activate
```

### 3. Upgrade build tools (DŮLEŽITÉ pro bezpečnost!)

```bash
pip install --upgrade "pip>=25.3" "setuptools>=78.1.1"
```

### 4. Instalace závislostí

**Produkční instalace:**
```bash
pip install -r requirements.txt
```

**Vývojářská instalace (s testy a lintingy):**
```bash
pip install -e ".[dev]"
```

### 5. Instalace crawl4ai (speciální krok)

```bash
pip install crawl4ai
```

**Poznámka:** crawl4ai může vyžadovat další závislosti podle vašeho systému. Viz [crawl4ai dokumentace](https://github.com/unclecode/crawl4ai).

## ⚙️ Konfigurace

### Vytvoření .env souboru

```bash
cp .env.example .env
```

### Editace .env souboru

```bash
# App Configuration
APP_NAME=Crawl MCP
APP_DESCRIPTION=A FastAPI-based microservice for web crawling
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=text  # nebo "json" pro structured logging
LOG_FILE=  # Nechte prázdné pro logging pouze do konzole

# CORS
CORS_ENABLED=true
CORS_ORIGINS=*  # V produkci nastavte konkrétní domény!

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100

# Crawler Settings
CRAWLER_TIMEOUT=30
CRAWLER_MAX_RETRIES=3
CRAWLER_RETRY_DELAY=2
CRAWLER_MAX_CONCURRENT=5

# URL Validation
ALLOWED_SCHEMES=http,https
BLOCKED_DOMAINS=localhost,127.0.0.1,0.0.0.0

# API
API_PREFIX=/api/v1
```

## 🎯 Spuštění aplikace

### Vývojové prostředí

```bash
# Pomocí uvicorn přímo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Nebo pomocí Python modulu
python -m uvicorn app.main:app --reload
```

### Produkční prostředí

```bash
# S více workery pro lepší výkon
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info

# Nebo pomocí gunicorn (doporučeno pro produkci)
pip install gunicorn
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info
```

### Pomocí Docker

```bash
# Build image
docker build -t crawl-mcp:latest .

# Spuštění containeru
docker run -d \
  --name crawl-mcp \
  -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  crawl-mcp:latest

# Nebo pomocí docker-compose
docker-compose up -d
```

## 🧪 Testování instalace

### 1. Spuštění testů

```bash
# Všechny testy
pytest tests/ -v

# S coverage reportem
pytest tests/ -v --cov=app --cov-report=html

# Pouze jednotkové testy
pytest tests/unit/ -v

# Pouze integrační testy
pytest tests/integration/ -v
```

### 2. Kontrola API

Po spuštění navštivte:

- **API Dokumentace (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 3. Test crawlování

```bash
# Pomocí curl
curl -X POST "http://localhost:8000/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Pomocí httpie
http POST localhost:8000/crawl url=https://example.com
```

## 🔧 Maintenance příkazy

### Bezpečnostní kontrola

```bash
# Kontrola vulnerabilities
pip install pip-audit
pip-audit

# Nebo pomocí bandit
bandit -r app/
```

### Code quality

```bash
# Linting
ruff check app/

# Formátování
black app/
isort app/

# Type checking
mypy app/ --ignore-missing-imports
```

## 🐛 Troubleshooting

### Problem: crawl4ai se nenainstaluje

**Řešení:**
```bash
# Zkuste instalaci s dodatečnými závislostmi
pip install crawl4ai[all]

# Nebo postupně
pip install playwright
playwright install
pip install crawl4ai
```

### Problem: Permission denied při spuštění

**Řešení:**
```bash
# Změňte port na vyšší číslo (> 1024)
uvicorn app.main:app --port 8080
```

### Problem: Import error

**Řešení:**
```bash
# Ujistěte se, že jste ve správném adresáři
pwd  # mělo by být /path/to/enhanced-crawl-mcp

# A že máte aktivované virtual environment
which python  # mělo by ukazovat do venv/
```

## 📊 Monitoring

### Logs

```bash
# Real-time logs
tail -f logs/app.log  # pokud máte LOG_FILE nastavené

# Nebo Docker logs
docker logs -f crawl-mcp
```

### Metriky

Navštivte endpoint `/stats` pro aktuální statistiky:

```bash
curl http://localhost:8000/stats
```

## 🔒 Production Best Practices

1. **Použijte HTTPS** - nastav reverse proxy (nginx, traefik)
2. **Nastavte konkrétní CORS_ORIGINS** - ne `*`
3. **Použijte environment proměnné** - ne .env soubor v produkci
4. **Rate limiting** - přizpůsobte svým potřebám
5. **Monitoring** - nastavte logging aggregaci (ELK, Datadog, atd.)
6. **Backups** - pokud používáte persistent storage
7. **Updates** - pravidelně aktualizujte dependencies
8. **Security scans** - spouštějte `pip-audit` pravidelně

## 📝 Další kroky

Po úspěšné instalaci:

1. ✅ Zkontrolujte `/health` endpoint
2. ✅ Prohlédněte `/docs` pro API dokumentaci
3. ✅ Otestujte crawlování na testovací URL
4. ✅ Nastavte monitoring
5. ✅ Nakonfigurujte reverse proxy (pro HTTPS)

## 💡 Užitečné odkazy

- **GitHub**: https://github.com/milhy545/enhanced-crawl-mcp
- **API Docs**: http://localhost:8000/docs
- **Security Policy**: viz SECURITY.md
- **Changelog**: viz CHANGELOG.md

---

Potřebuješ pomoc? Otevři issue na GitHubu nebo kontaktuj maintainera.
