from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from app.agent.prompts import build_extraction_prompt


class OllamaUnavailableError(RuntimeError):
    pass


class OllamaExtractionClient:
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout_seconds: float = 15,
    ) -> None:
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434").rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL") or "llama3.1:8b"
        self.timeout_seconds = timeout_seconds

    def extract_fields(self, message: str) -> dict[str, Any]:
        body = json.dumps(
            {
                "model": self.model,
                "prompt": build_extraction_prompt(message),
                "stream": False,
                "format": "json",
            }
        ).encode("utf-8")
        request = Request(
            f"{self.base_url}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise OllamaUnavailableError(
                "Ollama is unavailable or returned an unreadable response."
            ) from exc

        raw_model_response = payload.get("response", "")
        if not isinstance(raw_model_response, str):
            return {}

        try:
            extracted = json.loads(raw_model_response)
        except json.JSONDecodeError:
            return {}

        return extracted if isinstance(extracted, dict) else {}
