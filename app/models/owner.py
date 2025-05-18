from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Session, select
from datetime import datetime, timezone
from app.core.db import engine
import uuid


class OwnerBase(SQLModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    email: EmailStr = Field(default=None)  # Use EmailStr for validation
    phone: str = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Owner).where(Owner.email == value)
        email_exists = session.exec(query).first()
        if email_exists:
            raise ValueError("Email already registered")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        session = Session(engine)
        query = select(Owner).where(Owner.phone == value)
        phone_exists = session.exec(query).first()
        if phone_exists:
            raise ValueError("Phone already registered")

        return value


class Owner(OwnerBase, table=True):
    # id: int | None = Field(default=None, primary_key=True)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    password_hash: str = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool | None = Field(default=True)
