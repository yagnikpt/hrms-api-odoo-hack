from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
import uuid

class LeaveTypeBase(BaseModel):
    name: str = Field(..., max_length=50)
    is_paid: bool = True

class LeaveTypeCreate(LeaveTypeBase):
    pass

class LeaveTypeOut(LeaveTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class LeaveRequestBase(BaseModel):
    leave_type_id: int
    start_date: date
    end_date: date
    remarks: Optional[str] = None

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequestUpdate(BaseModel):
    status: str = Field(..., pattern="^(APPROVED|REJECTED)$")
    review_comment: Optional[str] = None

class LeaveRequestOut(LeaveRequestBase):
    id: uuid.UUID
    employee_id: uuid.UUID
    status: str
    reviewed_by: Optional[str] = None
    review_comment: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    leave_type: LeaveTypeOut

    model_config = ConfigDict(from_attributes=True)
