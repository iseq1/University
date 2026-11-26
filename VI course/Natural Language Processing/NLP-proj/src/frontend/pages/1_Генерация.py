"""Создание геймерского паспорта"""

import json
import streamlit as st
from src.frontend.utils import require_login, call

api = require_login()
st.title("Генерация геймерского паспорта на основе Steam")
single, batch = st.tabs(["Один профиль", "Пакетная генерация"])

with single:

    with st.form("generate"):
        identifier = st.text_input("SteamID64 или ссылка на профиль")
        source = st.text_area("Дополнительные сведения (необязательно)")
        mode = st.selectbox("Режим", ["full", "baseline"])
        use_cache = st.checkbox("Использовать кэш", value=True)
        submit = st.form_submit_button("Получить паспорт")

    if submit:
        identifier = identifier.strip()

        if not identifier:
            st.error("Укажите SteamID64 или ссылку на профиль!")

        else:
            payload = {
                "mode": mode,
                "input_text": source or None,
                "use_cache": use_cache,
                "profile_url" if "/" in identifier else "steam_id": identifier
            }

            with st.spinner("Подписываем бумаги для выдачи паспорта..."):
                result = call(
                    api.post,
                    "/api/v1/generate",
                    json=payload
                )

            if result:
                st.session_state["last_request_id"] = result.get("request_id")
                st.subheader("Ваш геймерский паспорт")
                st.write(result.get("summary", ""))
                st.caption(f"Request ID: {result.get('request_id')} · кэш: {result.get('cached')}")
                st.json({k: v for k, v in result.items() if k != "summary"})

with batch:
    ids = st.text_area("SteamID64 (по одному на строку, максимум 20)")
    batch_mode = st.selectbox("Режим пакета", ["baseline", "full"])
    uploaded = st.file_uploader("Или загрузите TXT с одним SteamID64 на строку", type=["txt"])

    if st.button("Запустить пакет генерации"):
        source_lines = uploaded.getvalue().decode("utf-8-sig") if uploaded else ids
        values = [x.strip() for x in source_lines.splitlines() if x.strip()]

        if not 1 <= len(values) <= 20:
            st.error("Укажите от 1 до 20 SteamID")

        else:
            result = call(
                api.post,
                "/api/v1/generate/batch",
                json={
                    "items": [
                        {
                            "steam_id": v,
                            "mode": batch_mode
                        } for v in values
                    ]
                }
            )

            if result:
                st.json(result)
                st.download_button(
                    "Сохранить JSON",
                    json.dumps(result, ensure_ascii=False, indent=2),
                    "batch.json",
                    "application/json"
                )
