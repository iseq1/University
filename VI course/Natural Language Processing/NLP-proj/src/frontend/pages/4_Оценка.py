"""История оценок, сравнение и статус асинхронных задач"""

import streamlit as st
from src.frontend.utils import require_login, call

api = require_login()
st.title("Оценка качества")
with st.expander("Оценить один текст"):

    with st.form("evaluate"):
        reference = st.text_area("Эталон")
        prediction = st.text_area("Предсказание")
        evaluate = st.form_submit_button("Рассчитать метрики")

    if evaluate:
        result = call(api.post, "/api/v1/evaluate", json={"reference": reference, "prediction": prediction})

        if result:
            st.json(result)

st.subheader("История")
history = call(api.get, "/api/v1/evaluate/history", params={"limit": 100})

if history:
    import pandas as pd
    rows = []

    for entry in history:
        row = {k: entry.get(k) for k in ("id", "model_name", "mode", "sample_size", "created_at")}
        row.update({k: v for k, v in (entry.get("metrics") or {}).items() if isinstance(v, (int, float))})
        rows.append(row)

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    numeric = [k for k in df.select_dtypes(include="number").columns if k not in ("id", "sample_size")]

    if numeric:
        metric = st.selectbox("Метрика для графика", numeric)
        import plotly.express as px
        fig = px.bar(df, x="id", y=metric, color="mode", hover_data=["model_name"])
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("Сохранить интерактивный график HTML", fig.to_html(include_plotlyjs="cdn"), "evaluation_chart.html", "text/html")

st.subheader("Фоновое сравнение")

with st.form("batch_eval"):
    providers = st.multiselect("Провайдеры", ["atria", "sharellm", "sber"], default=["sber"])
    modes = st.multiselect("Режимы", ["baseline", "+dict", "+rag", "+agents", "+ensemble"], default=["baseline"])
    sample_size = st.selectbox("Количество примеров", [20, 50, 100])
    seed = st.number_input("Seed", value=42, step=1)
    submit = st.form_submit_button("Запустить в Celery")

if submit:
    result = call(api.post, "/api/v1/evaluate/batch", json={"models": providers, "modes": modes, "sample_size": sample_size, "seed": int(seed)})

    if result:
        st.session_state["eval_task_id"] = result["task_id"]
        st.json(result)

task_id = st.text_input("ID задачи", value=st.session_state.get("eval_task_id", ""))

if st.button("Проверить статус") and task_id:
    result = call(api.get, f"/api/v1/evaluate/tasks/{task_id}")

    if result:
        st.json(result)
