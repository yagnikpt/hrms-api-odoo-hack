from datetime import date, time
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from src.users.schemas import UserCreate, UserOut


# Shared base
class EmployeeBase(BaseModel):
    job_title: str
    department: str
    address: str | None = None
    check_in_time: time | None = None
    check_out_time: time | None = None


# Create request (Admin only)
class EmployeeCreate(EmployeeBase):
    user: UserCreate
    date_of_joining: date
    profile_picture_url: str | None = None


# Update request (limited fields)
class EmployeeUpdate(BaseModel):
    job_title: str | None = None
    department: str | None = None
    address: str | None = None
    profile_picture_url: str | None = None
    check_in_time: time | None = None
    check_out_time: time | None = None


# Response model
class EmployeeOut(EmployeeBase):
    id: UUID
    user: UserOut

    model_config = ConfigDict(from_attributes=True)
