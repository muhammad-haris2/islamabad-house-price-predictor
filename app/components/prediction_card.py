"""
prediction_card.py
==================
Displays the prediction result in a styled card with
price breakdown and comparable metrics.
"""

import streamlit as st


def render_prediction_card(result: dict):
    """Renders the prediction result card."""

    price_label       = result.get("predicted_price_label", "N/A")
    per_marla_label   = result.get("price_per_marla_label", "N/A")
    price_pkr         = result.get("predicted_price_pkr", 0)
    model_r2          = result.get("model_r2", 0)
    summary           = result.get("input_summary", {})

    # ── Main price card ───────────────────────────────────────
    st.markdown(
        f"""
        <div style='
            background: linear-gradient(135deg, #1a472a 0%, #2d6a4f 50%, #40916c 100%);
            border: 1px solid rgba(144, 238, 144, 0.3);
            border-radius: 20px;
            padding: 32px 24px;
            text-align: center;
            margin: 16px 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        '>
            <p style='color:rgba(255,255,255,0.8);font-size:15px;margin:0 0 8px;'>
                🏠 Estimated Property Price
            </p>
            <h1 style='
                color: #ffffff;
                font-size: 3rem;
                margin: 0 0 8px;
                letter-spacing: 0.5px;
            '>{price_label}</h1>
            <p style='color:rgba(255,255,255,0.75);font-size:14px;margin:0;'>
                📍 {summary.get("location", "")} &nbsp;|&nbsp;
                {summary.get("area_marla", "")} Marla &nbsp;|&nbsp;
                {summary.get("bedrooms", "")} Bed &nbsp;|&nbsp;
                {summary.get("bathrooms", "")} Bath
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Metrics row ───────────────────────────────────────────
    st.markdown(
        f"""
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0;'>
            <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                        border-radius:12px;padding:14px 16px;'>
                <div style='font-size:11px;color:#aac4d0;text-transform:uppercase;
                            letter-spacing:.5px;margin-bottom:4px;'>Total Price</div>
                <div style='font-size:18px;font-weight:600;color:#fff;'>{price_label}</div>
            </div>
            <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                        border-radius:12px;padding:14px 16px;'>
                <div style='font-size:11px;color:#aac4d0;text-transform:uppercase;
                            letter-spacing:.5px;margin-bottom:4px;'>Per Marla</div>
                <div style='font-size:18px;font-weight:600;color:#fff;'>{per_marla_label}</div>
            </div>
            <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                        border-radius:12px;padding:14px 16px;'>
                <div style='font-size:11px;color:#aac4d0;text-transform:uppercase;
                            letter-spacing:.5px;margin-bottom:4px;'>Model Accuracy</div>
                <div style='font-size:18px;font-weight:600;color:#fff;'>{model_r2*100:.1f}%</div>
            </div>
            <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                        border-radius:12px;padding:14px 16px;'>
                <div style='font-size:11px;color:#aac4d0;text-transform:uppercase;
                            letter-spacing:.5px;margin-bottom:4px;'>Property Type</div>
                <div style='font-size:18px;font-weight:600;color:#fff;'>{summary.get("property_type","N/A")}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Price breakdown table ─────────────────────────────────
    st.markdown("#### 📋 Full Breakdown")

    area    = summary.get("area_marla", 1)
    per_m   = result.get("price_per_marla_pkr", 0)

    st.markdown(
        f"""
        | Detail | Value |
        |--------|-------|
        | **Location** | {summary.get("location", "N/A")} |
        | **Property Type** | {summary.get("property_type", "N/A")} |
        | **Area** | {area} Marla |
        | **Bedrooms** | {summary.get("bedrooms", "N/A")} |
        | **Bathrooms** | {summary.get("bathrooms", "N/A")} |
        | **Predicted Price** | {price_label} |
        | **Price per Marla** | {per_marla_label} |
        | **Price (PKR)** | PKR {price_pkr:,.0f} |
        """
    )

    # ── Disclaimer ────────────────────────────────────────────
    st.caption(
        "⚠️ This is an ML-based estimate. Actual prices may vary based on "
        "exact plot location, road access, construction quality, and current market conditions."
    )