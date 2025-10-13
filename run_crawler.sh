#!/bin/bash
# Run Crawl MCP server

cd /home/milhy777/Develop/Development/crawl-mcp/
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8012
