from fastapi.testclient import TestClient

from diet_outline_builder.web import create_app


SAMPLE_INPUT = {
    "sex": "male",
    "age": 22,
    "heightCM": 178,
    "weightKG": 87.4,
    "activityLevel": "moderate",
    "goal": "lose_fat",
}


def test_index_serves_local_ui() -> None:
    client = TestClient(create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert "Diet Outline Builder" in response.text
    assert "Build diet outline" in response.text


def test_api_returns_diet_outline() -> None:
    client = TestClient(create_app())

    response = client.post("/api/diet", json=SAMPLE_INPUT)

    assert response.status_code == 200
    assert response.json()["macros"] == {"protein": 140, "fat": 52, "carb": 326}


def test_api_returns_400_for_invalid_input() -> None:
    client = TestClient(create_app())

    response = client.post("/api/diet", json=SAMPLE_INPUT | {"activityLevel": "extreme"})

    assert response.status_code == 400
    assert "activityLevel" in response.json()["detail"]
