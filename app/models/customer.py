import uuid
from datetime import datetime, date, timezone
from pydantic import EmailStr, field_validator
from sqlmodel import Relationship, SQLModel, Field, Session, select
from typing import TYPE_CHECKING, Optional
from app.core.db import engine
from app.models.customer_pass import CustomerPass

if TYPE_CHECKING:
    from app.models.pass_model import PassModel
   

class CustomerBase(SQLModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    phone: str = Field(default=None)
    birth_date: date = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        email_exists = session.exec(query).first()
        if email_exists:
            raise ValueError("Email already registered")
        return value

    

class Customer(CustomerBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    passes: list["PassModel"] = Relationship(back_populates='customers', link_model=CustomerPass)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = Field(default=True)