# Этап 12. API и метрики

## Архитектура запроса генерации

`POST /api/v1/generate` принимает Steam ID и профиль. В режиме `baseline` профиль передаётся в LLM API напрямую. В режиме `full` дополнительно выполняется гибридный поиск по базе знаний (BM25 + векторный поиск Qdrant + RRF), найденные материалы добавляются в prompt, после генерации Supervisor запускает Validator, Critic и Editor. Все вызовы генеративной модели идут через единый `LLMManager` этапа 11 (Atria/ShareLLM).

## Режимы

- `baseline`: одна генерация без Retrieval и цикла агентов.
- `full`: Retrieval, генерация, Validator, Critic, Editor и сохранение reasoning log.

Если Retrieval не может получить контекст, API добавляет предупреждение и продолжает с исходными данными профиля. Для демонстрации RAG необходимо предварительно импортировать данные и построить Qdrant индекс.

## Эндпоинты

| Метод | Путь | Назначение |
|---|---|---|
| POST | `/api/v1/generate` | Генерация baseline/full |
| POST | `/api/v1/generate/batch` | Пакетная генерация |
| POST | `/api/v1/generate/variants` | Несколько вариантов одной конфигурацией |
| POST | `/api/v1/generate/ensemble` | Сравнение настроенных Atria/ShareLLM |
| POST | `/api/v1/evaluate` | Метрики одного эталонного/сгенерированного текста |
| GET | `/api/v1/evaluate/history` | История оценок |
| GET | `/api/v1/requests/{request_id}/reasoning_log` | Логи агентов и LLM-вызовов |
| GET/POST/PUT/DELETE | `/api/v1/admin/knowledge-base` | CRUD базы знаний |
| GET/POST/PUT/DELETE | `/api/v1/admin/glossary` | CRUD глоссария |
| POST | `/api/v1/admin/knowledge-base/import` | Импорт JSON |
| POST | `/api/v1/admin/knowledge-base/import-csv` | Импорт CSV в теле JSON |

Все API-маршруты, кроме healthcheck и auth endpoints, требуют JWT. Чтение справочников доступно editor/admin, изменение — admin.

## Метрики

- Exact Match — совпадение строк без учёта регистра.
- BLEU — n-граммная точность с учетом штрафа за длину.
- ROUGE-L — F1 на основе наибольшей общей подпоследовательности.
- METEOR — сопоставление токенов; если ресурс WordNet NLTK отсутствует, метрика возвращается как `null` с пояснением.
- chrF — символьная n-граммная метрика.
- BERTScore F1 — дополнительная семантическая метрика, включается отдельно, требует установки `poetry install --with bert-score` и локальной загрузки модели оценивания.

Метрики сравнивают текст с эталоном и не являются самостоятельным доказательством фактической достоверности утверждений о Steam-профиле.

## Этап 12.2 — интеграция со Steam Web API

Добавлен импорт публичных данных Steam без авторизации через Steam: пользователь передаёт ссылку `https://steamcommunity.com/id/<vanity>` / `https://steamcommunity.com/profiles/<SteamID64>` либо сам SteamID64. Логин и пароль Steam не запрашиваются. Для разрешения vanity URL и получения данных нужен личный Steam Web API Key в `STEAM_API_KEY`.

### Конфигурация

```env
STEAM_API_KEY=your_steam_web_api_key
STEAM_API_BASE_URL=https://api.steampowered.com
STEAM_API_TIMEOUT=15
STEAM_CACHE_TTL_HOURS=12
```

### API

- `POST /api/v1/steam/profile` — импортирует или возвращает закэшированный профиль. Тело: `{"profile_url":"https://steamcommunity.com/id/username","refresh":false}`. В поле `profile_url` также можно передать SteamID64. Для принудительного обновления установите `refresh=true`.
- `POST /api/v1/generate` — теперь можно передать `profile_url` вместо `steam_id` и `profile`; профиль будет получен из Steam и передан в существующий конвейер генерации. Пример: `{"profile_url":"https://steamcommunity.com/id/username","mode":"full"}`.

### Получаемые данные

Публичная сводка профиля, аватар, статус, URL, список принадлежащих игр и недавно запущенные игры (если они доступны через настройки приватности профиля). Для игр сохраняются AppID, название и время в игре. Отсутствие `games` в ответе Steam фиксируется флагом `games_available=false`, а не трактуется как достоверно пустая библиотека.

### Кэш и ограничения

Данные сохраняются в таблице `steam_profiles` в JSON-поле `profile_data`. По умолчанию TTL составляет 12 часов; повторный запрос в пределах TTL не обращается к Steam. `refresh=true` обходит кэш. Если список игр закрыт настройками приватности, Steam может не вернуть его. Сервис не обходит приватность и не получает закрытые данные. Steam API key хранится только на backend в `.env` и не должен попадать во frontend или репозиторий.

При запуске приложения `Base.metadata.create_all` создаёт новую таблицу `steam_profiles` в существующей БД. Для уже работающего экземпляра достаточно перезапустить приложение после обновления кода.
