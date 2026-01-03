from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict


# Shared base
class EmployeeBase(BaseModel):
    job_title: str
    department: str
    address: str | None = None
    check_in_time: str | None = None
    check_out_time: str | None = None


# Create request (Admin only)
class EmployeeCreate(EmployeeBase):
    user_id: str
    date_of_joining: date
    profile_picture_url: str | None = None


# Update request (limited fields)
class EmployeeUpdate(BaseModel):
    phone: str | None = None
    address: str | None = None
    profile_picture_url: str | None = None
    check_in_time: str | None = None
    check_out_time: str | None = None


# Response model
class EmployeeOut(EmployeeBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
