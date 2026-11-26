"""Рабочее состояние без раскрытия учетных данных или внутренних аспектов базы данных"""

import streamlit as st
from src.frontend.utils import require_login, call

api = require_login()
st.title("Мониторинг")
st.caption("Доступность API и состояние задач Celery. Детальные метрики инфраструктуры требуют отдельного мониторинга.")

if st.button("Проверить API"):
    result = call(api.get, "/healthz")

    if result:
        st.success("API доступен")
        st.json(result)

task_id = st.text_input("Celery task ID", value=st.session_state.get("eval_task_id", ""))

if st.button("Проверить задачу") and task_id:
    result = call(api.get, f"/api/v1/evaluate/tasks/{task_id}")

    if result:
        st.json(result)

# st.info("Статистика попаданий в кэш пока не предоставляется отдельным API endpoint. Нельзя достоверно отображать её без backend-маршрута.")
