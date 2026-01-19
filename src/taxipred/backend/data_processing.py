from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "taxi_trip_pricing.csv"

FEATURE_COLS = [
    "Trip_Distance_km",
    "Trip_Duration_Minutes",
    "Passenger_Count",
    "Base_Fare",
    "Per_Km_Rate",
    "Per_Minute_Rate",
]
TARGET_COL = "Trip_Price"


def load_raw_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load raw data from CSV."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Do basic data cleaning."""
    df = df.copy()

    # Delete rows without labels
    df = df.dropna(subset=[TARGET_COL] + FEATURE_COLS)

    # Remove impossible/strange values ​​(negative or zero)
    df = df[df["Trip_Distance_km"] > 0]
    df = df[df["Trip_Duration_Minutes"] > 0]
    df = df[df["Base_Fare"] >= 0]
    df = df[df["Per_Km_Rate"] >= 0]
    df = df[df["Per_Minute_Rate"] >= 0]
    df = df[df[TARGET_COL] > 0]

    # Remove extreme outliers (simple but effective method)
    df = df[df[TARGET_COL] < df[TARGET_COL].quantile(0.99)]
    df = df[df["Trip_Distance_km"] < df["Trip_Distance_km"].quantile(0.99)]
    df = df[df["Trip_Duration_Minutes"] < df["Trip_Duration_Minutes"].quantile(0.99)]

    return df


def get_features_and_target(df: pd.DataFrame):
    """Return X (features) and y (target)."""
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    return X, y
