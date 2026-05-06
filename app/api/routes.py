from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import uuid
from datetime import datetime

from app.services.scraper import WebScraper
from app.services.ai_parser import AIParser
from app.services.playwright_scraper import PlaywrightScraper

router = APIRouter()

# In-memory storage
scrapes_db = {}

class ScrapeRequest(BaseModel):
    url: str = Field(..., description="URL to scrape")
    extract_schema: Optional[Dict] = Field(None, description="Schema for AI extraction")
    use_playwright: bool = Field(False, description="Use Playwright for JS sites")
    ai_summarize: bool = Field(False, description="AI summary of content")

class BatchScrapeRequest(BaseModel):
    urls: List[str] = Field(..., min_items=1, max_items=10)

@router.post("/scrape")
async def scrape_url(request: ScrapeRequest):
    """Scrape a single URL"""
    scrape_id = str(uuid.uuid4())
    
    scraper = WebScraper()
    scraped_data = await scraper.scrape(request.url)
    await scraper.close()
    
    if "error" in scraped_data:
        raise HTTPException(status_code=500, detail=scraped_data["error"])
    
    result = {
        "id": scrape_id,
        "url": request.url,
        "scraped_data": scraped_data,
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Use Playwright for JS sites if requested
    if request.use_playwright:
        pw_scraper = PlaywrightScraper()
        dynamic_data = await pw_scraper.scrape_dynamic(request.url)
        result["dynamic_data"] = dynamic_data
    
    # AI extraction if schema provided
    if request.extract_schema:
        ai_parser = AIParser()
        extracted = await ai_parser.extract_structured_data(scraped_data, request.extract_schema)
        result["extracted_data"] = extracted
    
    # AI summary if requested
    if request.ai_summarize:
        ai_parser = AIParser()
        summary = await ai_parser.summarize_data(scraped_data)
        result["summary"] = summary
    
    # Store
    scrapes_db[scrape_id] = result
    
    return result

@router.post("/scrape/batch")
async def scrape_batch(request: BatchScrapeRequest):
    """Scrape multiple URLs"""
    results = []
    
    for url in request.urls:
        try:
            scraper = WebScraper()
            data = await scraper.scrape(url)
            await scraper.close()
            results.append({
                "url": url,
                "status": "success",
                "data": data
            })
        except Exception as e:
            results.append({
                "url": url,
                "status": "failed",
                "error": str(e)
            })
    
    return {
        "total": len(request.urls),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
        "results": results
    }

@router.get("/scrape/{scrape_id}")
async def get_scrape(scrape_id: str):
    """Get scrape result by ID"""
    if scrape_id not in scrapes_db:
        raise HTTPException(status_code=404, detail="Scrape not found")
    return scrapes_db[scrape_id]

@router.get("/scrapes/recent")
async def recent_scrapes(limit: int = 10):
    """Get recent scrapes"""
    scrapes = list(scrapes_db.values())
    scrapes.sort(key=lambda x: x["created_at"], reverse=True)
    return scrapes[:limit]

@router.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "scrapes_count": len(scrapes_db),
        "timestamp": datetime.utcnow().isoformat()
    }
