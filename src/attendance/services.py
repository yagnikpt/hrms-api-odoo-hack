from datetime import datetime, date, timezone
from fastapi import HTTPException, status
from src.attendance.models import AttendanceRecord
from src.attendance.repo import AttendanceRepository
from src.attendance.schemas import AttendanceStatus

repo = AttendanceRepository()


class AttendanceService:
    async def _get_employee_or_fail(self, db, user_id: str):
        employee = await repo.get_employee_by_user_id(db, user_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee profile not found. Please contact HR.",
            )
        return employee

    async def check_in(self, db, user_id: str):
        employee = await self._get_employee_or_fail(db, user_id)

        # 1. Prevent double check-in
        existing = await repo.get_today_record(db, employee.id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already checked in today.",
            )

        # 2. Create Record with timezone-aware datetime
        new_record = AttendanceRecord(
            employee_id=employee.id,
            work_date=date.today(),
            check_in=datetime.now(timezone.utc),
            status=AttendanceStatus.PRESENT.value,
        )
        return await repo.create(db, new_record)

    async def check_out(self, db, user_id: str):
        employee = await self._get_employee_or_fail(db, user_id)

        # 1. Ensure check-in exists
        record = await repo.get_today_record(db, employee.id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No check-in record found for today.",
            )

        # 2. Prevent double check-out
        if record.check_out is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already checked out today.",
            )

        # 3. Update Record with timezone-aware datetime
        record.check_out = datetime.now(timezone.utc)

        # Half-day logic: if worked < 4 hours
        duration = record.check_out - record.check_in
        if duration.total_seconds() < 14400:  # 4 hours = 14400 seconds
            record.status = AttendanceStatus.HALF_DAY.value

        return await repo.update(db, record)

    async def get_my_attendance(self, db, user_id: str):
        employee = await self._get_employee_or_fail(db, user_id)
        return await repo.get_history(db, employee.id)

    def calculate_working_hours(self, record: AttendanceRecord) -> float:
        """Calculate working hours for an attendance record."""
        if not record.check_in or not record.check_out:
            return 0.0
        duration = record.check_out - record.check_in
        return round(duration.total_seconds() / 3600, 2)  # Convert to hours

    async def get_employee_attendance_by_date_range(
        self, db, employee_id: str, start_date: date, end_date: date
    ):
        """Get employee attendance for a specific date range (for admin)."""
        return await repo.get_attendance_by_date_range(
            db, employee_id, start_date, end_date
        )

    async def get_all_employees_attendance(self, db, work_date: date):
        """Get all employees attendance for a specific date (for admin)."""
        return await repo.get_all_employees_attendance(db, work_date)

    async def manual_update_attendance(
        self, db, attendance_id: str, check_in: datetime, check_out: datetime, status: str
    ):
        """Manually update attendance record (for admin)."""
        record = await repo.get_by_id(db, attendance_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance record not found.",
            )
        
        record.check_in = check_in
        record.check_out = check_out
        record.status = status
        
        return await repo.update(db, record)
