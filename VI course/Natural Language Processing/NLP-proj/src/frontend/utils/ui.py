"""Вспомогательные средства для аутентификации и API в Streamlit"""

import streamlit as st
from src.frontend.utils import APIClient, APIError


def client() -> APIClient:
    """Получение API-клиента"""
    return APIClient(
        token=st.session_state.get("token")
    )


def require_login() -> APIClient:
    """Потребность ре-логина"""

    if not st.session_state.get("token"):
        st.warning("Авторизуйтесь на главной странице.")
        st.stop()

    return client()


def call(action, *args, **kwargs):
    """Вызов метода"""

    try:
        return action(*args, **kwargs)

    except APIError as exc:
        st.error(str(exc))
        return None
