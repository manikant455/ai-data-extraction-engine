import logging
from typing import Dict, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIParser:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
    
    async def extract_structured_data(self, scraped_data: Dict, schema: Dict) -> Dict:
        """Use AI to extract structured data from scraped content"""
        
        # Fallback parser (no API key needed)
        if not self.api_key or self.api_key == "":
            return self._fallback_extraction(scraped_data, schema)
        
        # AI-powered extraction
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)
            
            prompt = self._build_extraction_prompt(scraped_data, schema)
            
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data extraction expert. Extract structured data from web content according to the schema."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return {
                "extracted_data": result,
                "method": "ai",
                "confidence": 0.9
            }
            
        except Exception as e:
            logger.error(f"AI extraction failed: {e}")
            return self._fallback_extraction(scraped_data, schema)
    
    def _build_extraction_prompt(self, data: Dict, schema: Dict) -> str:
        """Build prompt for AI extraction"""
        return f"""Extract the following information from this web content according to the schema.

Schema: {schema}

Content:
Title: {data.get('title', '')}
Description: {data.get('meta_description', '')}
Text: {data.get('text_content', '')[:2000]}
Headings: {data.get('headings', {})}

Return ONLY valid JSON matching the schema. If information is not found, use null."""
    
    def _fallback_extraction(self, data: Dict, schema: Dict) -> Dict:
        """Rule-based extraction fallback"""
        result = {}
        
        for field, field_type in schema.items():
            if field in data:
                result[field] = data[field]
            elif field == "emails":
                import re
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                                   data.get('text_content', ''))
                result[field] = list(set(emails))[:5]
            elif field == "phones":
                import re
                phones = re.findall(r'\b[\d\-\(\)\.]{7,}\b', data.get('text_content', ''))
                result[field] = phones[:5]
            elif field == "prices":
                import re
                prices = re.findall(r'\$[\d,]+\.?\d*', data.get('text_content', ''))
                result[field] = prices[:10]
            else:
                result[field] = None
        
        return {
            "extracted_data": result,
            "method": "fallback",
            "confidence": 0.5
        }
    
    async def summarize_data(self, data: Dict) -> Dict:
        """AI summary of scraped data"""
        if not self.api_key or self.api_key == "":
            return self._fallback_summary(data)
        
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)
            
            prompt = f"""Summarize this web content in 3-5 bullet points:

Title: {data.get('title', '')}
Content: {data.get('text_content', '')[:1000]}

Be concise and informative."""
            
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )
            
            return {
                "summary": response.choices[0].message.content,
                "method": "ai"
            }
            
        except Exception as e:
            return self._fallback_summary(data)
    
    def _fallback_summary(self, data: Dict) -> Dict:
        """Rule-based summary fallback"""
        text = data.get('text_content', '')
        title = data.get('title', '')
        headings = data.get('headings', {})
        
        bullets = []
        if title:
            bullets.append(f"Page Title: {title}")
        if headings.get('h1'):
            bullets.append(f"Main Heading: {headings['h1'][0]}")
        
        # First 200 chars as summary
        if text:
            bullets.append(f"Content Preview: {text[:200]}...")
        
        return {
            "summary": "\n".join(bullets) if bullets else "No content to summarize",
            "method": "fallback"
        }
