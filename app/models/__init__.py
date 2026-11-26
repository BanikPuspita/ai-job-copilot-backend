"""SQLAlchemy models.

Import each model module here when it is added. Alembic imports this package
so those models are registered on ``Base.metadata`` before autogenerate runs.
No product tables are defined yet.
"""

from app.core.database import Base

__all__ = ["Base"]
