from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
import uuid
from enum import Enum


class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    HALF_DAY = "HALF_DAY"
    LEAVE = "LEAVE"


class CheckInRequest(BaseModel):
    # Empty for now, but extensible for geolocation/remarks later
    pass


class CheckOutRequest(BaseModel):
    pass


class AttendanceOut(BaseModel):
    id: uuid.UUID
    employee_id: uuid.UUID
    work_date: date
    check_in: datetime | None
    check_out: datetime | None
    status: AttendanceStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttendanceWithHours(AttendanceOut):
    """Attendance record with calculated working hours."""
    working_hours: float = 0.0


class ManualAttendanceUpdate(BaseModel):
    """Schema for admin to manually update attendance."""
    check_in: datetime
    check_out: datetime
    status: AttendanceStatus


class AttendanceDateRangeRequest(BaseModel):
    """Request schema for filtering attendance by date range."""
    start_date: date
    end_date: date


class AttendanceSummary(BaseModel):
    """Summary statistics for attendance."""
    employee_id: uuid.UUID
    total_days: int
    present_days: int
    absent_days: int
    half_days: int
    leave_days: int
    total_working_hours: float

