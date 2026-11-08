"""Выбор облачного LLM-шлюза"""

import logging
import time
from functools import lru_cache
from typing import Any

from src.backend.core import get_settings
from src.backend.gateways.llm.client import AtriaClient, ShareLLMClient, SberClient
from src.backend.gateways.llm.logger import log_llm_call


logger = logging.getLogger(__name__)
SUPPORTED_PROVIDERS = ("atria", "sharellm", 'sber')


class LLMGateway:
    """Единая точка входа для удаленных API-шлюзов LLM"""

    def __init__(self, provider: str | None = None, client: Any | None = None) -> None:
        self.settings = get_settings()
        self.provider = (provider or self.settings.llm_provider_base).strip().lower()
        self._client = client


    @property
    def model_name(self) -> str:
        """Получение наименования модели"""
        return str(getattr(self._get_client(), "model", self.provider))


    @staticmethod
    def _secret(value: Any) -> str:
        """Получение секрета"""
        return value.get_secret_value() if value else ""


    def _get_client(self) -> Any:
        """Получение API-клиента"""

        if self._client is not None:
            return self._client

        settings = self.settings

        if self.provider == 'sber':
            key = self._secret(settings.sber_auth_key)
            if not key:
                raise ValueError(
                    "Параметр SBER_AUTH_KEY обязателен, если LLM_PROVIDER=sber"
                )

            self._client = SberClient(
                api_key=key,
                model=settings.sber_model_base,
                base_url=settings.sber_base_url,
                timeout=settings.llm_timeout,
            )

        elif self.provider == "atria":
            key = self._secret(settings.atria_api_key)
            if not key:
                raise ValueError(
                    "Параметр ATRIA_API_KEY обязателен, если LLM_PROVIDER=atria"
                )

            self._client = AtriaClient(
                api_key=key,
                model=settings.atria_model,
                base_url=settings.atria_base_url,
                timeout=settings.llm_timeout,
            )

        elif self.provider == "sharellm":
            key = self._secret(settings.sharellm_api_key)
            if not key:
                raise ValueError(
                    "Параметр SHARELLM_API_KEY обязателен, если LLM_PROVIDER=sharellm"
                )

            self._client = ShareLLMClient(
                api_key=key,
                model=settings.sharellm_model,
                base_url=settings.sharellm_base_url,
                timeout=settings.llm_timeout,
            )

        else:
            raise ValueError(
                f"Неподдерживаемый LLM_PROVIDER: {self.provider}. "
                f"Поддерживаемы облачные шлюзы: {', '.join(SUPPORTED_PROVIDERS)}"
            )
        return self._client


    async def generate(
        self,
        prompt: str,
        *,
        agent_name: str = "unknown",
        request_id: str = "",
    ) -> str:
        """Генерация текст и лог метаданных об запросе"""

        client = self._get_client()
        model_name = str(getattr(client, "model", self.provider))

        started = time.perf_counter()
        response: str | None = None
        status = "success"

        try:
            response = await client.call(prompt)
            if not isinstance(response, str) or not response.strip():
                raise ValueError(
                    "Провайдер LLM вернул пустой ответ"
                )
            return response.strip()

        except Exception:
            status = "error"
            logger.exception(
                "LLM-генерация закончилась с ошибкой: provider=%s model=%s",
                self.provider,
                model_name
            )
            raise

        finally:
            await log_llm_call(
                request_id=request_id,
                agent_name=agent_name,
                model_name=model_name,
                provider=self.provider,
                prompt=prompt,
                response=response,
                latency_ms=round((time.perf_counter() - started) * 1000, 2),
                status=status,
            )


@lru_cache(maxsize=1)
def get_llm_gateway() -> LLMGateway:
    """Получение LLM-шлюза"""
    return LLMGateway()
