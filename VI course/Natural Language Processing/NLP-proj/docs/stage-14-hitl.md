# Этап 14: HITL и Active Learning

При генерации `full` результаты с `critic_score < 0.65` или `validation_passed=false` попадают в SQL-очередь `uncertain_examples`. Если Critic не вернул числовую оценку, это само по себе не считается низким качеством. Порог задаётся в `src/hitl/active_learning.py`.

Роль `editor` или `admin` обязательна для всех `/api/v1/hitl/*` маршрутов.

- `GET /api/v1/hitl/queue?status=pending` — очередь.
- `POST /api/v1/hitl/{id}/approve` с `{"corrected_text":"..."}` — подтверждение и создание записи KnowledgeBase.
- `POST /api/v1/hitl/{id}/feedback` — подтверждение с обязательным исправлением.
- `POST /api/v1/hitl/{id}/reject` — отклонение.
- `POST /api/v1/hitl/reindex` — постановка задачи переиндексации Qdrant.

После подтверждения система пытается автоматически отправить задачу переиндексации в Celery. Если Redis/Celery недоступны, SQL-решение остаётся сохранённым, а `reindex_scheduled=false` сигнализирует о необходимости повторной постановки через `/reindex`. Необходим запущенный worker.

Кэш результатов LLM хранится в SQL (`Cache`), TTL 24 часа, попадания учитываются в `hits`. Задача `cleanup_cache_task` удаляет просроченные записи; её можно запускать по расписанию Celery Beat или вручную. Текущая реализация не включает автоматическое расписание Beat.

Celery задачи: `reindex_knowledge_base_task`, `cleanup_cache_task`, `generate_batch_task`, плюс задачи оценки из этапа 13.

Запуск: `poetry run celery -A src.worker.celery_app.celery_app worker --loglevel=info`. Для переиндексации необходимы Qdrant, модель эмбеддингов и база знаний.

Проверка покрытия: `poetry run pytest --cov=src --cov-report=term-missing`. Порог ≥70% должен подтверждаться на полном окружении с установленными зависимостями; при недостижении требуется расширение тестов.
