from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime, timezone


class PassTypeBase(SQLModel):
    type: str = Field(default=None)


class PassType(PassTypeBase, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool | None = Field(default=True)
