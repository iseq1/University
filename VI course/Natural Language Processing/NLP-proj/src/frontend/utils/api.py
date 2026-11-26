"""Компактная типизированная HTTP-обертка для Streamlit"""
from __future__ import annotations

import os
from typing import Any

import httpx


class APIError(RuntimeError):
    """Безопасный, понятный человеку вариант сообщения об ошибке API"""


class APIClient:
    """Класс-обертка для использования API"""


    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = (base_url or os.getenv("API_BASE_URL", "http://localhost:8000")).rstrip("/")
        self.token = token


    def request(self, method: str, path: str, *, json: Any = None, params: dict | None = None) -> Any:
        """Формирование API-запроса"""

        headers = {
            "Authorization": f"Bearer {self.token}"
        } if self.token else {}

        try:
            with httpx.Client(base_url=self.base_url, timeout=180.0) as client:
                response = client.request(
                    method,
                    path,
                    json=json,
                    params=params,
                    headers=headers
                )

                response.raise_for_status()

                if response.status_code == 204 or not response.content:
                    return None

                return response.json()

        except httpx.HTTPStatusError as exc:

            try:
                detail = exc.response.json().get("detail", exc.response.text)

            except ValueError:
                detail = exc.response.text

            raise APIError(
                f"HTTP {exc.response.status_code}: {detail}"
            ) from exc

        except httpx.RequestError as exc:
            raise APIError(
                f"API недоступен: {exc}"
            ) from exc


    def get(self, path: str, **kwargs: Any) -> Any:
        """Формирование GET-запроса"""
        return self.request("GET", path, **kwargs)


    def post(self, path: str, **kwargs: Any) -> Any:
        """Формирование POST-запроса"""
        return self.request("POST", path, **kwargs)


    def put(self, path: str, **kwargs: Any) -> Any:
        """Формирование PUT-запроса"""
        return self.request("PUT", path, **kwargs)


    def delete(self, path: str, **kwargs: Any) -> Any:
        """Формирование DELETE-запроса"""
        return self.request("DELETE", path, **kwargs)
