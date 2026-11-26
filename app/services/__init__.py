"""Application services.

Business logic and external integrations live here. API routes should depend
on these services instead of calling the database or Ollama directly.
"""

from app.services.ollama import OllamaService, OllamaStatus

__all__ = ["OllamaService", "OllamaStatus"]
