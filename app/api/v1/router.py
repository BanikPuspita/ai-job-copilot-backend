"""Version 1 route registration.

Add feature routers here when they are introduced. Keep handlers thin:
validate input with Pydantic schemas, then call a service.
"""

from fastapi import APIRouter

from app.schemas.health import HealthResponse

api_router = APIRouter()


@api_router.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    """Report that the versioned API process is running."""
    return HealthResponse(status="ok", service="api-v1")
