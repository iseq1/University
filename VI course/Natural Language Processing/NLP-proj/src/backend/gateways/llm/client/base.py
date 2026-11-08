"""Базовый HTTP-клиент для поддерживаемых облачных шлюзов LLM"""

from typing import Any

import httpx


class BaseClient:
    """Базовый клиент для шлюзов, предоставляющих доступ через протокол OpenAI Chat Completions"""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        *,
        timeout: float = 120.0,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.extra_headers = extra_headers or {}


    def get_headers(self) -> dict[str, str]:
        """Формирование заголовка запроса"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            **self.extra_headers,
        }


    def get_payload(self, prompt: str) -> Any:
        """Формирование тела запроса"""
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "stream": False,
        }


    async def call(self, prompt: str) -> str:
        """Вызов модели"""

        headers = self.get_headers()
        payload = self.get_payload(prompt)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
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
