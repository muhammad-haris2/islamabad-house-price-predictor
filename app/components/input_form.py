"""
input_form.py
=============
Input form component — collects all user inputs and returns them
ONLY when the Predict button is clicked.

Fix: uses explicit keys + session_state so Streamlit does NOT
re-predict on every slider or dropdown change.
"""

import streamlit as st


def render_input_form(info: dict) -> dict | None:
    """
    Renders the property input form.
    Returns input dict ONLY when Predict button is clicked.
    Returns None otherwise.
    """

    locations      = info.get("locations", [])
    property_types = info.get("property_types", [])
    area_min       = float(info.get("area_min_marla", 1.0))
    area_max       = float(info.get("area_max_marla", 100.0))

    st.markdown("### 📝 Property Details")

    # ── Row 1: Property type + Location ──────────────────────
    col1, col2 = st.columns(2)

    with col1:
        property_type = st.selectbox(
            "🏗️ Property Type",
            options=property_types,
            index=property_types.index("House") if "House" in property_types else 0,
            key="input_property_type",
            help="Select the type of property",
        )

    with col2:
        default_loc = "DHA Defence" if "DHA Defence" in locations else (locations[0] if locations else None)
        location = st.selectbox(
            "📍 Location / Area",
            options=locations,
            index=locations.index(default_loc) if default_loc and default_loc in locations else 0,
            key="input_location",
            help="Select the Islamabad area or sector",
        )

    # ── Area slider ───────────────────────────────────────────
    st.markdown("#### 📐 Size")
    area_marla = st.slider(
        "Area (Marla)",
        min_value=area_min,
        max_value=min(area_max, 50.0),
        value=10.0,
        step=0.5,
        key="input_area_marla",
        help="1 Kanal = 20 Marla",
        format="%.1f Marla",
    )

    # ── Bedrooms + Bathrooms ──────────────────────────────────
    st.markdown("#### 🛏️ Rooms")
    col3, col4 = st.columns(2)

    with col3:
        bedrooms = st.selectbox(
            "🛏️ Bedrooms",
            options=list(range(1, 12)),
            index=2,
            key="input_bedrooms",
        )

    with col4:
        bathrooms = st.selectbox(
            "🚿 Bathrooms",
            options=list(range(1, 10)),
            index=1,
            key="input_bathrooms",
        )

    # ── Input Summary (display only — no API call here) ───────
    st.markdown("#### 📊 Input Summary")
    st.markdown(
        f"""
        <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:8px;'>
            <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                        border-radius:10px;padding:10px 14px;'>
                <div style='font-size:11px;color:#aac4d0;text-transform:uppercase;
                            letter-spacing:.5px;margin-bottom:3px;'>Type</div>
                <div style='font-size:15px;font-weight:600;color:#fff;'>{property_type}</div>
            </div>
            <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                        border-radius:10px;padding:10px 14px;'>
                <div style='font-size:11px;color:#aac4d0;text-transform:uppercase;
                            letter-spacing:.5px;margin-bottom:3px;'>Size</div>
                <div style='font-size:15px;font-weight:600;color:#fff;'>{area_marla:.1f} Marla</div>
            </div>
            <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                        border-radius:10px;padding:10px 14px;'>
                <div style='font-size:11px;color:#aac4d0;text-transform:uppercase;
                            letter-spacing:.5px;margin-bottom:3px;'>Rooms</div>
                <div style='font-size:15px;font-weight:600;color:#fff;'>{bedrooms} Bed / {bathrooms} Bath</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Predict button — ONLY this triggers prediction ────────
    if st.button("🔮 Predict Price", use_container_width=True, type="primary"):
        return {
            "property_type": property_type,
            "location":      location,
            "area_marla":    area_marla,
            "bedrooms":      bedrooms,
            "bathrooms":     bathrooms,
        }

    return None