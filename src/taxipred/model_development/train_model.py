from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from taxipred.backend.data_processing import (
    clean_data,
    get_features_and_target,
    load_raw_data,
)

# src/taxipred
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "backend" / "model.joblib"


def train():
    print("Loading data...")
    df_raw = load_raw_data()
    df_clean = clean_data(df_raw)
    X, y = get_features_and_target(df_clean)

    print(f"Data shape after cleaning: {df_clean.shape}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training model...")
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"MAE: {mae:.2f}")
    print(f"R2 score: {r2:.3f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train()
