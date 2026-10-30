"""Identidade visual do Segundo Cérebro."""

THEMES = {
    "Dark Profundo": {
        "emoji": "🌌",
        "background": "#0B1020",
        "surface": "#121A2B",
        "surface_alt": "#182338",
        "text": "#F3F6FC",
        "muted": "#A7B2C7",
        "primary": "#6EA8FE",
        "secondary": "#A78BFA",
        "border": "#26344D",
        "success": "#53C7A5",
    },
    "Clean Minimalista": {
        "emoji": "☁️",
        "background": "#F5F7FB",
        "surface": "#FFFFFF",
        "surface_alt": "#EEF2F8",
        "text": "#202B3C",
        "muted": "#68758A",
        "primary": "#477DE8",
        "secondary": "#8B78D6",
        "border": "#E1E7F0",
        "success": "#269B78",
    },
    "High Performance Bege": {
        "emoji": "✨",
        "background": "#F4EFE7",
        "surface": "#FFFCF7",
        "surface_alt": "#EEE5D8",
        "text": "#352D27",
        "muted": "#817365",
        "primary": "#A66B45",
        "secondary": "#8D7965",
        "border": "#E5D9C9",
        "success": "#64836B",
    },
}


def apply_theme(theme_name: str) -> None:
    """Aplica o tema visual escolhido pelo usuário."""
    import streamlit as st

    palette = THEMES.get(theme_name, THEMES["Dark Profundo"])
    css = """
    <style>
      :root {
        --sc-bg: __BG__;
        --sc-surface: __SURFACE__;
        --sc-surface-alt: __ALT__;
        --sc-text: __TEXT__;
        --sc-muted: __MUTED__;
        --sc-primary: __PRIMARY__;
        --sc-secondary: __SECONDARY__;
        --sc-border: __BORDER__;
        --sc-success: __SUCCESS__;
      }
      .stApp { background: var(--sc-bg); color: var(--sc-text); }
      [data-testid="stHeader"] { background: transparent; }
      [data-testid="stSidebar"] { background: var(--sc-surface); border-right: 1px solid var(--sc-border); }
      [data-testid="stSidebar"] * { color: var(--sc-text); }
      .block-container { padding-top: 2.1rem; padding-bottom: 3rem; max-width: 1440px; }
      h1, h2, h3 { color: var(--sc-text); letter-spacing: -0.035em; }
      h1 { font-weight: 750; }
      [data-testid="stCaptionContainer"] p, .stMarkdown small { color: var(--sc-muted); }
      [data-testid="stMetric"] { background: var(--sc-surface); border: 1px solid var(--sc-border); padding: 1rem 1.1rem; border-radius: 16px; }
      [data-testid="stMetricLabel"] { color: var(--sc-muted); }
      [data-testid="stMetricValue"] { color: var(--sc-text); }
      [data-testid="stTabs"] [role="tablist"] { gap: .45rem; border-bottom: 1px solid var(--sc-border); }
      [data-testid="stTabs"] button[role="tab"] { border-radius: 12px 12px 0 0; padding: .7rem 1rem; color: var(--sc-muted); }
      [data-testid="stTabs"] button[aria-selected="true"] { color: var(--sc-primary); border-bottom: 3px solid var(--sc-primary); }
      [data-testid="stForm"], [data-testid="stExpander"] { background: var(--sc-surface); border: 1px solid var(--sc-border); border-radius: 16px; }
      [data-testid="stChatMessage"] { background: var(--sc-surface); border: 1px solid var(--sc-border); border-radius: 16px; padding: .8rem 1rem; margin-bottom: .7rem; }
      .stButton > button, .stFormSubmitButton > button { border-radius: 12px; border: 1px solid var(--sc-primary); background: var(--sc-primary); color: white; font-weight: 650; padding: .55rem 1rem; transition: all .18s ease; }
      .stButton > button:hover, .stFormSubmitButton > button:hover { filter: brightness(1.08); transform: translateY(-1px); }
      [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stNumberInput"] input, [data-testid="stSelectbox"] div[data-baseweb="select"] { border-radius: 11px; }
      [data-testid="stProgressBar"] > div > div { background: var(--sc-primary); }
      hr { border-color: var(--sc-border); }
      .sc-eyebrow { color: var(--sc-primary); font-size: .78rem; font-weight: 750; letter-spacing: .13em; text-transform: uppercase; margin-bottom: .35rem; }
      .sc-hero { background: linear-gradient(120deg, var(--sc-surface), var(--sc-surface-alt)); border: 1px solid var(--sc-border); border-radius: 22px; padding: 1.35rem 1.5rem; margin: .5rem 0 1.4rem 0; }
      .sc-hero-title { color: var(--sc-text); font-size: clamp(1.65rem, 3vw, 2.25rem); font-weight: 780; letter-spacing: -.045em; margin: 0; }
      .sc-hero-subtitle { color: var(--sc-muted); margin: .35rem 0 0 0; font-size: .98rem; }
      @media (max-width: 700px) { .block-container { padding: 1rem .8rem 2rem .8rem; } .sc-hero { padding: 1rem; border-radius: 16px; } }
    </style>
    """
    replacements = {
        "__BG__": palette["background"], "__SURFACE__": palette["surface"],
        "__ALT__": palette["surface_alt"], "__TEXT__": palette["text"],
        "__MUTED__": palette["muted"], "__PRIMARY__": palette["primary"],
        "__SECONDARY__": palette["secondary"], "__BORDER__": palette["border"],
        "__SUCCESS__": palette["success"],
    }
    for key, value in replacements.items():
        css = css.replace(key, value)
    st.markdown(css, unsafe_allow_html=True)
