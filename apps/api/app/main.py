from __future__ import annotations

from collections.abc import Callable

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.agent import AgentTurnResult
from app.schemas import (
    AssistantMessage,
    DietResultMessage,
    ErrorMessage,
    IncomingChatMessage,
    ServerConversationState,
    StateSnapshotMessage,
)
from app.services import run_api_conversation_turn


ConversationRunner = Callable[[IncomingChatMessage], AgentTurnResult]


def _json(model) -> dict:
    return model.model_dump(mode="json", by_alias=True)


async def _send_error(websocket: WebSocket, code: str, message: str) -> None:
    await websocket.send_json(_json(ErrorMessage(code=code, message=message)))


async def _send_turn_result(websocket: WebSocket, result: AgentTurnResult) -> None:
    if result.assistant_message:
        await websocket.send_json(
            _json(AssistantMessage(text=result.assistant_message))
        )

    if result.error is not None:
        await websocket.send_json(
            _json(ErrorMessage(code=result.error.code, message=result.error.message))
        )

    if result.diet_result is not None:
        await websocket.send_json(_json(DietResultMessage(result=result.diet_result)))

    await websocket.send_json(
        _json(
            StateSnapshotMessage(
                state=ServerConversationState(
                    collected_data=result.collected_data,
                    missing_fields=result.missing_fields,
                    invalid_fields=result.invalid_fields,
                )
            )
        )
    )


def create_app() -> FastAPI:
    api = FastAPI(title="Diet Outline Builder API")
    api.state.conversation_runner = run_api_conversation_turn

    api.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["content-type"],
    )

    @api.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @api.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @api.websocket("/ws/chat")
    async def chat(websocket: WebSocket) -> None:
        await websocket.accept()
        runner: ConversationRunner = websocket.app.state.conversation_runner

        try:
            while True:
                raw_message = await websocket.receive_json()
                try:
                    message = IncomingChatMessage.model_validate(raw_message)
                except ValidationError:
                    await _send_error(
                        websocket,
                        "invalid_message",
                        "Send a valid user_message with text and optional state.",
                    )
                    continue

                try:
                    result = runner(message)
                except Exception:
                    await _send_error(
                        websocket,
                        "internal_error",
                        "Something went wrong while processing the message.",
                    )
                    continue

                await _send_turn_result(websocket, result)
        except WebSocketDisconnect:
            return

    return api


app = create_app()
