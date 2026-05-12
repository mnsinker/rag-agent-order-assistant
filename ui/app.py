import streamlit as st

demo_page = st.Page(
    "demo.py",
    title="Demo",
    icon="💬",
)

overview_page = st.Page(
    "pages/1_Overview.py",
    title="Overview",
    icon="💡",
)

archi_page = st.Page(
    "pages/2_Architecture.py",
    title="Architecture",
    icon="🏗️",
)

evolution_page = st.Page(
    "pages/3_Evolution.py",
    title="Evolution",
    icon="🗺️",
)

pg = st.navigation(
    [demo_page, overview_page, archi_page, evolution_page],
)

pg.run()