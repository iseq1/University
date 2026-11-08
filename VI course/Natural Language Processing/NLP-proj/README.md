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

## Этап 6 — Validator

Реализован `ValidatorAgent` с проверками:

- наличие обязательных полей (по умолчанию — `steam_id`);
- минимальная длина `input_text` и `summary`, если эти поля переданы;
- дубликаты в списке `items`;
- неизвестные термины в `terms` при переданном словаре (формируются предупреждения);
- опциональная заглушка LLM-проверки с логированием, без вызова внешней модели.

Результат агента — поля `errors`, `warnings` и `validation_passed` в общем состоянии. 

## Этап 7 — Critic LLM-as-a-Judge

Реализован `CriticAgent` (`src/agents/critic.py`), который оценивает саммари профиля Steam по релевантности, полноте и стилю. Агент формирует few-shot prompt, проверяет структуру и диапазоны JSON-оценки и возвращает `critic_score`, `critic_reasoning`, `critic_suggestions`, `critic_passed` и оценки по отдельным критериям в `critic_dimensions`.

Реальный вызов модели пока оставлен заглушкой: до этапа 11 используется резервная оценка 5.0 с пояснением и рекомендацией повторить проверку после настройки LLM. Добавлены unit-тесты корректного ответа, fallback и обработки невалидного JSON.

## Этап 8 — Editor

Реализован `EditorAgent` (`src/agents/editor.py`), который использует ошибки `Validator` и рекомендации `Critic` для подготовки исправленного саммари. Если ошибок и рекомендаций нет, вызов модели пропускается. Ответ редактора проверяется: ожидается JSON-объект с непустым полем `summary`. Поле `editor_changed` отражает, изменился ли текст. Если вызов LLM недоступен или ответ некорректен, исходный текст сохраняется, а ошибка записывается в `editor_error`. Реальный вызов LLM подключается на этапе 11. Добавлены unit-тесты успешного исправления, пропуска вызова, fallback и разбора ответа.

## Этап 9 — подготовка и импорт данных

Добавлены скрипты:

- `scripts/generate_data.py` — воспроизводимо создаёт синтетическую обучающую выборку (по умолчанию 1000 примеров), отдельную тестовую выборку (200 примеров) и глоссарий (565 уникальных контекстных записей); сохраняет каждый набор в JSON и CSV;
- `scripts/import_data.py` — асинхронно загружает обучающую выборку в `knowledge_base` и термины в `glossary` через SQLAlchemy. Повторно существующие примеры и термины пропускаются без учёта регистра;
- `data/source/README.md` — описывает происхождение и ограничения демонстрационных данных;
- `data/generated/` — созданные JSON/CSV-файлы и метаданные набора.

**Важно:** все профили в текущем наборе синтетические и не получены из Steam. Глоссарий демонстрационный; контекстные варианты терминов помогают проверить импорт и поиск, но не являются независимыми экспертными аннотациями. Тестовая выборка не импортируется в базу знаний и не пересекается с обучающей по полю `source_text`.

### Генерация и проверка данных

```bash
poetry run python scripts/generate_data.py
poetry run pytest tests/unit/test_data_pipeline.py
```

### Импорт в БД

Перед импортом настройте `DATABASE_URL` в `.env` и убедитесь, что PostgreSQL запущен либо выбран локальный SQLite:

```bash
poetry run python scripts/import_data.py
```

Повторный запуск генерации создаёт те же данные с теми же параметрами. Повторный запуск импорта не должен добавлять уже имеющиеся записи. Для другого размера выборки используйте `--train-count` и `--test-count`; для другого каталога — `--output-dir`, а при импорте — `--data-dir`.

## Этап 10 — RAG и гибридный поиск

Реализованы компоненты retrieval-контура в `src/retrieval/`:

- `documents.py` — единая структура `RetrievedDocument`;
- `embeddings.py` — лениво загружаемый singleton-обёртка Sentence Transformers; модель по умолчанию `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`;
- `bm25.py` — лексический поиск BM25 по тексту профиля;
- `qdrant_store.py` — асинхронное создание коллекции, пакетная загрузка векторов и семантический поиск в Qdrant;
- `hybrid.py` — объединение ранжированных списков BM25 и Qdrant методом Reciprocal Rank Fusion (RRF);
- `service.py` — загрузка примеров из SQLAlchemy `knowledge_base` и создание retriever.

Векторизация и подключение к Qdrant выполняются лениво: импорт модулей и unit-тесты не требуют запущенного Qdrant или скачивания модели. В обычном окружении проекта используются зависимости `sentence-transformers`, `qdrant-client` и `rank-bm25`. Для минимального окружения в `BM25Retriever` предусмотрен совместимый fallback BM25, если `rank-bm25` ещё не установлен.

### Запуск индексации

1. Запустите PostgreSQL/SQLite и импортируйте данные этапа 9:

```bash
poetry run python scripts/import_data.py
```

2. Запустите Qdrant (например, через Docker):

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

3. При необходимости задайте в `.env` `QDRANT_URL`, `QDRANT_COLLECTION` и `EMBEDDING_MODEL`, затем постройте индекс:

```bash
poetry run python scripts/index_knowledge_base.py --batch-size 64
```

4. Пример использования гибридного поиска из асинхронного кода:

```python
from src.retrieval.service import build_retriever

retriever = await build_retriever(session)
results = await retriever.search(profile_text, limit=5)
for document, score in results:
    print(document.target_text, score)
```

RRF использует вклад `1 / (k + rank)` для каждого списка результатов, поэтому не смешивает напрямую несопоставимые BM25- и cosine-оценки. Индексация использует стабильные UUID от ID записи БД: повторный запуск обновляет те же точки, а не создаёт дубликаты.

### Проверка

```bash
poetry run pytest tests/unit/test_retrieval.py
```

Unit-тесты используют подменные embedder и vector store, поэтому не требуют загрузки нейросети и работающего Qdrant. Реальная индексация и семантический поиск требуют установленных зависимостей, доступного Qdrant и скачанной модели Sentence Transformers.

## Этап 11 — интеграция облачных LLM API и трассировка вызовов

Генерация текста выполняется **только через API**. Локальная загрузка/запуск LLM не используется: Ollama, Hugging Face Transformers, OpenAI API, OpenRouter, Anthropic и Google Generative AI исключены из списка рабочих LLM-провайдеров этого проекта.

Поддерживаются три OpenAI-compatible шлюза:

- **Atria** — `https://api.atria-asi.ai/v1`, модель по умолчанию `Atria-Dawn`;
- **ShareLLM** — `https://sharellm.net/v1`, модель задаётся по точному ID из каталога аккаунта.
- **GigaChat** — `https://api.giga.chat/v1`, модель задаётся по точному ID из каталога аккаунта.

`src/llm/clients.py` содержит общий асинхронный HTTP-клиент Chat Completions и адаптеры `AtriaClient` / `ShareLLMClient` / `SberClient`. `src/llm/gateway.py` выбирает один шлюз через `LLM_PROVIDER`, получает секреты из `.env` и выполняет генерацию. Critic и Editor используют этот менеджер; Validator может выполнять дополнительную проверку при `enable_llm_check=True`.

Метаданные вызовов сохраняются в `llm_calls`: имя агента, провайдер/модель, SHA-256 хеши промпта и ответа, задержка и статус. Содержимое промптов и ответов в БД не сохраняется. Ошибка записи лога не должна ломать основной вызов модели.

### Быстрый запуск

1. Скопируйте `.env.example` в `.env`.
2. Получите API-ключ выбранного шлюза и проверьте доступность бесплатной квоты.
3. Заполните конфиг:
   * Для Atria заполните `ATRIA_API_KEY`, `ATRIA_MODEL`; 
   * Для ShareLLM — `SHARELLM_API_KEY`, `SHARELLM_MODEL`;
   * Для GigaChat — `SBER_AUTH_KEY`, `SBER_MODEL`.
4. Установите `LLM_PROVIDER`.
5. Запустите приложение после настройки БД.

Полная пошаговая инструкция получения ключей, проверки модели через curl, настройки `.env`, ограничений бесплатных тарифов и диагностики ошибок находится в [`docs/llm-providers.md`](docs/llm-providers.md).

