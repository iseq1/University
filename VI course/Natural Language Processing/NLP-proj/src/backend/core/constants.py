"""Константы уровня приложения"""

APP_NAME = "Gamer Passport"
API_PREFIX = "/api"
HEALTHCHECK_PATH = "/healthz"

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FILE = "logs/app.log"

LLM_PROVIDERS = (
    "ollama",
    "huggingface",
    "openai",
    "anthropic",
    "google",
    "openrouter",
)
