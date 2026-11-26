"""Управление базой знаний и глоссарием (CRUD) для редакторов/администраторов, включая импорт из CSV."""

import streamlit as st
from src.frontend.utils import require_login, call

api = require_login()
st.title("База знаний и глоссарий")
kind = st.radio("Раздел", ["knowledge-base", "glossary"], format_func=lambda x: "База знаний" if x == "knowledge-base" else "Глоссарий", horizontal=True)
root = f"/api/v1/admin/{kind}"
items = call(api.get, root)

if items is not None:
    st.dataframe(items, use_container_width=True)
    st.caption("Чтение доступно editor/admin, изменение — admin.")

with st.expander("Создать или обновить запись"):
    item_id = st.number_input("ID для обновления (0 — новая запись)", min_value=0, step=1)
    a = st.text_area("Исходный текст" if kind == "knowledge-base" else "Термин")
    b = st.text_area("Целевой текст" if kind == "knowledge-base" else "Определение")
    category = st.text_input("Категория")
    if st.button("Сохранить запись"):
        payload = ({"source_text": a, "target_text": b, "category": category or None}
                   if kind == "knowledge-base" else {"term": a, "definition": b, "category": category or None})
        result = call(api.put if item_id else api.post, f"{root}/{item_id}" if item_id else root, json=payload)
        if result is not None:
            st.success("Сохранено. Обновите страницу для просмотра.")

with st.expander("Удалить запись"):
    delete_id = st.number_input("ID для удаления", min_value=1, step=1)
    confirm = st.checkbox("Подтверждаю удаление")
    if st.button("Удалить", disabled=not confirm):
        call(api.delete, f"{root}/{delete_id}")
        st.success("Запрос удаления отправлен")

if kind == "knowledge-base":
    with st.expander("Импорт CSV"):
        st.caption("Колонки: source_text,target_text,category (последняя необязательна); до 1000 строк")
        uploaded = st.file_uploader("CSV UTF-8", type="csv")
        if uploaded and st.button("Импортировать"):
            try:
                csv_text = uploaded.getvalue().decode("utf-8-sig")
            except UnicodeDecodeError:
                st.error("Файл должен быть в UTF-8")
            else:
                result = call(api.post, "/api/v1/admin/knowledge-base/import-csv", json={"csv_text": csv_text})
                if result:
                    st.json(result)
