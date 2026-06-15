from __future__ import annotations

from app.agent import AgentTurnInput, AgentTurnResult, run_conversation_turn
from app.schemas import IncomingChatMessage


def run_api_conversation_turn(message: IncomingChatMessage) -> AgentTurnResult:
    return run_conversation_turn(
        AgentTurnInput(
            message=message.text,
            collected_data=message.state.collected_data,
        )
    )
