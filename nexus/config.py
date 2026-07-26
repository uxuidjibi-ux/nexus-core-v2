from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4.1-mini"
    nexus_dry_run: bool = True
    nexus_log_level: str = "INFO"
    nexus_artifact_dir: Path = Path("artifacts")
    nexus_max_parallel_projects: int = Field(default=2, ge=1, le=4)

    notion_token: SecretStr | None = None
    notion_database_id: str | None = None
    jira_url: str | None = None
    jira_email: str | None = None
    jira_api_token: SecretStr | None = None

    figma_token: SecretStr | None = None
    figma_file_key: str | None = None

    adobe_client_id: str | None = None
    adobe_client_secret: SecretStr | None = None
    adobe_access_token: SecretStr | None = None
    firefly_api_url: str = "https://firefly-api.adobe.io/v3/images/generate"
    replicate_api_token: SecretStr | None = None
    comfyui_url: str | None = None

    wp_url: str | None = None
    wp_user: str | None = None
    wp_app_password: SecretStr | None = None
    readyai_webhook_url: str | None = None
    readyai_api_key: SecretStr | None = None
    readymag_webhook_url: str | None = None

    github_token: SecretStr | None = None
    github_repository: str | None = None
    sandbox_root: Path = Path("artifacts/sandbox")
    sandbox_timeout_seconds: int = Field(default=20, ge=1, le=120)
    social_webhook_url: str | None = None

    @field_validator("wp_url", "jira_url", "comfyui_url", mode="before")
    @classmethod
    def strip_trailing_slash(cls, value: str | None) -> str | None:
        return value.rstrip("/") if value else value

    def secret(self, name: str) -> str | None:
        value = getattr(self, name)
        return value.get_secret_value() if isinstance(value, SecretStr) else value


@lru_cache
def get_settings() -> Settings:
    return Settings()
