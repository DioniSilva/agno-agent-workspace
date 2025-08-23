from pydantic_settings import BaseSettings
from agno.embedder.google import GeminiEmbedder
from agno.models.google import Gemini



class AgentSettings(BaseSettings):
    """Agent settings that can be set using environment variables.
    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    gemini_2_5_pro: str = "gemini-2.5-pro"
    gemini_2_5_flash: str = "gemini-2.5-flash"
    gemini_2_5_flash_lite: str = "gemini-2.5-flash-lite"
    gemma_3n_e2b_it: str = "gemma-3n-e2b-it"

    gemini_embedding_001: str = "gemini-embedding-001"
    default_embedder: any = GeminiEmbedder(id=gemini_embedding_001)

    default_max_completion_tokens: int = 16000
    default_temperature: float = 0


# Create an TeamSettings object
agent_settings = AgentSettings()
