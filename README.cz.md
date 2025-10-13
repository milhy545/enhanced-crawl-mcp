# Crawl MCP

Výkonná mikroslužba postavená na FastAPI pro web crawling optimalizovaný pro AI a LLM.

## Funkce

- 🌐 Crawling jednotlivých i více URL
- 📦 Dávkové zpracování s podporou konkurence
- 🔗 Extrakce odkazů a obrázků
- ⚡ Asynchronní architektura
- 🔄 Automatická retry logika
- 📊 Sledování stavu úloh

## Rychlý start

```bash
git clone <repository-url>
cd crawl-mcp
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./run_crawler.sh
```

API bude dostupné na `http://localhost:8012`

## Použití

```bash
# Základní crawl
curl -X POST http://localhost:8012/api/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Dávkový crawl
curl -X POST http://localhost:8012/api/v1/crawl/batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com", "https://example.org"]}'
```

## Dokumentace

- API dokumentace: `http://localhost:8012/docs`
- Detaily API: [API_REFERENCE.cz.md](docs/API_REFERENCE.cz.md)
- Deployment: [DEPLOYMENT.cz.md](docs/DEPLOYMENT.cz.md)
- Development: [DEVELOPMENT.cz.md](docs/DEVELOPMENT.cz.md)
- Architektura: [ARCHITECTURE.cz.md](docs/ARCHITECTURE.cz.md)

## Konfigurace

Konfigurace přes environment proměnné (viz `.env.example`)

## Docker

```bash
docker-compose up -d
```

## Testování

```bash
pytest
pytest --cov=app
```

## Licence

MIT License
