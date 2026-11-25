from datetime import date

from fastapi.testclient import TestClient

from main import app
from rules import trip_length_days

client = TestClient(app)


def test_trip_length_includes_both_dates():
    assert trip_length_days(
        date(2026, 12, 31),
        date(2027, 1, 2),
    ) == 3


def test_endpoint_returns_trip_duration():
    response = client.post(
        "/api/v1/trip-duration",
        json={
            "start_date": "2026-12-01",
            "end_date": "2026-12-03",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"days": 3}


def test_endpoint_rejects_reversed_dates():
    response = client.post(
        "/api/v1/trip-duration",
        json={
            "start_date": "2026-12-03",
            "end_date": "2026-12-01",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "End date must be on or after start date."
    )
