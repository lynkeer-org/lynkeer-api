from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.owner import OwnerBase
import uuid


class OwnerResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime
    updated_at: datetime | None = None
    active: bool


class OwnerCreate(OwnerBase):
    password: str


class OwnerUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class OwnerDelete(BaseModel):
    active: bool = False  # Set active to False to mark as deleted


class OwnerLogin(BaseModel):
    email: EmailStr
    password: str
