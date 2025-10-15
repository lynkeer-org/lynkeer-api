import uuid
from datetime import datetime, date, timezone
from pydantic import EmailStr
from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, Optional
from app.models.customer_pass import CustomerPass

if TYPE_CHECKING:
    from app.models.pass_model import PassModel
   

class CustomerBase(SQLModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    phone: str = Field(default=None)
    birth_date: date = Field(default=None)

    

class Customer(CustomerBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    passes: list["PassModel"] = Relationship(back_populates='customers', link_model=CustomerPass)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = Field(default=True)