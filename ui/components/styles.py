import streamlit as st


def inject_css():

    css = """
    <style>

    .stApp {
        background-color: #050816;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 4rem;
        padding-right: 4rem;
        max-width: 1600px;
    }

    .hero-title {
        font-size: 84px;
        line-height: 1.02;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 28px;
        white-space: nowrap;
    }

    .hero-subtitle {
        font-size: 22px;
        line-height: 1.8;
        color: #9CA3AF;
        max-width: 1100px;
    }

    .section-title {
        font-size: 44px;
        font-weight: 700;
        margin-bottom: 14px;
        margin-top: 120px;
    }

    .section-subtitle {
        font-size: 20px;
        color: #9CA3AF;
        line-height: 1.7;
        max-width: 1100px;
        margin-bottom: 40px;
    }

    .card {
        background: linear-gradient(
            180deg,
            rgba(22,27,45,1) 0%,
            rgba(11,14,24,1) 100%
        );

        border: 1px solid #262B3D;
        border-radius: 28px;

        padding: 34px;

        transition: all 0.25s ease;

        min-height: 280px;
    }

    .card:hover {
        transform: translateY(-6px);
        border-color: #6366F1;
        box-shadow: 0 20px 50px rgba(99,102,241,0.15);
    }

    .card-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 18px;
    }

    .card-desc {
        color: #A1A1AA;
        line-height: 1.8;
        font-size: 17px;
    }

    .card-highlight {
        margin-top: 24px;
        color: #818CF8;
        font-family: monospace;
        font-size: 15px;
    }

    .usecase-card {
        background: linear-gradient(
            180deg,
            rgba(22,27,45,1) 0%,
            rgba(11,14,24,1) 100%
        );

        border: 1px solid #262B3D;
        border-radius: 30px;

        padding: 38px;

        transition: all 0.25s ease;

        min-height: 650px;
    }

    .usecase-card:hover {
        transform: translateY(-8px);
        border-color: #6366F1;
        box-shadow: 0 25px 60px rgba(99,102,241,0.18);
    }

    .usecase-title {
        font-size: 38px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 24px;
    }

    .usecase-desc {
        color: #B0B3C1;
        font-size: 18px;
        line-height: 1.8;
        min-height: 150px;
    }

    .usecase-divider {
        height: 1px;
        background: #262B3D;
        margin-top: 30px;
        margin-bottom: 30px;
    }

    .usecase-fit-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 20px;
    }

    .usecase-list {
        color: #A1A1AA;
        line-height: 2;
        font-size: 17px;
    }

    .runtime-box {
        margin-top: 28px;

        background: #070B18;

        border: 1px solid #2B3147;

        border-radius: 20px;

        padding: 24px;

        color: #D6DBFF;

        font-family: monospace;

        font-size: 17px;

        line-height: 1.8;
    }

    .limit-box {
        background: linear-gradient(
            180deg,
            rgba(22,27,45,1) 0%,
            rgba(11,14,24,1) 100%
        );

        border: 1px solid #262B3D;

        border-radius: 30px;

        padding: 50px;

        margin-top: 60px;
    }

    .limit-title {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 28px;
    }

    .limit-list {
        color: #B0B3C1;
        line-height: 2.2;
        font-size: 18px;
    }
    
    /* ======================================================
HOW IT WORKS
====================================================== */

.flow-card {

    background:
        linear-gradient(
            180deg,
            rgba(20,26,48,1) 0%,
            rgba(8,12,24,1) 100%
        );

    border: 1px solid #23283B;

    border-radius: 30px;

    padding: 36px;

    min-height: 320px;

    transition: all 0.25s ease;
}

.flow-card:hover {

    transform: translateY(-8px);

    border-color: #4ADE80;

    box-shadow:
        0 25px 60px rgba(74,222,128,0.12);
}

.flow-icon {

    width: 72px;
    height: 72px;

    border-radius: 20px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(74,222,128,0.12);

    color: #4ADE80;

    font-size: 34px;
    font-weight: 700;

    margin-bottom: 28px;
}

.flow-card-title {

    font-size: 34px;

    font-weight: 700;

    line-height: 1.2;

    margin-bottom: 22px;
}

.flow-card-desc {

    color: #A1A1AA;

    font-size: 19px;

    line-height: 1.9;
}

.flow-arrow {

    font-size: 64px;

    color: #4ADE80;

    text-align: center;

    margin-top: 120px;

    opacity: 0.7;
}

    </style>
    """
    st.html(css)