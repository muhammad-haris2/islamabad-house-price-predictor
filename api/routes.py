"""
routes.py
=========
API route definitions.

Endpoints:
    GET  /health   - health check
    GET  /info     - model metadata and valid input options
    POST /predict  - predict house price
"""

import json
import joblib
import numpy as np
from fastapi import APIRouter, HTTPException

from api.schemas import PredictionRequest, PredictionResponse, HealthResponse, InfoResponse
from api.config  import MODEL_PATH, ENCODERS_PATH, FEATURES_PATH, STATS_PATH, API_VERSION

router = APIRouter()


def _load_artifacts():
    try:
        model          = joblib.load(MODEL_PATH)
        label_encoders = joblib.load(ENCODERS_PATH)
        feature_names  = joblib.load(FEATURES_PATH)
        with open(STATS_PATH, "r") as f:
            stats = json.load(f)
        return model, label_encoders, feature_names, stats, True
    except Exception as e:
        print(f"[WARNING] Could not load artifacts: {e}")
        return None, None, None, {}, False


model, label_encoders, feature_names, training_stats, model_loaded = _load_artifacts()


def format_pkr(amount: float) -> str:
    if amount >= 1_00_00_000:
        return f"PKR {amount / 1_00_00_000:.2f} Crore"
    elif amount >= 1_00_000:
        return f"PKR {amount / 1_00_000:.2f} Lakh"
    return f"PKR {amount:,.0f}"


@router.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Returns API health status and whether the model is loaded."""
    return HealthResponse(
        status       = "ok" if model_loaded else "degraded",
        model_loaded = model_loaded,
        api_version  = API_VERSION,
    )


@router.get("/info", response_model=InfoResponse, tags=["System"])
def model_info():
    """Returns model training stats and all valid input options for dropdowns."""
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded. Run ml/train.py first.")
    return InfoResponse(
        model_type     = training_stats.get("model_type", "Unknown"),
        total_rows     = training_stats.get("total_rows", 0),
        r2_score       = training_stats.get("r2_score", 0.0),
        mae_pkr        = training_stats.get("mae_pkr", 0.0),
        locations      = training_stats.get("locations", []),
        property_types = training_stats.get("property_types", []),
        area_min_marla = training_stats.get("area_min_marla", 1.0),
        area_max_marla = training_stats.get("area_max_marla", 100.0),
    )


@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(request: PredictionRequest):
    """Predict the price of a residential property in Islamabad."""
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded. Run ml/train.py first.")

    pt_encoder = label_encoders["property_type"]
    if request.property_type not in pt_encoder.classes_:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid property_type '{request.property_type}'. Valid: {pt_encoder.classes_.tolist()}"
        )
    property_type_enc = int(pt_encoder.transform([request.property_type])[0])

    loc_encoder = label_encoders["location"]
    if request.location not in loc_encoder.classes_:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid location '{request.location}'. Use GET /info for valid locations."
        )
    location_enc = int(loc_encoder.transform([request.location])[0])

    features = np.array([[
        property_type_enc,
        location_enc,
        request.area_marla,
        request.bedrooms,
        request.bathrooms,
    ]], dtype=float)

    predicted_price = float(max(model.predict(features)[0], 0))
    price_per_marla = predicted_price / request.area_marla

    return PredictionResponse(
        predicted_price_pkr   = round(predicted_price, 2),
        predicted_price_label = format_pkr(predicted_price),
        price_per_marla_pkr   = round(price_per_marla, 2),
        price_per_marla_label = format_pkr(price_per_marla),
        input_summary         = {
            "property_type": request.property_type,
            "location"     : request.location,
            "area_marla"   : request.area_marla,
            "bedrooms"     : request.bedrooms,
            "bathrooms"    : request.bathrooms,
        },
        model_r2 = training_stats.get("r2_score", 0.0),
    )