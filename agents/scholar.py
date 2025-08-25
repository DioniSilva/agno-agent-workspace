from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools

from agents.settings import agent_settings
from db.session import db_url
from utils.base_agent import create_agent


def get_scholar(
    model_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    user_query: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    
    additional_context = ""

    if user_id:
        additional_context += f"""
        <context>
            You are interacting with the user: {user_id}
        </context>
        """

    agent: Agent = create_agent(
        name="Scholar Agent",
        prompt_path="prompts/agents/scholar.yaml",
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        db_url=db_url,
        tools=[DuckDuckGoTools()],
        storage_table="scholar_sessions",
        knowledge=None,
        user_query=user_query,
    )

    agent.context = additional_context

    return agent

