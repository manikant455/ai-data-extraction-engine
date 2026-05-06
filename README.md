
# 🤖 AI Data Extraction Engine

> Intelligent web scraping with AI-powered data structuring. Scrape any website and extract meaningful data using LLMs.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI-412991.svg)](https://openai.com/)

## ✨ Features

- **Smart Scraping**: BeautifulSoup + Playwright for any website
- **AI Extraction**: LLM-powered structured data extraction
- **Batch Processing**: Scrape multiple URLs at once
- **Auto-Detection**: Emails, phones, prices, and more
- **Dual Parser**: AI-powered + Rule-based fallback
- **Performance Metrics**: Load time, content size tracking

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Core language |
| FastAPI | API framework |
| BeautifulSoup4/lXML | HTML parsing |
| Playwright | JavaScript rendering |
| OpenAI API | AI data extraction |
| MongoDB | Storage |
| Redis + Celery | Queue system |
| Docker | Containerization |

## 🚀 Quick Start

### Local Installation

```bash
git clone https://github.com/manikant455/ai-data-extraction-engine.git
cd ai-data-extraction-engine

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

uvicorn app.main:app --reload --port 8002

Docker
bash
git clone https://github.com/manikant455/ai-data-extraction-engine.git
cd ai-data-extraction-engine

docker-compose up --build
Open http://localhost:8002/docs

📚 API Endpoints
Method	Endpoint	Description
POST	/api/v1/scrape	Scrape single URL
POST	/api/v1/scrape/batch	Scrape multiple URLs
GET	/api/v1/scrape/{id}	Get result
GET	/api/v1/scrapes/recent	Recent scrapes
GET	/api/v1/health	Health check

📊 Usage Examples

Basic Scrape

curl -X POST http://localhost:8002/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'


Scrape with AI Extraction

curl -X POST http://localhost:8002/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "extract_schema": {
      "title": "string",
      "description": "string",
      "emails": "array",
      "phones": "array"
    },
    "ai_summarize": true
  }'


Batch Scrape

curl -X POST http://localhost:8002/api/v1/scrape/batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com", "https://github.com"]}'


JavaScript Sites

curl -X POST http://localhost:8002/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "use_playwright": true}'


📈 Sample Response
json
{
  "id": "abc-123",
  "url": "https://example.com",
  "scraped_data": {
    "title": "Example Domain",
    "text_content": "This domain is for use...",
    "links": [...],
    "images": [...],
    "headings": {"h1": ["Example Domain"]}
  },
  "extracted_data": {
    "extracted_data": {
      "title": "Example Domain",
      "emails": [],
      "phones": []
    },
    "method": "fallback",
    "confidence": 0.5
  },
  "summary": {
    "summary": "Page Title: Example Domain\nContent Preview: This domain is...",
    "method": "fallback"
  }
}


🎯 Use Cases
Lead Generation: Extract emails, phones from directories

Price Monitoring: Track competitor pricing

Content Aggregation: Collect articles, news

Market Research: Structured data from any website

Job Boards: Scrape and structure job listings

👤 Author
Manikant

GitHub: @manikant455