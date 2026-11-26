"""Трассировки рассуждений и вызовов LLM по идентификатору запроса"""

import streamlit as st
from src.frontend.utils import require_login, call

api = require_login()
st.title("ReasoningLog и LLM-вызовы")
request_id = st.text_input("Request ID", value=st.session_state.get("last_request_id", ""))

if st.button("Загрузить"):

    if not request_id.strip():
        st.warning("Укажите Request ID")

    else:
        result = call(api.get, f"/api/v1/requests/{request_id.strip()}/reasoning_log")

        if result:
            st.subheader("Этапы агентов")
            st.dataframe(result.get("reasoning_log", []), use_container_width=True)
            st.subheader("LLM-вызовы")
            st.dataframe(result.get("llm_calls", []), use_container_width=True)
