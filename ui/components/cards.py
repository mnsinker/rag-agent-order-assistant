import streamlit as st


def render_problem_card(
        title,
        desc,
        highlight
):

    with st.container(border=True):

        st.markdown(f"""
### {title}

{desc}

`{highlight}`
""")

        st.markdown("<br>", unsafe_allow_html=True)


def render_usecase_card(
        title,
        desc,
        runtime_flow
):

    with st.container(border=True):

        st.markdown(f"## {title}")
        st.markdown(desc)
        st.divider()
        st.markdown("<br>", unsafe_allow_html=True)

        runtime_text = "\n".join(runtime_flow)
        st.code(runtime_text)