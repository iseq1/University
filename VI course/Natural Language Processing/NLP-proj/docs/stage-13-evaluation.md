# Этап 13 — оценка качества и сравнение моделей

## Реализовано

- `scripts/run_eval.py`: запуск экспериментов на 20/50/100 примерах, фиксированный seed, выбор провайдеров и режимов, JSON/CSV/Markdown отчёты.
- `src/evaluation/runner.py`: единый конвейер экспериментов, подготовка словарного/RAG-контекста, запуск агентов, сравнение ансамбля, агрегирование метрик и сохранение результатов.
- Режимы: `baseline`, `+dict`, `+rag`, `+agents`, `+ensemble`.
- Провайдеры: Atria и ShareLLM; учитываются только настроенные API keys.
- `GET /api/v1/evaluate/compare`: синхронное сравнение выбранных моделей и режимов.
- `POST /api/v1/evaluate/batch`: постановка пакетного сравнения в Celery.
- `GET /api/v1/evaluate/tasks/{task_id}`: получение статуса и результата фоновой задачи.
- Celery tasks: `evaluate_model_task`, `compare_models_task`.
- Redis добавлен в Docker Compose как broker/result backend.
- Результаты сохраняются в `evaluation_results` и `model_comparisons`.

## Запуск

```bash
poetry run python scripts/run_eval.py --providers atria,sharellm --modes baseline,+dict,+rag,+agents,+ensemble --sample-sizes 20,50,100
```

Для RAG предварительно запустить Qdrant, импортировать обучающую базу и выполнить `scripts/index_knowledge_base.py`.

Для Celery:

```bash
docker compose -f "ci-cd files/docker-compose.yml" up -d redis
poetry run celery -A src.worker.celery_app.celery_app worker --loglevel=info
```

## Интерпретация результатов и ограничения

Тестовый набор содержит 200 синтетических примеров. Он не должен пересекаться с обучающей базой и не является выборкой реальных Steam-профилей. Метрики BLEU, ROUGE-L, METEOR, chrF и Exact Match сравнивают сгенерированный текст с эталоном; они не гарантируют фактологическую корректность. BERTScore опционален. Бонусные bootstrap/paired t-test и доверительные интервалы пока не реализованы.

Режим `+rag` требует доступного Qdrant с предварительно проиндексированной базой знаний. `+ensemble` сравнивает настроенные облачные шлюзы по оценке Critic; если настроен только один шлюз, ансамбль фактически состоит из одного кандидата. Эксперименты расходуют API-квоты и выполняются последовательно, чтобы не создавать неконтролируемую нагрузку на провайдеров.
