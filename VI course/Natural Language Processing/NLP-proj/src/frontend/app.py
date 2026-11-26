"""Точка входа Streamlit для Gamer Passport 2.0."""

import streamlit as st
from src.frontend.utils import APIError, client

st.set_page_config(page_title="Геймерский паспорт 2.0", page_icon="🎮", layout="wide")
st.title("Геймерский паспорт 2.0")
st.caption("Генерация профилей Steam через защищённый FastAPI и внешний LLM-API")

if st.session_state.get("token"):

    try:
        user = client().get("/auth/me")
        st.success(f"Вы вошли как {user.get('username', user.get('email', 'пользователь'))} · роль: {user.get('role', 'user')}")

    except APIError as exc:
        st.error(str(exc))

    if st.button("Выйти"):
        st.session_state.pop("token", None)
        st.rerun()

    st.info("Выберите страницу в боковом меню: генерация, база знаний, HITL, оценка или логи.")

else:
    login_tab, register_tab = st.tabs(["Войти", "Регистрация"])

    with login_tab:

        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Пароль", type="password")
            submitted = st.form_submit_button("Войти")

        if submitted:
            try:
                result = client().post("/auth/login", json={"email": email, "password": password})
                st.session_state["token"] = result["access_token"]
                st.rerun()
            except (APIError, KeyError) as exc:
                st.error(str(exc))

    with register_tab:

        with st.form("register"):
            username = st.text_input("Имя пользователя")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Пароль", type="password", key="reg_password")
            register = st.form_submit_button("Создать аккаунт")

        if register:
            try:
                client().post("/auth/register", json={"username": username, "email": reg_email, "password": reg_password})
                st.success("Аккаунт создан. Войдите через вкладку «Войти».")
            except APIError as exc:
                st.error(str(exc))
