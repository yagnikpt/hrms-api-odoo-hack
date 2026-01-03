from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.deps import get_db, get_current_user, admin_required
from src.users.models import User
from src.attendance.schemas import (
    AttendanceOut,
    AttendanceWithHours,
    CheckInRequest,
    CheckOutRequest,
    ManualAttendanceUpdate,
)
from src.attendance.services import AttendanceService
from datetime import date
import uuid

router = APIRouter(prefix="/attendance", tags=["Attendance"])
service = AttendanceService()


@router.post("/check-in", response_model=AttendanceOut)
async def check_in(
    data: CheckInRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Employee: Clock In.
    Creates a new attendance record for today.
    """
    return await service.check_in(db, current_user.id)


@router.post("/check-out", response_model=AttendanceOut)
async def check_out(
    data: CheckOutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Employee: Clock Out.
    Updates today's record with checkout time.
    """
    return await service.check_out(db, current_user.id)


@router.get("/me", response_model=list[AttendanceOut])
async def get_my_attendance_history(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Employee: View History.
    Returns the last 30 days of attendance logs.
    """
    return await service.get_my_attendance(db, current_user.id)


# ============= Admin Endpoints =============


@router.get("/employees/{employee_id}", response_model=list[AttendanceWithHours])
async def get_employee_attendance(
    employee_id: uuid.UUID,
    start_date: date = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: date = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(admin_required),
):
    """
    Admin: View specific employee's attendance with working hours.
    Optionally filter by date range.
    """
    from datetime import timedelta

    # Default to last 30 days if no dates provided
    if not end_date:
        end_date = date.today()
    if not start_date:
        start_date = end_date - timedelta(days=30)

    records = await service.get_employee_attendance_by_date_range(
        db, employee_id, start_date, end_date
    )

    # Add working hours to each record
    result = []
    for record in records:
        record_dict = AttendanceWithHours.model_validate(record).model_dump()
        record_dict["working_hours"] = service.calculate_working_hours(record)
        result.append(record_dict)

    return result


@router.get("/daily/{work_date}", response_model=list[AttendanceOut])
async def get_all_employees_attendance_by_date(
    work_date: date,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(admin_required),
):
    """
    Admin: View all employees' attendance for a specific date.
    """
    return await service.get_all_employees_attendance(db, work_date)


@router.put("/{attendance_id}", response_model=AttendanceOut)
async def update_attendance_manually(
    attendance_id: uuid.UUID,
    data: ManualAttendanceUpdate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(admin_required),
):
    """
    Admin: Manually update an attendance record.
    Allows correction of check-in/check-out times and status.
    """
    return await service.manual_update_attendance(
        db, attendance_id, data.check_in, data.check_out, data.status.value
    )
