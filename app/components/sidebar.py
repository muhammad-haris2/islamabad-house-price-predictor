"""
sidebar.py
==========
Sidebar component — shows model info and top locations with
average prices fetched from the API /info endpoint.
"""

import streamlit as st
import requests

API_URL = "http://localhost:8000"


def render_sidebar(info: dict):
    with st.sidebar:
        st.markdown("## 🏙️ Islamabad Areas")
        st.caption("All locations available in the model")

        # ── Model stats card ──────────────────────────────────
        st.markdown(
            f"""
            <div style='
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px;
                padding: 12px 16px;
                margin-bottom: 16px;
            '>
                <div style='font-size:11px;color:#aaa;text-transform:uppercase;
                            letter-spacing:.6px;margin-bottom:6px;'>Model Stats</div>
                <div style='font-size:13px;color:#eee;margin-bottom:3px;'>
                    🎯 Accuracy: <b>{info.get("r2_score", 0)*100:.1f}%</b>
                </div>
                <div style='font-size:13px;color:#eee;margin-bottom:3px;'>
                    🏠 Trained on: <b>{info.get("total_rows", 0):,} listings</b>
                </div>
                <div style='font-size:13px;color:#eee;'>
                    📍 Locations: <b>{len(info.get("locations", []))} areas</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Search box ────────────────────────────────────────
        search = st.text_input("🔍 Search area", placeholder="e.g. DHA, Bahria...")

        locations = info.get("locations", [])
        if search:
            locations = [l for l in locations if search.lower() in l.lower()]

        # ── Location list ─────────────────────────────────────
        if locations:
            for loc in locations:
                st.markdown(
                    f"""
                    <div style='
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 6px 10px;
                        margin: 3px 0;
                        border-radius: 8px;
                        background: rgba(255,255,255,0.04);
                        border: 1px solid rgba(255,255,255,0.07);
                        font-size: 12px;
                    '>
                        <span style='color:#ddd;'>📍 {loc}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No areas match your search.")

        st.divider()
        st.caption("🤖 Model: Gradient Boosting Regressor")
        st.caption("📊 Data source: Zameen.com / Graana.com")
        st.caption("🏙️ City: Islamabad, Pakistan")