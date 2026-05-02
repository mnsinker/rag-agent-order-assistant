import os
from dotenv import load_dotenv
load_dotenv()

def get_secret(name: str, default: str | None = None) -> str | None:
    """
    读取顺序:
    1. streamlit secrets 适合:    streamlit 本地/线上
    2. .env 适合:                 pycharm / terminal / pytest
    """
    try:
        import streamlit as st
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name, default)

