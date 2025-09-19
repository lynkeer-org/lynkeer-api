from pydantic import BaseModel, EmailStr
from datetime import date
import uuid

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_date: date

class CustomerResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_date: date
    created_at: str
    updated_at: str | None = None
    active: bool