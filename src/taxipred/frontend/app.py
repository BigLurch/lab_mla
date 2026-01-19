import httpx
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"


def call_backend_predict(payload: dict) -> dict | None:
    """Send features to the FastAPI backend and return the prediction."""
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(f"{BACKEND_URL}/predict", json=payload)
            response.raise_for_status()
        return response.json()
    except Exception as exc:  # noqa: BLE001
        st.error(f"Error while calling backend: {exc}")
        return None


def main() -> None:
    st.set_page_config(page_title="Taxi Price Prediction", page_icon="🫆")

    st.title("Taxi Price Prediction")
    st.write(
        "Enter trip details below and click **Predict price** to get an estimated taxi fare."
    )

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            trip_distance_km = st.number_input(
                "Trip distance (km)",
                min_value=0.1,
                max_value=500.0,
                value=5.0,
                step=0.1,
            )
            trip_duration_minutes = st.number_input(
                "Trip duration (minutes)",
                min_value=1.0,
                max_value=600.0,
                value=15.0,
                step=1.0,
            )
            passenger_count = st.number_input(
                "Passenger count",
                min_value=1,
                max_value=8,
                value=1,
                step=1,
            )

        with col2:
            base_fare = st.number_input(
                "Base fare (SEK)",
                min_value=0.0,
                max_value=500.0,
                value=40.0,
                step=1.0,
            )
            per_km_rate = st.number_input(
                "Per km rate (SEK)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.5,
            )
            per_minute_rate = st.number_input(
                "Per minute rate (SEK)",
                min_value=0.0,
                max_value=50.0,
                value=2.0,
                step=0.5,
            )

        submitted = st.form_submit_button("Predict price")

    if submitted:
        payload = {
            "Trip_Distance_km": trip_distance_km,
            "Trip_Duration_Minutes": trip_duration_minutes,
            "Passenger_Count": passenger_count,
            "Base_Fare": base_fare,
            "Per_Km_Rate": per_km_rate,
            "Per_Minute_Rate": per_minute_rate,
        }

        st.write("Sending request to backend…")
        result = call_backend_predict(payload)

        if result is not None and "predicted_price" in result:
            st.success(
                f"Estimated taxi price: **{result['predicted_price']} {result.get('currency', 'SEK')}**"
            )
        elif result is not None:
            st.warning(f"Unexpected response from backend: {result}")


if __name__ == "__main__":
    main()
else:
    main()
