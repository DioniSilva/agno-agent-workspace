
from utils.base_agent import create_agent
from textwrap import dedent
from agno.models.google import Gemini

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.log import logger
from app_settings.settings import app_settings
from models import SearchResults

def search_agent() -> Agent:

    agent: Agent = Agent(
        model=Gemini(id=app_settings.gemini_2_5_flash_lite),
        tools=[DuckDuckGoTools(cache_results=True)],
        # tool_call_limit=3,
        name="Searcher Agent",
        agent_id="searcher_agent",
        description=dedent("""\
        You are BlogResearch-X, an elite research assistant specializing in discovering
        high-quality sources for compelling blog content. Your expertise includes:

        - Finding authoritative and trending sources
        - Evaluating content credibility and relevance
        - Identifying diverse perspectives and expert opinions
        - Discovering unique angles and insights
        - Ensuring comprehensive topic coverage\
        """),
        instructions=dedent("""\
        1. Search Strategy 🔍
           - Find 10-15 relevant sources and select the 5-7 best ones
           - Prioritize recent, authoritative content
           - Look for unique angles and expert insights
        2. Source Evaluation 📊
           - Verify source credibility and expertise
           - Check publication dates for timeliness
           - Assess content depth and uniqueness
        3. Diversity of Perspectives 🌐
           - Include different viewpoints
           - Gather both mainstream and expert opinions
           - Find supporting data and statistics\
        """),
        # response_model=SearchResults,
        # structured_outputs=True,
    )

    return agent