"""
config.py
=========
Central configuration for the FastAPI application.
"""

import os

BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "ml", "artifacts")

MODEL_PATH    = os.path.join(ARTIFACTS_DIR, "model.pkl")
ENCODERS_PATH = os.path.join(ARTIFACTS_DIR, "label_encoders.pkl")
FEATURES_PATH = os.path.join(ARTIFACTS_DIR, "feature_names.pkl")
STATS_PATH    = os.path.join(ARTIFACTS_DIR, "training_stats.json")

API_TITLE       = "Islamabad House Price Predictor API"
API_DESCRIPTION = "ML-powered residential property valuation for Islamabad, Pakistan."
API_VERSION     = "1.0.0"
API_HOST        = "0.0.0.0"
API_PORT        = 8000