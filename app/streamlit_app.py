"""
streamlit_app.py
================
Main Streamlit application entry point.

Run with:
    streamlit run app/streamlit_app.py

Make sure the FastAPI server is running first:
    python -m api.main
"""

import sys

# ── Allow imports from project root ──────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import requests
import streamlit as st
from app.components.sidebar         import render_sidebar
from app.components.input_form      import render_input_form
from app.components.prediction_card import render_prediction_card

# ── Config ────────────────────────────────────────────────────────────────────

API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:8000"))
st.set_page_config(
    page_title = "Islamabad House Price Predictor",
    page_icon  = "🏠",
    layout     = "wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a1628 0%, #0d1f3c 50%, #0a1628 100%);
        color: #e8f4f8;
    }

    [data-testid="stHeader"] { background: transparent; }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1f3c 0%, #0a1628 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Inputs */
    div[data-baseweb="select"] > div,
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: #e8f4f8 !important;
    }

    /* Slider */
    .stSlider > div > div > div {
        background: rgba(255,255,255,0.07);
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1a472a, #40916c) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 0.6rem 1rem !important;
        min-height: 3rem !important;
        box-shadow: 0 4px 15px rgba(64,145,108,0.4) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(64,145,108,0.5) !important;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 12px;
    }

    [data-testid="stMetricLabel"]  { color: #aac4d0 !important; }
    [data-testid="stMetricValue"]  { color: #e8f4f8 !important; }

    /* Tables */
    .stMarkdown table {
        width: 100%;
        border-collapse: collapse;
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stMarkdown table th {
        background: rgba(255,255,255,0.08);
        color: #aac4d0 !important;
        padding: 10px 14px;
        font-size: 13px;
    }
    .stMarkdown table td {
        color: #e8f4f8 !important;
        padding: 9px 14px;
        border-top: 1px solid rgba(255,255,255,0.06);
        font-size: 13px;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.1) !important; }

    /* Labels */
    .stSelectbox label,
    .stSlider label,
    .stTextInput label { color: #aac4d0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Fetch model info from API ─────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_info() -> dict:
    try:
        r = requests.get(f"{API_URL}/info", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


# ── Header ────────────────────────────────────────────────────────────────────
def render_header():
    st.markdown(
        """
        <div style='
            text-align: center;
            padding: 28px 20px 20px;
            margin-bottom: 8px;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(26,71,42,0.6), rgba(64,145,108,0.4));
            border: 1px solid rgba(144,238,144,0.2);
        '>
            <h1 style='color:#fff;font-size:2.2rem;margin:0 0 6px;'>
                🏠 Islamabad House Price Predictor
            </h1>
            <p style='color:rgba(255,255,255,0.75);font-size:15px;margin:0;'>
                🇵🇰 ML-powered property valuation for Islamabad &nbsp;|&nbsp;
                Powered by Gradient Boosting &nbsp;|&nbsp; Prices in PKR
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── API health check ──────────────────────────────────────────────────────────
def check_api() -> bool:
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.status_code == 200 and r.json().get("model_loaded", False)
    except Exception:
        return False


# ── Main app ──────────────────────────────────────────────────────────────────
def main():
    # Header
    render_header()

    # API health check
    api_ok = check_api()
    if not api_ok:
        st.error(
            "⚠️ Cannot connect to the FastAPI backend. "
            "Please make sure it is running:\n\n"
            "```bash\npython -m api.main\n```"
        )
        st.stop()

    # Fetch model info
    info = fetch_info()
    if not info:
        st.error("⚠️ Could not load model info from API. Check if the API is running.")
        st.stop()

    # Sidebar
    render_sidebar(info)

    # ── Two column layout: form (left) | result (right) ──────
    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        inputs = render_input_form(info)

    with right_col:
        st.markdown("### 💰 Prediction Result")

        # Initialise session state
        if "last_result" not in st.session_state:
            st.session_state.last_result = None

        # Only call API when button was just clicked (inputs is not None)
        if inputs is not None:
            with st.spinner("Calculating price..."):
                try:
                    response = requests.post(
                        f"{API_URL}/predict",
                        json=inputs,
                        timeout=10,
                    )
                    if response.status_code == 200:
                        # Store result — survives reruns caused by other widgets
                        st.session_state.last_result = response.json()
                    else:
                        st.error(f"API Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Could not reach API: {e}")

        # Always show last result if it exists (even after widget interactions)
        if st.session_state.last_result:
            render_prediction_card(st.session_state.last_result)
        else:
            st.markdown(
                """
                <div style='
                    border: 2px dashed rgba(255,255,255,0.15);
                    border-radius: 16px;
                    padding: 60px 20px;
                    text-align: center;
                    color: rgba(255,255,255,0.35);
                    margin-top: 16px;
                '>
                    <div style='font-size:48px;margin-bottom:12px;'>🏠</div>
                    <div style='font-size:16px;'>
                        Fill in the property details on the left<br>
                        and click <b>Predict Price</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Footer ────────────────────────────────────────────────
    st.divider()
    st.markdown(
        """
        <div style='text-align:center;color:rgba(255,255,255,0.4);font-size:12px;padding:8px;'>
            🏠 Islamabad House Price Predictor &nbsp;|&nbsp;
            Built with FastAPI + Streamlit + scikit-learn &nbsp;|&nbsp;
            🇵🇰 Data: Zameen.com / Graana.com
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()