"""
preprocess.py
=============
Cleans and prepares the raw Zameen.com dataset for model training.
Filters Islamabad listings, parses prices and area units,
handles missing values, removes outliers, and saves clean data.

Usage:
    python ml/preprocess.py
"""

import os
import re
import pandas as pd
import numpy as np

RAW_PATH       = os.path.join("data", "raw", "islamabad_fresh.csv")
PROCESSED_PATH = os.path.join("data", "processed", "clean_data.csv")

VALID_TYPES = ["House", "Flat", "Upper Portion", "Lower Portion", "Farm House"]


def parse_price(raw: str) -> float:
    """Convert PKR string (e.g. 'PKR 2.5 Crore') to a float in PKR."""
    if not isinstance(raw, str):
        return np.nan
    text = raw.replace("\n", " ").replace(",", "").strip().upper()
    match = re.search(r"[\d.]+", text)
    if not match:
        return np.nan
    value = float(match.group())
    if "CRORE" in text:
        return value * 1_00_00_000
    elif "LAC" in text or "LAKH" in text:
        return value * 1_00_000
    elif "THOUSAND" in text or "HAZAR" in text:
        return value * 1_000
    return value


def parse_area_to_marla(raw: str) -> float:
    """Convert area string (Marla / Kanal / Sqyd / Sqft) to Marla."""
    if not isinstance(raw, str):
        return np.nan
    text = raw.strip().upper()
    match = re.search(r"[\d.]+", text)
    if not match:
        return np.nan
    value = float(match.group())
    if "KANAL" in text:
        return value * 20
    elif "MARLA" in text:
        return value
    elif "SQYD" in text or "SQ. YD" in text or "SQUARE YARD" in text:
        return round(value * 0.0337, 2)
    elif "SQFT" in text or "SQ. FT" in text or "SQUARE FEET" in text:
        return round(value * 0.00313, 2)
    return np.nan


def parse_rooms(val) -> float:
    """Parse bedroom/bathroom value, returning NaN for missing or zero."""
    if val in ["-", "", "none", "null", None]:
        return np.nan
    try:
        v = float(val)
        return np.nan if v == 0 else v
    except (ValueError, TypeError):
        return np.nan


def clean_location(loc: str) -> str:
    """
    Normalize compound location strings from the scraper.
    e.g. 'DHA Defence Phase 2, DHA Defence' -> 'DHA Defence'
         'F-7, Islamabad'                   -> 'F-7'
    """
    if not isinstance(loc, str):
        return loc
    loc = loc.strip()
    if "," in loc:
        parts = [p.strip() for p in loc.split(",")]
        if parts[-1].lower() in ["islamabad", "rawalpindi", "pakistan"]:
            return parts[0]
        return parts[-1]
    return loc


def preprocess():
    print("=" * 55)
    print("  Islamabad House Price — Preprocessing Pipeline")
    print("=" * 55)

    print(f"\n[1/7] Loading raw data from: {RAW_PATH}")
    df = pd.read_csv(RAW_PATH)
    print(f"      Raw rows: {len(df):,}")

    print("\n[2/7] Filtering for Islamabad...")
    df = df[df["location_city"].str.strip().str.lower() == "islamabad"].copy()
    print(f"      Rows after city filter: {len(df):,}")

    print("\n[3/7] Keeping 'For Sale' listings only...")
    df = df[df["purpose"].str.strip().str.lower() == "for sale"].copy()
    print(f"      Rows after purpose filter: {len(df):,}")

    print("\n[4/7] Keeping residential property types...")
    df = df[df["type"].isin(VALID_TYPES)].copy()
    print(f"      Rows after type filter: {len(df):,}")

    print("\n[5/7] Parsing and cleaning columns...")
    df["price_pkr"]     = df["price"].apply(parse_price)
    df["area_marla"]    = df["area"].apply(parse_area_to_marla)
    df["bedrooms"]      = df["bedroom"].apply(parse_rooms)
    df["bathrooms"]     = df["bath"].apply(parse_rooms)
    df["property_type"] = df["type"].str.strip()
    df["location"]      = df["location"].apply(clean_location)

    df = df.dropna(subset=["price_pkr", "area_marla"])
    print(f"      Rows after dropping missing price/area: {len(df):,}")

    df["bedrooms"]  = df["bedrooms"].fillna(df["bedrooms"].median()).astype(int)
    df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms"].median()).astype(int)

    print("\n[6/7] Removing outliers...")
    low  = df["price_pkr"].quantile(0.025)
    high = df["price_pkr"].quantile(0.975)
    df   = df[(df["price_pkr"] >= low) & (df["price_pkr"] <= high)]
    df   = df[(df["area_marla"] >= 1)  & (df["area_marla"] <= 100)]
    print(f"      Price range: PKR {low:,.0f} — PKR {high:,.0f}")
    print(f"      Rows after outlier removal: {len(df):,}")

    final_cols = ["property_type", "location", "area_marla", "bedrooms", "bathrooms", "price_pkr"]
    df = df[final_cols].reset_index(drop=True)

    print(f"\n[7/7] Saving to: {PROCESSED_PATH}")
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print("\n" + "=" * 55)
    print("  DONE — Clean Dataset Summary")
    print("=" * 55)
    print(f"  Total rows     : {len(df):,}")
    print(f"  Property types :\n{df['property_type'].value_counts().to_string()}")
    print(f"\n  Top 10 locations :\n{df['location'].value_counts().head(10).to_string()}")
    print(f"\n  Area   : {df['area_marla'].min()} – {df['area_marla'].max()} Marla")
    print(f"  Price  : PKR {df['price_pkr'].min():,.0f} – {df['price_pkr'].max():,.0f}")
    print(f"  Median : PKR {df['price_pkr'].median():,.0f}")
    print("=" * 55)


if __name__ == "__main__":
    preprocess()