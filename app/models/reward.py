from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.customer_pass import CustomerPass

class Reward(SQLModel, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    customer_pass_id: uuid.UUID = Field(foreign_key="customerpass.id", nullable=False)
    customer_pass: "CustomerPass" = Relationship(back_populates="rewards")
    claimed_at: datetime | None = Field(default=None)  # When the reward was claimed - set when customer redeems
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # When the reward was issued
    active: bool = Field(default=True)
