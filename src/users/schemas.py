from datetime import datetime
from pydantic import BaseModel, ConfigDict


# Shared base
class UserBase(BaseModel):
    full_name: str
    email: str
    role: str
    company: str
    phone: str | None = None


# Create request (Admin only)
class UserCreate(UserBase):
    password: str


# Update request (limited fields)
class UserUpdate(BaseModel):
    company: str | None = None
    phone: str | None = None


# Response model
class UserOut(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
