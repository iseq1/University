import ssl
import time
from typing import Any

import httpx

from src.backend.gateways.llm.client.base import BaseClient
from src.backend.core import get_settings
from src.backend.utils.utils import make_uuid


class SberClient(BaseClient):
    """Адаптер шлюза-Sber"""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        timeout: float = 120.0
    ) -> None:

        self.oauth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.ssl_context = ssl.create_default_context(cafile=get_settings().rus_certs)
        self.oauth_params = {}
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout=timeout
        )


    def _get_access_headers(self) -> dict[str, str]:
        """Формирование заголовка для запроса-аутентификации"""
        return {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'RqUID': make_uuid(),
          'Authorization': f'Bearer {self.api_key}'
        }


    async def _get_access_token(self):
        """Авторизация в сервисе Сбера"""

        async with httpx.AsyncClient(
            timeout=self.timeout,
            verify=self.ssl_context
        ) as client:
            response = await client.post(
                url=self.oauth_url,
                headers=self._get_access_headers(),
                data={'scope': 'GIGACHAT_API_PERS'},
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()

        try:
            access_token = data["access_token"]
            expires_at = data["expires_at"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError(
                "LLM-шлюз авторизации вернул неожиданный ответ"
            ) from exc

        if not isinstance(access_token, str) or not access_token.strip():
            raise ValueError(
                "LLM-шлюз вернул пустой ответ"
            )

        self.oauth_params["access_token"] = access_token
        self.oauth_params["expires_at"] = expires_at


    async def call(self, prompt: str) -> str:
        """Вызов модели"""

        if not self.oauth_params or self.oauth_params["expires_at"] < time.time():
            await self._get_access_token()

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.oauth_params["access_token"]}'
        }
        payload = self.get_payload(prompt)

        async with httpx.AsyncClient(
            timeout=self.timeout,
            verify=self.ssl_context
        ) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError(
                "LLM-шлюз вернул неожиданный ответ"
            ) from exc

        if not isinstance(content, str) or not content.strip():
            raise ValueError(
                "LLM-шлюз вернул пустой ответ"
            )

        return content.strip()
