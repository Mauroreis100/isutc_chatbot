import os
import json
import asyncio
from typing import Dict
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlResult, CrawlerRunConfig, DefaultMarkdownGenerator, LLMConfig, PruningContentFilter
from crawl4ai import LLMExtractionStrategy
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Google GenAI config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if GEMINI_API_KEY:
    genai_client = genai.Client(api_key=GEMINI_API_KEY)
    print("Initialized Google GenAI client.")
else:
    genai_client = None


import asyncio
from openai import OpenAI
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    DefaultMarkdownGenerator,
    PruningContentFilter,
    CrawlResult,
)

# Set your OpenAI API key 


# ── Function: Summarize/Clean Data via ChatGPT ─────────────────────────────────
def summarize_with_gemini(markdown_text: str) -> str:
    prompt = (
        "Extraia informação relevante para a criação de um sistema RAG do ISUTC "
        f"do texto HTML:\n\n{markdown_text}"
    )

    response = genai_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=types.Part.from_text(text=prompt),
            config=types.GenerateContentConfig(
                temperature=0,
                top_p=0.95,
                top_k=20,
            ),
        ) 
    return response.text if response else "❌ Google GenAI returned no result."
# ── Main Async Function ────────────────────────────────────────────────────────
async def main():
    # 1. Configure headless browser
    browser_cfg = BrowserConfig(
        headless=True,
        verbose=True,
    )    # 2. Initialise crawler
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        run_cfg = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Force fresh requests
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter()
            ),
        )
        
        # 3. Perform crawl
        result: CrawlResult = await crawler.arun(
            url="https://www.isutc.ac.mz/?p=12455",
            config=run_cfg,
        )        # 4. Check content and pass to summarizer
        if result and result.markdown:
            markdown_data = result.markdown
            
            with open("isutc_candidaturas_licenciaturas_online_outras_provincias.md", "w", encoding="utf-8") as f:
                f.write(markdown_data)
            
            # 2. Extrair links internos para crawling recursivo (opcional)
            links = result.links.get("internal", [])
            print(f"Encontrados {len(links)} links internos para explorar.")
            
            summary = summarize_with_gemini(markdown_data)
            print(summary)
            return markdown_data
        
        else:
            print(f"Erro na extração: {result.error_message}")
            print("❌ No content extracted – check page access.")
# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(main())