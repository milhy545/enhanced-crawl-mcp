import sys
sys.path.insert(0, '/home/milhy777/Develop/Development/crawl-mcp/libs/crawl4ai')

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from crawl4ai import AsyncWebCrawler

app = FastAPI(
    title="Crawl MCP",
    description="A microservice for crawling web pages for AI context.",
    version="1.0.0",
)

class CrawlRequest(BaseModel):
    url: str

@app.post("/crawl")
async def crawl_url(request: CrawlRequest):
    """
    Crawls a given URL and returns the content in markdown format.
    """
    if not request.url:
        raise HTTPException(status_code=400, detail="URL is required.")
    
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(request.url)
            if result and result.markdown:
                return {"status": "success", "markdown": result.markdown.raw_markdown}
            else:
                raise HTTPException(status_code=500, detail="Failed to retrieve content.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Crawl MCP is running."}

@app.get("/health")
def health_check():
    return {"status": "ok"}
