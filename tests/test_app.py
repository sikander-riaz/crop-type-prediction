from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_success():
    response = client.post(
        "/predict",
        json={
            "Nitrogen": 90, "Phosphorus": 42, "Potassium": 43, "Temperature": 20.879744,
            "Humidity": 82.002744, "PH": 6.502985, "Rainfall": 202.935536
        }
    )
    assert response.status_code == 200
    assert "predicted_category" in response.json()
    assert isinstance(response.json()["predicted_category"], str)

def test_predict_invalid_input():
    response = client.post(
        "/predict",
        json={
            "N": "invalid", "P": 42, "K": 43, "temperature": 20.879744,
            "humidity": 82.002744, "ph": 6.502985, "rainfall": 202.935536
        }
    )
    assert response.status_code == 422 # Unprocessable Entity for validation errors
    assert "detail" in response.json()