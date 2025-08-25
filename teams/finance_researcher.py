from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.postgres import PostgresStorage
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

from db.session import db_url
from teams.settings import team_settings

from utils.base_agent import create_agent

def finance_agent() -> Agent:

    agent: Agent = create_agent(
        name="Finance Agent",
        prompt_path="prompts/agents/finance.yaml",
        model_id=team_settings.gemini_2_5_pro,
        tools=[DuckDuckGoTools(cache_results=True)],
        db_url=db_url,
        storage_table="finance_agent",
    )

    return agent

def web_agent() -> Agent:

    agent: Agent = create_agent(
        name="Web Agent",
        prompt_path="prompts/agents/web_agent.yaml",
        model_id=team_settings.gemini_2_5_pro,
        tools=[DuckDuckGoTools(cache_results=True)],
        db_url=db_url,
        storage_table="web_agent",
    )
    return agent


def get_finance_researcher_team(
    model_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
):
    model_id = model_id or team_settings.gemini_2_5_flash_lite
    a_web = web_agent()
    a_finance = finance_agent()

    return Team(
        name="Finance Researcher Team",
        team_id="financial-researcher-team",
        mode="route",
        members=[a_web, a_finance],
        instructions=[
            "You are a team of finance researchers!",
        ],
        session_id=session_id,
        user_id=user_id,
        description="You are a team of finance researchers!",
        model=Gemini(
            id=team_settings.gemini_2_5_pro,
            max_output_tokens=team_settings.default_max_completion_tokens,
            temperature=team_settings.default_temperature,
        ),
        success_criteria="A good financial research report.",
        enable_agentic_context=True,
        expected_output="A good financial research report.",
        storage=PostgresStorage(
            table_name="finance_researcher_team",
            db_url=db_url,
            mode="team",
            auto_upgrade_schema=True,
        ),
        debug_mode=debug_mode,
    )
