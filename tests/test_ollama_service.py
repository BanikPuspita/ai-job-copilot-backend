"""Ollama connectivity tests that do not contact a real server."""

import httpx
import pytest

from app.core.config import Settings
from app.services.ollama import OllamaService


def test_check_availability_handles_connection_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_get(*args: object, **kwargs: object) -> httpx.Response:
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(httpx, "get", fail_get)
    service = OllamaService(settings=Settings())

    status = service.check_availability()

    assert status.available is False
    assert "connection refused" in status.detail


def test_check_availability_reports_reachable_server(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def succeed_get(*args: object, **kwargs: object) -> httpx.Response:
        request = httpx.Request("GET", "http://127.0.0.1:11434/api/tags")
        return httpx.Response(200, request=request)

    monkeypatch.setattr(httpx, "get", succeed_get)
    service = OllamaService(
        settings=Settings(ollama_model="llama3.2"),
    )

    status = service.check_availability()

    assert status.available is True
    assert "llama3.2" in status.detail
