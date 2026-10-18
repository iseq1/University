# Геймерский паспорт 2.0

Автоматическая генерация саммари профиля Steam на основе игровых данных пользователя.

## Цель проекта

Разработать интеллектуальную NLP-систему, которая получает данные Steam-профиля и формирует краткое информативное саммари игрового профиля пользователя. Система должна использовать мультиагентную архитектуру, RAG, несколько вариантов LLM и автоматическую оценку качества результата.

## Основные требования проекта

- мультиагентная архитектура: минимум 3 агента + Supervisor;
- самостоятельная реализация логики агентов и оркестрации без LangChain/LangGraph;
- RAG с гибридным поиском BM25 + векторный поиск;
- поддержка Ollama и HuggingFace Transformers, а также внешних LLM API;
- REST API на FastAPI;
- асинхронная обработка, Redis и Celery;
- Human-in-the-Loop;
- хранение reasoning log и трассировки LLM-вызовов;
- оценка качества на выборках 20, 50 и 100 образцов;
- Docker-контейнеризация;
- тестирование через pytest;
- UI на Streamlit.

## Структура проекта

```text
gamer-passport/
├── ci-cd files/           # Docker и CI/CD-конфигурация
├── data/                   # импортируемые и локальные данные
├── src/                   # исходный код приложения
│   ├── backend/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── core/
│   │   ├── data/
│   │   ├── db/
│   │   ├── evaluation/
│   │   ├── hitl/
│   │   ├── retrieval/
│   │   ├── utils/
│   │   └── worker/
│   ├── frontend/
│   ├── tests/                 # unit/integration tests
│   └── scripts/               # служебные скрипты
├── pyproject.toml         # Poetry и зависимости
├── .gitignore
└── README.md
```

`pyproject.toml` находится в корне, поскольку это стандартная точка входа Poetry; Docker/CI-CD-файлы размещаются в `ci-cd files/`.

## Стек

- Python 3.11+
- FastAPI + Uvicorn
- Pydantic Settings
- SQLAlchemy async + PostgreSQL / SQLite
- Alembic
- Redis + Celery
- Qdrant
- BM25 (`rank-bm25`)
- Sentence Transformers
- HuggingFace Transformers
- Ollama
- Streamlit
- pytest / pytest-asyncio / pytest-cov
- Docker

## Метрики качества

Предварительный набор метрик:

- BLEU
- ROUGE-L
- METEOR
- chrF
- BERTScore

Конкретный набор и способ формирования эталонных саммари будут уточнены на этапе разработки системы оценки.

## Установка

Требуется Poetry.

```bash
poetry install
poetry run pytest
```

## Статус

## Этап 1 — выбор темы и настройка окружения.



## Этап 2 — архитектура и каркас приложения

Реализованы:

- конфигурация через `pydantic-settings` и переменные окружения;
- параметры БД, LLM, Qdrant, Redis, JWT и внешних API;
- базовые константы и исключения;
- FastAPI-приложение;
- CORS;
- endpoint `GET /healthz`;
- запуск через `run.py`;
- логирование одновременно в консоль и файл с ротацией;
- smoke-тест healthcheck.

Пока не реализованы БД, агенты, RAG, Celery и LLM-клиенты — они относятся к следующим этапам ТЗ.

### Запуск

```bash
poetry install
cp .env.example .env
poetry run python run.py
```

Проверка:

```text
GET http://127.0.0.1:8000/healthz
```

Ожидаемый ответ:

```json
{"status": "ok"}
```

## Этап 3 — база данных

Реализованы:

- асинхронный SQLAlchemy engine и `AsyncSession`;
- автоматическое создание таблиц при запуске FastAPI;
- модели `users`, `knowledge_base`, `glossary`, `uncertain_examples`, `cache`, `evaluation_results`, `model_comparisons`;
- таблицы `reasoning_logs` и `llm_calls` для трассировки агентов и LLM-вызовов;
- SQLite для локальной разработки;
- PostgreSQL через `ci-cd files/docker-compose.yml`;
- тесты схемы базы данных.

## Этап 4 — аутентификация и авторизация

Реализованы: 
- bcrypt-хеширование и проверка паролей;
- JWT access token с указанием пользователя и роли;
- `POST /auth/register`;
- `POST /auth/login`;
- `GET /auth/me`;
- зависимости `get_current_user`, `require_editor`, `require_admin`;
- роли `user`, `editor`, `admin`;
- unit-тесты security и auth с моками сессии БД.

Для запуска API требуется установить зависимости Poetry из `pyproject.toml`.

## Этап 5 — Base Agent + Supervisor

Реализованы:

- абстрактный асинхронный интерфейс `Agent.process(state)`;
- `Supervisor` с ленивой инициализацией агентов;
- последовательное выполнение агентов с общим словарём состояния;
- остановка по `state["done"]` или по лимиту итераций;
- сохранение успешных и неуспешных шагов в `reasoning_logs`;
- unit-тесты оркестрации с моками агентов и сессии БД.

Агенты пока демонстрационные в тестах: подключение реальных LLM и бизнес-логики выполняется на последующих этапах.
