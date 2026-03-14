# 🚀 Quick Start - 5 minut k spuštění!

Nejrychlejší cesta, jak rozjet Enhanced Crawl MCP.

## ⚡ Rychlá instalace (5 kroků)

```bash
# 1. Stáhni projekt
git clone https://github.com/milhy545/enhanced-crawl-mcp.git
cd enhanced-crawl-mcp

# 2. Vytvoř virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo: venv\Scripts\activate  # Windows

# 3. Upgrade bezpečnostních nástrojů
pip install --upgrade "pip>=25.3" "setuptools>=78.1.1"

# 4. Instaluj závislosti
pip install -r requirements.txt

# 5. Spusť server!
uvicorn app.main:app --reload
```

## ✅ Hotovo!

Server běží na: **http://localhost:8000**

### Vyzkoušej API:

**Otevři prohlížeč:**
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

**Nebo pomocí curl:**
```bash
# Zdravotní kontrola
curl http://localhost:8000/health

# Crawluj webovou stránku
curl -X POST "http://localhost:8000/api/v1/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# S linky a obrázky
curl -X POST "http://localhost:8000/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "include_links": true,
    "include_images": true
  }'
```

## 🎯 Hlavní endpointy

| Endpoint | Metoda | Popis |
|----------|--------|-------|
| `/health` | GET | Kontrola stavu serveru |
| `/stats` | GET | Statistiky serveru |
| `/crawl` | POST | Crawl jedné URL |
| `/crawl/batch` | POST | Crawl více URL najednou |
| `/crawl/validate` | POST | Validace URL |
| `/docs` | GET | Interaktivní API dokumentace |

## 📖 Příklady použití

### 1. Jednoduchý crawl

```bash
curl -X POST "http://localhost:8000/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://python.org"}'
```

### 2. Batch crawl

```bash
curl -X POST "http://localhost:8000/crawl/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example.com",
      "https://python.org",
      "https://github.com"
    ]
  }'
```

### 3. S vlastním timeout

```bash
curl -X POST "http://localhost:8000/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://slow-website.com",
    "timeout": 60
  }'
```

### 4. Python klient

```python
import requests

# Crawl URL
response = requests.post(
    "http://localhost:8000/crawl",
    json={
        "url": "https://example.com",
        "include_links": True,
        "include_images": True
    }
)

result = response.json()
print(f"Status: {result['status']}")
print(f"Markdown:\n{result['markdown']}")
print(f"Links: {len(result['links'])}")
```

## 🔧 Pokročilá konfigurace

### Environment proměnné (.env)

```bash
# Zkopíruj příklad
cp .env.example .env

# Edituj podle potřeby
nano .env
```

Důležité nastavení:
```
PORT=8000                    # Port serveru
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
RATE_LIMIT_REQUESTS=100     # Počet requestů za minutu
CRAWLER_TIMEOUT=30          # Timeout pro crawling
```

### Docker spuštění

```bash
# Build
docker-compose build

# Spusť
docker-compose up -d

# Kontrola logů
docker-compose logs -f
```

## 🐛 Časté problémy

### Port už je použitý?
```bash
# Použij jiný port
uvicorn app.main:app --port 8080
```

### Import errory?
```bash
# Ujisti se, že jsi v projektu a máš aktivní venv
pwd
which python  # mělo by ukazovat do venv/
```

### crawl4ai se neinstaluje?
```bash
# Zkus s playwright
pip install playwright
playwright install
pip install crawl4ai
```

## 📚 Další dokumentace

- **Plná instalace**: viz [INSTALL.md](INSTALL.md)
- **Bezpečnost**: viz [SECURITY.md](SECURITY.md)
- **API dokumentace**: http://localhost:8000/docs (po spuštění)
- **Změny**: viz [CHANGELOG.md](CHANGELOG.md)

## 🎉 A teď?

1. ✅ Prohlédni **Swagger UI** na http://localhost:8000/docs
2. ✅ Vyzkoušej **crawlování** různých webů
3. ✅ Přečti si **[INSTALL.md](INSTALL.md)** pro produkční nasazení
4. ✅ Nastav **monitoring** a **logging**

---

**Potřebuješ pomoc?** Otevři issue na GitHubu!

**Líbí se ti projekt?** Dej ⭐ na GitHubu!
