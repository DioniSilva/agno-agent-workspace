from typing import Optional

from agno.agent import Agent

from agno.tools.duckduckgo import DuckDuckGoTools

from agents.settings import agent_settings
from db.session import db_url
from utils.base_agent import create_agent
from agno.vectordb.pgvector import PgVector, SearchType
from agno.agent import AgentKnowledge


def get_sage(
    model_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    
    knowledge = AgentKnowledge(
        vector_db=PgVector(
            table_name="sage_knowledge",
            db_url=db_url,
            search_type=SearchType.hybrid,
            embedder=agent_settings.default_embedder,
        )
    )

    agent: Agent = create_agent(
        name="Sage Agent",
        prompt_path="prompts/agents/sage.yaml",
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        db_url=db_url,
        storage_table="sage_sessions",
        tools=[DuckDuckGoTools()],
        knowledge=knowledge,
    )

    # Adicione configurações adicionais que não são definidas em base_agent. 
    # Exemplo: adicionar contexto dinâmico ao agente.
    # Nesse exemplo, cada função no contexto será resolvida durante a execução do agente,
    # funcionando como uma injeção de dependências.
    # Exemplo de uso:
    # agent.context = {"get_user_details": get_user_details} <<<<<
    # onde get_user_details é uma função que obtém detalhes do usuário via api, por exemplo.
    # Para incluir o contexto nas instruções do agente:
    # agent.add_context = True <<<<<<
    # Detalhes em: https://docs.agno.ai/agents/context

    return agent