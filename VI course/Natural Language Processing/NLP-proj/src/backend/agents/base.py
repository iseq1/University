"""Базовый интерфейс для агентов асинхронной обработки"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class Agent(ABC):
    """Общий интерфейс для всех агентов в конвейере обработки"""

    name: str = "agent"

    @abstractmethod
    async def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Обработка общего состояния и получение его обновленного значения"""


AgentFactory = Callable[[], Agent]
