import logging
from textwrap import dedent
from typing import Any, Dict, List, Optional, Tuple
from os import getenv

from agno.agent import Agent, AgentKnowledge
from agno.models.google import Gemini
from utils.model_factory import create_model
from agno.storage.agent.postgres import PostgresAgentStorage
from agents.settings import agent_settings

from utils.prompt_loader import render_prompt, PromptKey


def _create_identity(name: str) -> Tuple[str, str]:
    agent_name = name
    agent_id = agent_name.replace(" ", "_").lower()
    return agent_name, agent_id


def _build_storage(table_name: str, db_url: str, auto_upgrade_schema: bool = True):
    return PostgresAgentStorage(
        table_name=table_name, db_url=db_url, auto_upgrade_schema=auto_upgrade_schema
    )


def create_agent(
    name: str,
    prompt_path: str,
    model_id: Optional[str],
    db_url: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    tools: Optional[List[Any]] = None,
    storage_table: Optional[str] = None,
    knowledge: Optional[AgentKnowledge] = None,
    defaults: Optional[Dict[str, Any]] = None,
    model_kwargs: Optional[Dict[str, Any]] = None,
    user_query: Optional[str] = None
) -> Agent:
    """Create a standardized Agent instance.

    Minimal opinionated factory to reduce duplication across agent modules.
    """
    tools = tools or []
    defaults = defaults or {}

    agent_name, agent_id = _create_identity(name)
    debug_mode: bool = getenv("DEBUG_MODE", "False")

    # determine default model if not provided
    if model_id is None:
        try:
            from agents.settings import agent_settings

            model_id = agent_settings.gemini_2_5_flash
        except Exception:
            model_id = "gemini-2.5-flash"

    prompts, metadata = render_prompt(
        path=prompt_path,
        model=model_id,
        user_id=user_id,
        user_query=user_query,
    )

    logging.debug(f"Prompts loaded for agent {agent_name}: {prompts}")

    agent_description = prompts.get(PromptKey.DESCRIPTION)
    agent_goal = prompts.get(PromptKey.GOAL)
    agent_system_prompt = prompts.get(PromptKey.SYSTEM_MESSAGE)
    agent_instructions = prompts.get(PromptKey.INSTRUCTIONS)
    agent_expected_output = prompts.get(PromptKey.EXPECTED_OUTPUT)

    model = create_model(
        model_id,
        **(model_kwargs or {}),
        #max_output_tokens=agent_settings.default_max_completion_tokens,
        #temperature=agent_settings.default_temperature,
    )

    storage = None
    if storage_table:
        storage = _build_storage(
            table_name=storage_table,
            db_url=db_url,
            auto_upgrade_schema=defaults.get("auto_upgrade_schema", True),
        )

    return Agent(
        name=agent_name,
        agent_id=agent_id,
        user_id=user_id,
        session_id=session_id,
        model=model,
        tools=tools,
        storage=storage,
        knowledge=knowledge,
        description=agent_description,
        instructions=agent_instructions,
        goal=agent_goal,
        system_message=agent_system_prompt,
        expected_output=agent_expected_output,
        markdown=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=3,
        read_chat_history=True,
        debug_mode=debug_mode,
    )
