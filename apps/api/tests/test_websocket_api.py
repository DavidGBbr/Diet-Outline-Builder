from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.agent import AgentTurnResult
from app.domain import build_diet_outline
from app.main import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    original_runner = app.state.conversation_runner
    with TestClient(app) as test_client:
        yield test_client
    app.state.conversation_runner = original_runner


def test_health_returns_ok_and_security_headers(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_websocket_rejects_invalid_message_shape(client: TestClient) -> None:
    with client.websocket_connect("/ws/chat") as websocket:
        websocket.send_json({"type": "unknown"})
        message = websocket.receive_json()

    assert message == {
        "type": "error",
        "code": "invalid_message",
        "message": "Send a valid user_message with text and optional state.",
    }


def test_websocket_maps_agent_turn_to_protocol_messages(client: TestClient) -> None:
    diet_result = build_diet_outline(
        {
            "sex": "male",
            "age": 22,
            "heightCM": 178,
            "weightKG": 87.4,
            "activityLevel": "moderate",
            "goal": "lose_fat",
        }
    )

    def fake_runner(message) -> AgentTurnResult:
        return AgentTurnResult(
            assistant_message="I have everything I need.",
            collected_data={"sex": "male", "age": 22},
            missing_fields=[],
            invalid_fields=[],
            diet_result=diet_result,
        )

    app.state.conversation_runner = fake_runner

    with client.websocket_connect("/ws/chat") as websocket:
        websocket.send_json(
            {
                "type": "user_message",
                "text": "Male, 22, 178cm, 87.4kg, moderate, lose fat.",
                "state": {"collectedData": {}},
            }
        )
        assistant_message = websocket.receive_json()
        diet_message = websocket.receive_json()
        state_message = websocket.receive_json()

    assert assistant_message == {
        "type": "assistant_message",
        "text": "I have everything I need.",
    }
    assert diet_message["type"] == "diet_result"
    assert diet_message["result"]["imcClassification"] == "overweight"
    assert state_message == {
        "type": "state_snapshot",
        "state": {
            "collectedData": {"sex": "male", "age": 22},
            "missingFields": [],
            "invalidFields": [],
        },
    }
