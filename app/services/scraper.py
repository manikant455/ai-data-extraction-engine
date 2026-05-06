import httpx
from bs4 import BeautifulSoup
import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
import time
import re

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            }
        )
    
    async def scrape(self, url: str, extract_type: str = "all") -> Dict:
        """Scrape webpage and extract content"""
        start_time = time.time()
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            result = {
                "url": url,
                "status_code": response.status_code,
                "load_time": round(time.time() - start_time, 2),
                "title": self._get_title(soup),
                "meta_description": self._get_meta_description(soup),
                "text_content": self._get_text(soup),
                "links": self._get_links(soup, url),
                "images": self._get_images(soup, url),
                "headings": self._get_headings(soup),
                "tables": self._get_tables(soup),
                "lists": self._get_lists(soup),
                "raw_html_size": len(response.text)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Scraping failed for {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "status": "failed"
            }
    
    def _get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('title')
        return title.text.strip() if title else ""
    
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '') if meta else ""
    
    def _get_text(self, soup: BeautifulSoup) -> str:
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text[:5000]  # Limit to 5000 chars
    
    def _get_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        links = []
        for a in soup.find_all('a', href=True):
            href = urljoin(base_url, a['href'])
            text = a.text.strip()
            if text and href.startswith('http'):
                links.append({
                    "text": text[:100],
                    "url": href,
                    "internal": urlparse(base_url).netloc in href
                })
        return links[:50]  # Limit to 50 links
    
    def _get_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        images = []
        for img in soup.find_all('img', src=True):
            src = urljoin(base_url, img['src'])
            alt = img.get('alt', '')
            images.append({
                "src": src,
                "alt": alt[:100]
            })
        return images[:20]  # Limit to 20 images
    
    def _get_headings(self, soup: BeautifulSoup) -> Dict:
        return {
            "h1": [h.text.strip() for h in soup.find_all('h1')],
            "h2": [h.text.strip() for h in soup.find_all('h2')][:10],
            "h3": [h.text.strip() for h in soup.find_all('h3')][:10]
        }
    
    def _get_tables(self, soup: BeautifulSoup) -> List[Dict]:
        tables = []
        for table in soup.find_all('table'):
            headers = []
            rows = []
            
            # Get headers
            for th in table.find_all('th'):
                headers.append(th.text.strip())
            
            # Get rows
            for tr in table.find_all('tr'):
                row = [td.text.strip() for td in tr.find_all('td')]
                if row:
                    rows.append(row)
            
            if rows:
                tables.append({
                    "headers": headers,
                    "rows": rows[:20],  # Limit rows
                    "total_rows": len(rows)
                })
        
        return tables[:5]  # Limit to 5 tables
    
    def _get_lists(self, soup: BeautifulSoup) -> List[Dict]:
        lists = []
        for ul in soup.find_all(['ul', 'ol']):
            items = [li.text.strip() for li in ul.find_all('li') if li.text.strip()]
            if items:
                lists.append({
                    "type": ul.name,
                    "items": items[:20],
                    "total_items": len(items)
                })
        return lists[:10]  # Limit to 10 lists
    
    async def close(self):
        await self.client.aclose()
