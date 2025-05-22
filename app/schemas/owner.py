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
    active: bool


class OwnerCreate(OwnerBase):
    password: str


class OwnerUpdate(OwnerBase):
    pass


class OwnerLogin(BaseModel):
    email: EmailStr
    password: str
