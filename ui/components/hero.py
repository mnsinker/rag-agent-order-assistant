import streamlit as st


def render_hero():

    col1, col2 = st.columns([1.2, 12])

    with col1:
        st.image("ui/assets/logo.svg", width=72)

    with col2:
        st.markdown("""
        <div class="hero-title">
            AI-Powered<br>
            Decision System
        </div>

        <div class="hero-subtitle">
            From refund evaluation to marketing campaigns,
            powered by reusable planning and policy layers.
        </div>
        """, unsafe_allow_html=True)