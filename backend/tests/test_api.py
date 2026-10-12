
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Stock News API is running!"
    }


def test_missing_finnhub_key(monkeypatch):
    monkeypatch.setattr("main.FINNHUB_API_KEY", None)

    response = client.get("/stocks/AAPL")

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Finnhub API key is missing"
    )
