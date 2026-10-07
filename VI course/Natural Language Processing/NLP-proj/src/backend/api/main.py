"""Точка входа в приложение FastAPI """

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.core import get_settings, HEALTHCHECK_PATH
from src.backend.utils import setup_logging
from src.backend.db import init_db, close_db


settings = get_settings()
setup_logging(settings)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Инициализация и закрытие БД-ресурсов приложения"""
    logger.info("Initializing database")
    await init_db()
    logger.info("Database initialized")
    yield
    logger.info("Closing database connection")
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Автоматическая генерация саммари профиля Steam",
    lifespan=lifespan,
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
