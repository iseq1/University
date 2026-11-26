# Этап 15 — интерфейс, развёртывание и сдача

## Запуск

1. Скопируйте `.env.example` в `.env`. Установите уникальные `JWT_SECRET_KEY` (не менее 32 байт), `POSTGRES_PASSWORD`, `LLM_PROVIDER` и ключ выбранного облачного провайдера (`ATRIA_API_KEY` или `SHARELLM_API_KEY`). Для импорта Steam укажите `STEAM_API_KEY`.
2. Убедитесь, что Docker Desktop запущен (Linux containers).
3. `docker compose up --build -d`
4. Откройте http://localhost:8080 (Nginx) или http://localhost:8501 (прямой Streamlit), API docs: http://localhost:8080/api/v1/... или через `docker compose exec api` / прямой API.
5. `docker compose ps`, `docker compose logs -f api worker frontend` — диагностика.

**Внимание:** `docker compose` предназначен для локальной демонстрации. Порты опубликованы только на `127.0.0.1`; TLS и публичное развёртывание требуют отдельной конфигурации. БД автоматически создаёт таблицы через `init_db()`, но в production нужны Alembic-миграции. При первом запуске эмбеддинги могут скачать модель SentenceTransformers; генеративные LLM локально не запускаются.

## Страницы

- регистрация, вход, JWT хранится в `st.session_state` (не долговременное хранилище).
- генерация и пакетная обработка (до 20 SteamID), TXT-загрузка, JSON-экспорт.
- просмотр, CRUD, CSV-импорт. Backend требует editor/admin на чтение, admin на изменение.
- проверка сомнительных результатов и переиндексация.
- метрики, история, графики Plotly, фоновое сравнение провайдеров.
- трассировка агентов и LLM по request_id.
- healthcheck и статус Celery. Статистика кэша пока не экспонирована API.

## Проверки

```bash
python -m pytest tests/unit/test_stage15_frontend.py -v
python -m pytest tests/unit -q
python -m ruff check frontend/utils tests/unit/test_stage15_frontend.py
python -m compileall -q src frontend
```

### Ручная демонстрация

1. Зарегистрировать пользователя и войти.
2. Ввести публичный SteamID64, запустить baseline и full, сравнить результаты.
3. Открыть логи по `request_id`.
4. Запустить пакет из TXT, экспортировать JSON.
5. От имени editor/admin проверить HITL, от admin — импорт CSV.
6. Запустить оценку и дождаться статуса `SUCCESS` в Celery; просмотреть историю и графики.
7. Перезапустить контейнеры, проверить сохранность данных в volumes.

## Ограничения

- Стандартный пользователь не может пользоваться административными страницами — это ожидаемое поведение RBAC.
- Реальные LLM-вызовы требуют ключа и могут тарифицироваться провайдером.
- Некоторые режимы оценки требуют предварительно подготовленного датасета в `data/generated/knowledge_base_test.json`.
- Для CI тесты не должны обращаться к реальному LLM API; если унаследованные тесты это делают, их нужно замокировать.
- Проверка `docker compose up` и end-to-end сценариев должна выполняться в среде с Docker, доступом к провайдеру и реальными ключами. В этом архиве она не заявляется как выполненная.
