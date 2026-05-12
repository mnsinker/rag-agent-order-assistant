import streamlit as st

from ui.components.cards import (
    render_problem_card,
    render_usecase_card,
)


def render_problem_types():

    st.markdown("""
    <div class="section-title">
    Best-Fit Problem Types
    </div>

    <div class="section-subtitle">
    This architecture is designed for workflows that require
    multiple data dependencies, business policies,
    decision-making logic, and multi-step orchestration.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_problem_card(
            "Multiple Data Dependencies",
            "Decisions often depend on several systems, user states, runtime context, and upstream data sources.",
            "get_order → get_user → get_credit"
        )

    with col2:
        render_problem_card(
            "Policy Evaluation",
            "Business rules are isolated into reusable policy layers instead of hardcoded workflows.",
            "refund_policy / coupon_policy"
        )

    with col3:
        render_problem_card(
            "Decision-Making",
            "Policies generate structured decisions that drive downstream execution logic.",
            "RefundDecisionDTO / CouponDecisionDTO"
        )

    with col4:
        render_problem_card(
            "Runtime Orchestration",
            "The planner resolves dependencies and orchestrates execution automatically.",
            "planner → tools → execution"
        )


def render_use_cases():

    st.markdown("""
    <div class="section-title">
    Example Use Cases
    </div>

    <div class="section-subtitle">
    The same architecture can support multiple business systems
    by reusing the same planning, policy,
    and orchestration layers.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        render_usecase_card(
            title="Order Assistant",
            desc="""
            AI-powered support workflows for refund checks,
            shipping tracking, coupon evaluation,
            and order-related decisions.
            """,
            runtime_flow=[
                "User Query",
                "→ Planner",
                "→ Tool Execution",
                "→ Policy Evaluation",
                "→ Final Response",
            ]
        )

    with col2:

        render_usecase_card(
            title="AI Marketing System",
            desc="""
            Decision-driven promotion workflows
            for retention, coupon strategy,
            user segmentation, and campaign triggering.
            """,
            runtime_flow=[
                "Detect Churn Risk",
                "→ Analyze User State",
                "→ Evaluate Promotion Policy",
                "→ Trigger Campaign",
            ]
        )

    with col3:

        render_usecase_card(
            title="Approval Workflow System",
            desc="""
            AI-assisted approval workflows
            for refunds, permissions,
            escalations, and operational decisions.
            """,
            runtime_flow=[
                "Analyze Request",
                "→ Evaluate Policy",
                "→ Generate Decision",
                "→ Trigger Approval Flow",
            ]
        )


def render_limitations():

    st.markdown("""
    <div class="section-title">
    Current Limitations
    </div>

    <div class="section-subtitle">
    Current implementation scope and technical constraints.
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown("""
- Single-intent execution only
- No retrieval planning yet
- No long-term memory management
- Mock database instead of production data sources
- No distributed execution runtime
        """)