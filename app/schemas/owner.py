from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Session, select
from datetime import datetime, timezone
from models.owner import OwnerBase
from db import engine
import uuid


class OwnerResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime
    active: bool


class OwnerCreate(OwnerBase):
    password: str


class OwnerUpdate(OwnerBase):
    pass
