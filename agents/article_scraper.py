
from utils.base_agent import create_agent
import json
from textwrap import dedent
from typing import Dict, Iterator, Optional
from agno.models.google import Gemini

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.log import logger
from app_settings.settings import app_settings
from models import ScrapedArticle

def article_scraper() -> Agent:

    agent: Agent = Agent(
        model=Gemini(id=app_settings.gemini_2_5_flash),
        name="Article Scraper",
        agent_id="article_scraper",
        tools=[],
        description=dedent("""\
        You are ContentBot-X, a specialist in extracting and processing digital content
        for blog creation. Your expertise includes:

        - Efficient content extraction
        - Smart formatting and structuring
        - Key information identification
        - Quote and statistic preservation
        - Maintaining source attribution\
        """),
        instructions=dedent("""\
        1. Content Extraction 📑
           - Extract content from the article
           - Preserve important quotes and statistics
           - Maintain proper attribution
           - Handle paywalls gracefully
        2. Content Processing 🔄
           - Format text in clean markdown
           - Preserve key information
           - Structure content logically
        3. Quality Control ✅
           - Verify content relevance
           - Ensure accurate extraction
           - Maintain readability\
        """),
        # response_model=ScrapedArticle,
        # structured_outputs=True,
    )

    return agent