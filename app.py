from __future__ import annotations

import streamlit as st

from src.data import build_general_view_model, load_dataframe
from src.render import inject_global_styles, render_general_page, render_participant_shell

st.set_page_config(
    page_title="Peñita FIFA World Cup 2026",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

df = load_dataframe()
page = st.sidebar.radio(
    label="",
    options=["General", "Participante"],
    label_visibility="collapsed",
)

if page == "General":
    model = build_general_view_model(df)
    render_general_page(model)
else:
    render_participant_shell()
