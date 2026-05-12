import streamlit as st


def render_flow_card(number, title, desc):

    html = f"""
    <div class="flow-card">

        <div class="flow-icon">
            {number}
        </div>

        <div class="flow-card-title">
            {title}
        </div>

        <div class="flow-card-desc">
            {desc}
        </div>

    </div>
    """

    st.html(html)


def render_arrow():

    st.html("""
    <div class="flow-arrow">
        →
    </div>
    """)


def render_how_it_works():

    # =====================================================
    # HEADER
    # =====================================================

    st.html("""
    <div class="section-title">
        How The Runtime Works
    </div>

    <div class="section-subtitle">
        The same runtime architecture can support different business systems
        through reusable planning, decision logic,
        and execution layers.
    </div>
    """)

    # =====================================================
    # ROW 1
    # =====================================================

    row1_col1, row1_arrow, row1_col2 = st.columns([4, 1, 4])

    with row1_col1:

        render_flow_card(
            1,
            "User Query",
            """
            LLMs translate natural language requests
            into structured execution goals.
            """
        )

    with row1_arrow:

        render_arrow()

    with row1_col2:

        render_flow_card(
            2,
            "Planning",
            """
            The planner builds execution flow
            by resolving dependencies
            and selecting tools dynamically.
            """
        )

    # =====================================================
    # SPACING
    # =====================================================

    st.html("<div style='height:32px'></div>")

    # =====================================================
    # ROW 2
    # =====================================================

    row2_col1, row2_arrow, row2_col2 = st.columns([4, 1, 4])

    with row2_col1:

        render_flow_card(
            3,
            "Decision Logic",
            """
            Business policies generate
            structured decisions
            instead of raw text outputs.
            """
        )

    with row2_arrow:

        render_arrow()

    with row2_col2:

        render_flow_card(
            4,
            "Execution",
            """
            Tools execute actions,
            update runtime state,
            and generate final responses.
            """
        )