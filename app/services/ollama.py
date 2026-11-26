"""Ollama HTTP client used by future feature modules.

Text generation and structured JSON generation are intentionally not
implemented yet. This module only checks whether the local Ollama server
can be reached. A connection failure is reported to the caller and is never
raised during application startup.
"""

from dataclasses import dataclass

import httpx

from app.core.config import Settings, get_settings


@dataclass(frozen=True)
class OllamaStatus:
    """Result of a non-fatal Ollama connectivity check."""

    available: bool
    detail: str


class OllamaService:
    """Reusable client for the local Ollama HTTP API.

    Future methods on this class are the single place for text generation
    and structured JSON generation. Feature modules should receive this
    service through dependency injection rather than creating their own
    HTTP clients.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        timeout_seconds: float = 2.0,
    ) -> None:
        self._settings = settings or get_settings()
        self._timeout_seconds = timeout_seconds

    @property
    def base_url(self) -> str:
        return self._settings.ollama_base_url.rstrip("/")

    @property
    def model(self) -> str:
        return self._settings.ollama_model

    def check_availability(self) -> OllamaStatus:
        """Return whether the configured Ollama server responds.

        This calls ``GET /api/tags``. It does not pull a model and it does
        not send a generation request.
        """
        url = f"{self.base_url}/api/tags"
        try:
            response = httpx.get(url, timeout=self._timeout_seconds)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            return OllamaStatus(available=False, detail=str(exc))
        return OllamaStatus(
            available=True,
            detail=f"Ollama is reachable. Configured model: {self.model}.",
        )


def get_ollama_service() -> OllamaService:
    """FastAPI dependency that provides the shared Ollama client."""
    return OllamaService()
