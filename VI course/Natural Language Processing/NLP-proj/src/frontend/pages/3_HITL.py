"""Очередь модерации с участием человека"""

import streamlit as st
from src.frontend.utils import require_login, call

api = require_login()
st.title("HITL — ручная проверка")
status = st.selectbox("Статус", ["pending", "approved", "rejected"])
result = call(api.get, "/api/v1/hitl/queue", params={"status": status, "limit": 100})

if result:
    st.caption(f"Найдено: {result.get('count', 0)}")

    for item in result.get("items", []):
        with st.expander(f"#{item['id']} · score={item.get('critic_score')}"):
            st.write("**Вход:**", item.get("input_text"))
            st.write("**Результат модели:**", item.get("model_output"))

            if status == "pending":
                corrected = st.text_area("Исправленный текст (необязательно)", key=f"corrected-{item['id']}")
                a, b = st.columns(2)

                if a.button("Подтвердить", key=f"approve-{item['id']}"):
                    response = call(api.post, f"/api/v1/hitl/{item['id']}/approve", json={"corrected_text": corrected or None})

                    if response is not None:
                        st.success("Подтверждено")

                if b.button("Отклонить", key=f"reject-{item['id']}"):
                    response = call(api.post, f"/api/v1/hitl/{item['id']}/reject")

                    if response is not None:
                        st.success("Отклонено")

if st.button("Переиндексировать базу знаний"):
    response = call(api.post, "/api/v1/hitl/reindex")

    if response:
        st.json(response)
