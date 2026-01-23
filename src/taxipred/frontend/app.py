import httpx
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

DEFAULT_BASE_FARE = 40.0
DEFAULT_PER_KM_RATE = 10.0
DEFAULT_PER_MINUTE_RATE = 2.0


def call_backend_predict(payload: dict) -> dict | None:
    """Send features to the FastAPI backend and return the prediction."""
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(f"{BACKEND_URL}/predict", json=payload)
            response.raise_for_status()
        return response.json()
    except Exception as exc:
        st.error(f"Error while calling backend: {exc}")
        return None


def main() -> None:
    st.set_page_config(page_title="Taxi Price Prediction", page_icon="🚕")

    st.title("Taxi Price Prediction")
    st.write(
        "Enter trip details below and click **Predict price** to get an estimated taxi fare."
    )

    st.markdown("#### Trip information")

    with st.form("prediction_form"):
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

        submitted = st.form_submit_button("Predict price")

    if submitted:
        payload = {
            "Trip_Distance_km": trip_distance_km,
            "Trip_Duration_Minutes": trip_duration_minutes,
            "Passenger_Count": passenger_count,
            "Base_Fare": DEFAULT_BASE_FARE,
            "Per_Km_Rate": DEFAULT_PER_KM_RATE,
            "Per_Minute_Rate": DEFAULT_PER_MINUTE_RATE,
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
