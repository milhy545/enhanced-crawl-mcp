# Project: Crawl MCP Server

## Project Overview

This project is a FastAPI-based microservice that acts as a web crawler, specifically designed to be consumed by AI models and agents (MCP - Model Context Protocol). It exposes a simple API to crawl a given URL and returns the web page's content converted into clean, LLM-friendly Markdown.

The core functionality is powered by the `crawl4ai` library, an advanced open-source web crawler that specializes in turning web content into structured Markdown suitable for RAG (Retrieval-Augmented Generation), AI agents, and data pipelines.

The server provides the following endpoints:
- `POST /crawl`: The main endpoint that accepts a URL and returns the crawled content.
- `GET /health`: A standard health check endpoint.
- `GET /`: A root endpoint with a welcome message.

## Building and Running

### 1. Setup

The project uses a Python virtual environment located in the `venv/` directory. Dependencies are listed in `requirements.txt`.

To install dependencies:
```bash
# Ensure you are in the project root directory
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Running the Server

You can run the FastAPI server using Uvicorn.

**Directly:**
```bash
# Make sure the virtual environment is activated
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8012
```

**Using the script:**
A convenience script `run_crawler.sh` is provided to start the server.
```bash
./run_crawler.sh
```

**For persistent development (Recommended):**
The `start_crawl_mcp_tmux.sh` script will start the server inside a detached `tmux` session, ensuring it keeps running in the background.

```bash
# Start the server in a new or existing tmux session
./start_crawl_mcp_tmux.sh

# To attach to the session later:
tmux attach -t crawl-mcp-server

# To stop the server:
# 1. Attach to the session
# 2. Press Ctrl+C
```

## Development Conventions

*   **Main Application Logic:** The FastAPI application is defined in `main.py`.
*   **Core Dependency:** The project is a consumer of the `crawl4ai` library, which is included as a git submodule in the `libs/` directory. The `sys.path` is modified in `main.py` to import it directly.
*   **API Structure:** The API is simple and follows FastAPI conventions. The request and response models are defined using Pydantic.
*   **Configuration:** The server is configured to run on `0.0.0.0` at port `8012`.
