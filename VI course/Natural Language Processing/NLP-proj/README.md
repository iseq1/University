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

**Этап 1 — выбор темы и настройка окружения.**
