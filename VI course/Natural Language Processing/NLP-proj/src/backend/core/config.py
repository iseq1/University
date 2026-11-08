"""Конфигурация приложения"""

from functools import lru_cache

from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


DIR = Path(__file__).resolve()
BASE_DIR = DIR.parents[2]
CERT_PATH = DIR.parents[3] / "certs"


class Settings(BaseSettings):
    """Настройки приложения для внутренних и внешних сервисов"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(default="Gamer Passport", validation_alias="APP_NAME")
    app_version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    host: str = Field(default="127.0.0.1", validation_alias="HOST")
    port: int = Field(default=8000, validation_alias="PORT")

    database_url: str = Field(
        default=f"sqlite+aiosqlite:///{BASE_DIR / 'gamer_passport.db'}",
        validation_alias="DATABASE_URL",
    )

    rus_certs: str = Field(default=f"{CERT_PATH / 'russian_trusted_root_ca_pem.crt'}", validation_alias="RUS_CERTS")

    # LLM-провайдер (API-only)
    llm_provider_base: str = Field(default="sber", validation_alias="LLM_PROVIDER_BASE")
    llm_provider_spare: str = Field(default="share_llm", validation_alias="LLM_PROVIDER_SPARE")
    llm_provider_test: str = Field(default="atria", validation_alias="LLM_PROVIDER_TEST")
    llm_timeout: float = Field(default=120.0, validation_alias="LLM_TIMEOUT")

    # ATRIA LLM-client
    atria_api_key: SecretStr | None = Field(default=None, validation_alias="ATRIA_API_KEY")
    atria_base_url: str = Field(default="https://api.atria-asi.ai/v1", validation_alias="ATRIA_BASE_URL")
    atria_model: str = Field(default="Atria-Dawn", validation_alias="ATRIA_MODEL")

    # ShareLLM LLM-client
    sharellm_api_key: SecretStr | None = Field(default=None, validation_alias="SHARELLM_API_KEY")
    sharellm_base_url: str = Field(default="https://sharellm.net/v1", validation_alias="SHARELLM_BASE_URL")
    sharellm_model_kimi: str = Field(default="kimi-k3", validation_alias="SHARELLM_MODEL_KIMI")
    sharellm_model_deepseek: str = Field(default="deepseek-v4.1-flash-1017", validation_alias="SHARELLM_MODEL_DEEPSEEK")
    sharellm_model_gpt: str = Field(default="gpt-6-astra", validation_alias="SHARELLM_MODEL_GPT")
    sharellm_model_qwen: str = Field(default="qwen3.8-flash", validation_alias="SHARELLM_MODEL_QWEN")
    sharellm_model_gemini: str = Field(default="gemini-4-argon", validation_alias="SHARELLM_MODEL_GEMINI")
    sharellm_model_spark: str = Field(default="spark-x2.6", validation_alias="SHARELLM_MODEL_SPARK")

    # SberTech LLM-client
    sber_auth_key: SecretStr | None = Field(default=None, validation_alias="SBER_AUTH_KEY")
    sber_base_url: str = Field(default="https://api.giga.chat/v1", validation_alias="SBER_BASE_URL")
    sber_model_base: str = Field(default="GigaChat-2", validation_alias="SBER_MODEL_BASE")
    sber_model_max: str = Field(default="GigaChat-2-Max", validation_alias="SBER_MODEL_MAX")
    sber_model_pro: str = Field(default="GigaChat-2-Pro", validation_alias="SBER_MODEL_PRO")
    sber_model_light: str = Field(default="GigaChat-3-Lightning", validation_alias="SBER_MODEL_LIGHT")
    sber_model_pro_plus: str = Field(default="GigaChat-3-Pro", validation_alias="SBER_MODEL_PRO_PLUS")
    sber_model_ultra: str = Field(default="GigaChat-3-Ultra", validation_alias="SBER_MODEL_ULTRA")

    qdrant_url: str = Field(default="http://localhost:6333", validation_alias="QDRANT_URL")
    qdrant_api_key: SecretStr | None = Field(default=None, validation_alias="QDRANT_API_KEY")
    qdrant_collection: str = Field(default="gamer_passport", validation_alias="QDRANT_COLLECTION")

    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")

    jwt_secret_key: SecretStr = Field(
        default=SecretStr("change-me-in-production"),
        validation_alias="JWT_SECRET_KEY",
    )
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", validation_alias="LOG_FILE")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Получение настроек конфигурации приложения"""
    return Settings()


settings = get_settings()
