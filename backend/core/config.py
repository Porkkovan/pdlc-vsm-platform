from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    app_name: str = "PDLC VSM Platform API"
    app_version: str = "1.0.0"
    debug: bool = True

    # Database
    database_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/database/vsm.db"

    # OpenAI (optional — falls back to rule-based)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # ALM defaults
    jira_url: str = ""
    jira_username: str = ""
    jira_api_token: str = ""

    ado_org_url: str = ""
    ado_personal_access_token: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
