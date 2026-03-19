"""
train.py
========
Trains a GradientBoostingRegressor on the cleaned Islamabad
housing dataset and saves all artifacts required by the API.

Usage:
    python ml/train.py
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

PROCESSED_PATH = os.path.join("data", "processed", "clean_data.csv")
ARTIFACTS_DIR  = os.path.join("ml", "artifacts")

MODEL_PATH    = os.path.join(ARTIFACTS_DIR, "model.pkl")
ENCODERS_PATH = os.path.join(ARTIFACTS_DIR, "label_encoders.pkl")
FEATURES_PATH = os.path.join(ARTIFACTS_DIR, "feature_names.pkl")
STATS_PATH    = os.path.join(ARTIFACTS_DIR, "training_stats.json")

os.makedirs(ARTIFACTS_DIR, exist_ok=True)


def format_pkr(amount: float) -> str:
    if amount >= 1_00_00_000:
        return f"PKR {amount / 1_00_00_000:.2f} Crore"
    elif amount >= 1_00_000:
        return f"PKR {amount / 1_00_000:.2f} Lakh"
    return f"PKR {amount:,.0f}"


def train():
    print("=" * 55)
    print("  Islamabad House Price — Training Pipeline")
    print("=" * 55)

    print(f"\n[1/6] Loading data from: {PROCESSED_PATH}")
    df = pd.read_csv(PROCESSED_PATH)
    print(f"      Rows: {len(df):,}  |  Columns: {df.columns.tolist()}")

    print("\n[2/6] Encoding categorical columns...")
    categorical_cols = ["property_type", "location"]
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col + "_enc"] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le
        print(f"      '{col}' → {len(le.classes_)} unique values")

    print("\n[3/6] Preparing features and target...")
    feature_names = ["property_type_enc", "location_enc", "area_marla", "bedrooms", "bathrooms"]
    X = df[feature_names].values
    y = df["price_pkr"].values
    print(f"      Features : {feature_names}")
    print(f"      X shape  : {X.shape}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\n[4/6] Train/test split: {len(X_train)} train | {len(X_test)} test")

    print("\n[5/6] Training GradientBoostingRegressor...")
    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        min_samples_split=5,
        min_samples_leaf=3,
        subsample=0.8,
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred    = model.predict(X_test)
    mae       = mean_absolute_error(y_test, y_pred)
    r2        = r2_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")

    print(f"\n      MAE        : {format_pkr(mae)}")
    print(f"      R²         : {r2:.4f}  ({r2*100:.1f}%)")
    print(f"      CV R² (5x) : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print("\n      Feature importances:")
    for fname, imp in sorted(zip(feature_names, model.feature_importances_), key=lambda x: x[1], reverse=True):
        bar = "█" * int(imp * 40)
        print(f"        {fname:<22} {bar}  {imp:.4f}")

    print(f"\n[6/6] Saving artifacts to: {ARTIFACTS_DIR}/")
    joblib.dump(model,          MODEL_PATH)
    joblib.dump(label_encoders, ENCODERS_PATH)
    joblib.dump(feature_names,  FEATURES_PATH)

    stats = {
        "model_type"       : "GradientBoostingRegressor",
        "total_rows"       : len(df),
        "train_rows"       : len(X_train),
        "test_rows"        : len(X_test),
        "features"         : feature_names,
        "mae_pkr"          : round(mae, 2),
        "r2_score"         : round(r2, 4),
        "cv_r2_mean"       : round(float(cv_scores.mean()), 4),
        "cv_r2_std"        : round(float(cv_scores.std()), 4),
        "price_min_pkr"    : int(df["price_pkr"].min()),
        "price_max_pkr"    : int(df["price_pkr"].max()),
        "price_median_pkr" : int(df["price_pkr"].median()),
        "locations"        : sorted(df["location"].unique().tolist()),
        "property_types"   : sorted(df["property_type"].unique().tolist()),
        "area_min_marla"   : float(df["area_marla"].min()),
        "area_max_marla"   : float(df["area_marla"].max()),
        "bedroom_min"      : int(df["bedrooms"].min()),
        "bedroom_max"      : int(df["bedrooms"].max()),
        "bathroom_min"     : int(df["bathrooms"].min()),
        "bathroom_max"     : int(df["bathrooms"].max()),
    }
    with open(STATS_PATH, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"      ✓ model.pkl")
    print(f"      ✓ label_encoders.pkl")
    print(f"      ✓ feature_names.pkl")
    print(f"      ✓ training_stats.json")
    print("\n" + "=" * 55)
    print("  DONE")
    print("=" * 55)
    print(f"  R² Score   : {r2:.4f}  ({r2*100:.1f}%)")
    print(f"  Mean Error : {format_pkr(mae)}")
    print(f"  Locations  : {len(label_encoders['location'].classes_)} areas")
    print("=" * 55)


if __name__ == "__main__":
    train()