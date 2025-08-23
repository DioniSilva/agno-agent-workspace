from pydantic_settings import BaseSettings


class TeamSettings(BaseSettings):
    """Team settings that can be set using environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    gemini_2_5_pro: str = "gemini-2.5-pro"
    gemini_2_5_flash: str = "gemini-2.5-flash"
    gemini_2_5_flash_lite: str = "gemini-2.5-flash-lite"
    gemma_3n_e2b_it: str = "gemma-3n-e2b-it"

    gemini_embedding_001: str = "gemini-embedding-001"

    default_max_completion_tokens: int = 16000
    default_temperature: float = 0


# Create an TeamSettings object
team_settings = TeamSettings()
