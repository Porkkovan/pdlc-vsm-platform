from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    app_name: str = "PDLC VSM Platform API"
    app_version: str = "1.0.0"
    debug: bool = True

    # Database — PostgreSQL (override via DATABASE_URL env var)
    database_url: str = "postgresql+asyncpg://postgres@localhost:5432/stump_db"

    # Azure OpenAI
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = "gpt-4o"
    azure_openai_api_version: str = "2024-02-15-preview"

    # Standard OpenAI (fallback if Azure not configured)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    @property
    def use_azure(self) -> bool:
        return bool(self.azure_openai_api_key and self.azure_openai_endpoint)

    # ALM defaults
    jira_url: str = ""
    jira_username: str = ""
    jira_api_token: str = ""

    ado_org_url: str = ""
    ado_personal_access_token: str = ""

    class Config:
        env_file = str(BASE_DIR / ".env")
        extra = "ignore"


settings = Settings()
