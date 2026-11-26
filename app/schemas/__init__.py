"""Pydantic schemas used at the API boundary."""

from app.schemas.health import AppInfoResponse, HealthResponse

__all__ = ["AppInfoResponse", "HealthResponse"]
