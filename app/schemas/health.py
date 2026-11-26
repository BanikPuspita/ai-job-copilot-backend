"""Response schemas for application information and health checks."""

from pydantic import BaseModel, Field


class AppInfoResponse(BaseModel):
    """Public description of the running application."""

    name: str
    environment: str
    version: str
    docs: str = Field(description="Path to the interactive API documentation.")


class HealthResponse(BaseModel):
    """Lightweight process health status."""

    status: str
    service: str
