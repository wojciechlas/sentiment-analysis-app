import pytest
from fastapi.testclient import TestClient
from app import app, inference

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello in Text Analysis API. Go to /docs for more information."
    }


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == 200


def test_model_loading():
    assert inference is not None, "Model failed to load from cloudpickle file."


@pytest.mark.parametrize(
    "input_text, expected_prediction",
    [
        ("I love this product!", "positive"),
        ("This is the worst experience ever.", "negative"),
    ],
)
def test_predict_endpoint(input_text, expected_prediction):
    response = client.post("/predict/", json={"text": input_text})
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], str)


def test_invalid_input():
    response = client.post("/predict/", json={"text": ""})
    assert response.status_code == 422  # Unprocessable Entity

    response = client.post("/predict/", json={})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"][0]["msg"] == "Field required"
