import streamlit as st

from ui.components.styles import inject_css
from ui.components.hero import render_hero

from ui.components.sections import (render_problem_types,render_use_cases)
from ui.components.how_it_works import (render_how_it_works)
st.set_page_config(
    page_title="Overview",
    layout="wide"
)

inject_css()

render_hero()

render_problem_types()

render_how_it_works()

render_use_cases()

