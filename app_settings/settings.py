from os import getenv
from pydantic_settings import BaseSettings
from pydantic import SkipValidation, Field
from typing import Any, ClassVar, Type
from agno.embedder.google import GeminiEmbedder
from agno.models.google import Gemini


class AppSettings(BaseSettings):
    """Settings that can be set using environment variables.
    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # Chaves de API
    gemini_api_key: str = getenv("GOOGLE_API_KEY", " ")

    # Modelos disponíveis
    gemini_2_5_pro: str = "gemini-2.5-pro"
    gemini_2_5_flash: str = "gemini-2.5-flash"
    gemini_2_5_flash_lite: str = "gemini-2.5-flash-lite"
    gemma_3n_e2b_it: str = "gemma-3n-e2b-it"

    # Configurações de embeddings
    gemini_embedding_001: str = "gemini-embedding-001"
    default_embedder: SkipValidation[GeminiEmbedder] = Field(
        default_factory=lambda: GeminiEmbedder(id="gemini-embedding-001")
    )

    # Configurações de geração
    default_max_completion_tokens: int = 16000
    default_temperature: float = 0

    # Configuração para uso em logging e metadados
    app_name: ClassVar[str] = "agent-app"
    app_version: ClassVar[str] = "0.1.0"

    class Config:
        """Configuração da classe Pydantic Settings."""

        env_prefix = "AGENT_APP_"
        case_sensitive = False
        validate_assignment = True


# Instância global das configurações
app_settings = AppSettings()
