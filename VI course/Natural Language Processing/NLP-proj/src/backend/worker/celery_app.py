"""Конфигурация приложения Celery."""
from celery import Celery

from src.backend.core import get_settings

settings = get_settings()

celery_app = Celery(
    "gamer_passport",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["src.worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=86400,
)
