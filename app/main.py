from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered web scraping and data extraction engine",
    version=settings.VERSION,
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "endpoints": {
            "scrape": "/api/v1/scrape [POST]",
            "batch_scrape": "/api/v1/scrape/batch [POST]",
            "get_result": "/api/v1/scrape/{id} [GET]",
            "recent": "/api/v1/scrapes/recent [GET]",
            "health": "/api/v1/health [GET]"
        }
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)
