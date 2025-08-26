from enum import Enum
from typing import List, Optional

from agents.sage import get_sage
from agents.scholar import get_scholar
from agents.article_scraper import article_scraper
from agents.writer import writer
from agents.searcher import search_agent


class AgentType(Enum):
    SAGE = "sage"
    SCHOLAR = "scholar"
    ARTICLE_SCRAPER = "article_scraper"
    WRITER = "writer"
    SEARCHER = "searcher"

# Use Factory Pattern to improve agent instantiation
class AgentFactory:
    @staticmethod
    def create(agent_id, **kwargs):
        factories = {
            AgentType.SAGE: lambda: get_sage(**kwargs),
            AgentType.ARTICLE_SCRAPER: lambda: article_scraper(),
            AgentType.WRITER: lambda: writer(),
            AgentType.SEARCHER: lambda: search_agent(),
            AgentType.SCHOLAR: lambda: get_scholar(**kwargs),
        }
        factory = factories.get(agent_id)
        if factory:
            return factory()
        raise ValueError(f"Unknown agent_id: {agent_id}")


def get_available_agents() -> List[str]:
    """Returns a list of all available agent IDs."""
    return [agent.value for agent in AgentType]


def get_agent(
    model_id: str = "gemini-2.5-flash-lite",
    agent_id: Optional[AgentType] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
):
    kwargs = dict(model_id=model_id, user_id=user_id, session_id=session_id, debug_mode=debug_mode)
    return AgentFactory.create(agent_id, **kwargs)
    