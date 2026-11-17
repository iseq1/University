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

## Этап 12 — основные API эндпоинты и начало метрик

Реализованы следующие возможности:

- `POST /api/v1/generate` — генерация саммари в режимах `baseline` и `full`; `full` использует гибридный Retrieval, затем Validator, Critic и Editor;
- `POST /api/v1/generate/batch` — последовательная пакетная обработка до 20 профилей с отдельным результатом/ошибкой для каждого;
- `POST /api/v1/generate/variants?count=3` — генерация нескольких вариантов и выбор по оценке Critic;
- `POST /api/v1/generate/ensemble` — запуск доступных настроенных провайдеров Atria и ShareLLM и выбор кандидата с наибольшей оценкой Critic;
- `POST /api/v1/evaluate` — расчёт метрик для эталонного и сгенерированного текста;
- `GET /api/v1/evaluate/history` — история оценок;
- `GET /api/v1/requests/{request_id}/reasoning_log` — журнал шагов агентов и трассировка вызовов LLM;
- `/api/v1/admin/knowledge-base` и `/api/v1/admin/glossary` — чтение, создание, изменение и удаление записей с проверкой ролей;
- `POST /api/v1/admin/knowledge-base/import` — импорт JSON-записей;
- `POST /api/v1/admin/knowledge-base/import-csv` — импорт CSV-текста с колонками `source_text,target_text` и необязательной `category`.

Метрики включают Exact Match, BLEU, ROUGE-L, METEOR и chrF. BERTScore доступен по флагу `include_bertscore=true`, но вынесен в необязательную группу зависимостей: `poetry install --with bert-score`. Для него требуется загрузка отдельной модели и дополнительные ресурсы. Метрики лексического совпадения не заменяют экспертную оценку фактической корректности саммари.

### Подготовка базы знаний для режима full

1. Запустите приложение и импортируйте подготовленные данные в SQL-базу:

```bash
poetry run python scripts/import_data.py
```

2. Запустите PostgreSQL и Qdrant через Compose: `docker compose -f "ci-cd files/docker-compose.yml" up -d`. Для локального SQLite PostgreSQL можно не запускать; Qdrant нужен для семантической части Retrieval.
3. Постройте/обновите векторный индекс:

```bash
poetry run python scripts/index_knowledge_base.py
```

4. Запустите API:

```bash
poetry run python run.py
```

После изменений записей базы знаний повторно запускайте индексацию: скрипт пересоздаёт коллекцию Qdrant по актуальному содержимому SQL-базы. Если база знаний или Qdrant не подготовлены, `full` возвращает предупреждение и продолжает генерацию на исходных данных профиля. Это позволяет не подменять отсутствие RAG-контекста выдуманными материалами; для полноценного RAG-сценария индекс должен быть подготовлен заранее.

### Примеры запросов

После регистрации и входа используйте `Authorization: Bearer <access_token>`.

```http
POST /api/v1/generate
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "steam_id": "76561198000000000",
  "profile": {"games": [{"name": "Portal 2", "playtime_hours": 42}]},
  "mode": "full",
  "use_cache": true
}
```

```http
POST /api/v1/evaluate
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "reference": "Игрок предпочитает головоломки и сюжетные игры.",
  "prediction": "Профиль указывает на интерес к сюжетным головоломкам.",
  "model_name": "Atria-Dawn",
  "mode": "full"
}
```

```http
GET /api/v1/requests/<request_id>/reasoning_log
Authorization: Bearer <access_token>
```

### Ограничения этапа 12

- Пакетная обработка выполняется последовательно в HTTP-запросе; Celery/background jobs относятся к следующим этапам.
- Варианты одного провайдера — это несколько независимых генераций, а `/generate/ensemble` сравнивает доступные шлюзы Atria и ShareLLM. Состав кандидатов зависит от настроенных ключей.
- BERTScore выключен по умолчанию; его вычисление может скачать модель для оценки. Это не локальный запуск генеративной LLM.
- При отсутствии/недоступности Qdrant RAG-контекст не подставляется, а в ответ добавляется предупреждение.
- Доступность бесплатного тарифа и API из конкретной сети не гарантируется кодом и зависит от актуальных условий провайдера.


## Steam Web API (этап 12.2)

Для импорта публичного Steam-профиля добавьте `STEAM_API_KEY` в `.env` (получить ключ: https://steamcommunity.com/dev). Авторизация Steam не используется: принимается ссылка на профиль или SteamID64. Подробности, ограничения приватности, TTL и примеры запросов описаны в [`docs/stage-12-api.md`](docs/stage-12-api.md).

## Этап 13 — оценка качества и сравнение моделей

Реализован экспериментальный контур оценки на отдельном тестовом наборе `data/generated/knowledge_base_test.json` (200 синтетических профилей). Скрипт поддерживает выборки 20, 50 и 100 примеров, фиксированный seed и следующие режимы:

- `baseline` — генерация без дополнительного словаря, RAG и мультиагентной доработки;
- `+dict` — генерация с релевантными терминами из глоссария;
- `+rag` — генерация с контекстом гибридного поиска BM25 + Qdrant;
- `+agents` — генерация с последующей обработкой Validator, Critic и Editor через Supervisor;
- `+ensemble` — генерация несколькими настроенными API-провайдерами и выбор кандидата по оценке Critic.

Сравниваются облачные провайдеры `atria` и `sharellm` (если соответствующие ключи настроены). Локальные Ollama/HuggingFace генеративные модели не добавляются: проект сохраняет согласованное API-only решение этапа 11. Для режима `+rag` необходимо предварительно импортировать базу знаний и проиндексировать её в запущенном Qdrant.

Запуск:

```bash
poetry run python scripts/run_eval.py \
  --providers atria,sharellm \
  --modes baseline,+dict,+rag,+agents,+ensemble \
  --sample-sizes 20,50,100
```

Для одного провайдера и более короткого прогона:

```bash
poetry run python scripts/run_eval.py --providers atria --modes baseline,+dict,+rag,+agents --sample-sizes 20
```

Каждый запуск создаёт отдельный каталог `reports/evaluation/<UTC timestamp>/` с JSON по размерам выборок, `results.csv` и `summary.md`. Результаты также сохраняются в таблицах `evaluation_results` и `model_comparisons`. Метрики включают Exact Match, BLEU, ROUGE-L, METEOR и chrF; BERTScore можно включить опцией `--bertscore` (потребуется установка `poetry install --with bert-score`, загрузка модели может занять время).

### API сравнения

- `GET /api/v1/evaluate/compare?models=atria,sharellm&sample_size=20&modes=baseline,%2Bdict,%2Brag,%2Bagents,%2Bensemble` — запускает сравнение и возвращает агрегированные и покомпонентные результаты.
- `POST /api/v1/evaluate/batch` — ставит сравнение в очередь Celery и возвращает `task_id`.
- `GET /api/v1/evaluate/tasks/{task_id}` — возвращает статус и результат фоновой задачи.

Пример тела `POST /api/v1/evaluate/batch`:

```json
{
  "models": ["atria", "sharellm"],
  "modes": ["baseline", "+dict", "+rag", "+agents", "+ensemble"],
  "sample_size": 20,
  "seed": 42
}
```

### Celery

Redis добавлен в `ci-cd files/docker-compose.yml`. Запуск инфраструктуры и worker:

```bash
docker compose -f "ci-cd files/docker-compose.yml" up -d redis postgres qdrant
poetry run celery -A src.worker.celery_app.celery_app worker --loglevel=info
```

Созданы задачи `evaluate_model_task` и `compare_models_task`. Для фонового запуска API должен быть доступен Redis по `REDIS_URL`, а Celery worker должен быть запущен отдельно.

**Ограничения экспериментальных данных:** тестовая выборка состоит из синтетических профилей и синтетических эталонных саммари. Полученные метрики характеризуют сходство генерации с этими эталонами, но сами по себе не доказывают фактическую точность описания реальных Steam-профилей. Статистические тесты и доверительные интервалы из бонусной части ТЗ в этом этапе не реализованы.
