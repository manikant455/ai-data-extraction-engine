import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "AI Data Extraction Engine"
    VERSION: str = "1.0.0"
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "scraper_db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Scraping
    USER_AGENT: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

settings = Settings()
