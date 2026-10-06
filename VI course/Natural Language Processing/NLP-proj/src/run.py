"""Скрипт запуска FastAPI-приложения с помощью Uvicorn"""

import uvicorn

from src.backend.core import get_settings


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.backend.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
