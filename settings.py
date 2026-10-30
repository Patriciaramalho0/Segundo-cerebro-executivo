import os

def get_setting(name, default=None):
    """Lê primeiro variável de ambiente e depois Streamlit Secrets."""
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return default
