from datetime import date
from pydantic import BaseModel, ConfigDict


# Shared base
class UserBase(BaseModel):
    full_name: str
    email: str
    role: str
    company: str
    phone: str
    created_at: date


# Create request (Admin only)
class UserCreate(UserBase):
    id: str
    password: str


# Update request (limited fields)
class UserUpdate(BaseModel):
    company: str | None = None
    phone: str | None = None


# Response model
class UserOut(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
