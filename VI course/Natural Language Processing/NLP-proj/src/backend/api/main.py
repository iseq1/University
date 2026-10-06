"""Точка входа в приложение FastAPI """

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.core import get_settings, HEALTHCHECK_PATH
from src.backend.utils import setup_logging


settings = get_settings()
setup_logging(settings)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Автоматическая генерация саммари профиля Steam",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(HEALTHCHECK_PATH, tags=["system"])
async def healthcheck() -> dict[str, str]:
    """Возвращает статус работоспособности приложения"""
    logger.debug("Health check requested")
    return {"status": "ok"}
