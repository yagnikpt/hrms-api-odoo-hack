from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict


# Shared base
class EmployeeBase(BaseModel):
    full_name: str
    job_title: str
    department: str
    phone: str | None = None
    address: str | None = None


# Create request (Admin only)
class EmployeeCreate(EmployeeBase):
    user_id: UUID
    employee_code: str
    date_of_joining: date


# Update request (limited fields)
class EmployeeUpdate(BaseModel):
    phone: str | None = None
    address: str | None = None
    profile_picture_url: str | None = None


# Response model
class EmployeeOut(EmployeeBase):
    id: UUID
    employee_code: str
    date_of_joining: date

    model_config = ConfigDict(from_attributes=True)
