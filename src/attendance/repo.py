from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date
import uuid
from src.attendance.models import AttendanceRecord
from src.employees.models import Employee


class AttendanceRepository:
    async def get_employee_by_user_id(
        self, db: AsyncSession, user_id: str
    ) -> Employee | None:
        """Finds the Employee profile linked to the User Account."""
        result = await db.execute(select(Employee).where(Employee.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_today_record(
        self, db: AsyncSession, employee_id: uuid.UUID
    ) -> AttendanceRecord | None:
        """Checks if there is already a row for this employee today."""
        query = select(AttendanceRecord).where(
            and_(
                AttendanceRecord.employee_id == employee_id,
                AttendanceRecord.work_date == date.today(),
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_history(
        self, db: AsyncSession, employee_id: uuid.UUID, limit: int = 30
    ):
        """Fetches recent attendance history."""
        query = (
            select(AttendanceRecord)
            .where(AttendanceRecord.employee_id == employee_id)
            .order_by(AttendanceRecord.work_date.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def create(
        self, db: AsyncSession, record: AttendanceRecord
    ) -> AttendanceRecord:
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    async def update(
        self, db: AsyncSession, record: AttendanceRecord
    ) -> AttendanceRecord:
        db.add(record)  # Ensure it's in the session
        await db.commit()
        await db.refresh(record)
        return record

    async def get_by_id(
        self, db: AsyncSession, attendance_id: uuid.UUID
    ) -> AttendanceRecord | None:
        """Get attendance record by ID."""
        query = select(AttendanceRecord).where(AttendanceRecord.id == attendance_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_attendance_by_date_range(
        self, db: AsyncSession, employee_id: uuid.UUID, start_date: date, end_date: date
    ):
        """Get attendance records for an employee within a date range."""
        query = (
            select(AttendanceRecord)
            .where(
                and_(
                    AttendanceRecord.employee_id == employee_id,
                    AttendanceRecord.work_date >= start_date,
                    AttendanceRecord.work_date <= end_date,
                )
            )
            .order_by(AttendanceRecord.work_date.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_all_employees_attendance(
        self, db: AsyncSession, work_date: date
    ):
        """Get all employees' attendance for a specific date."""
        query = (
            select(AttendanceRecord)
            .where(AttendanceRecord.work_date == work_date)
            .order_by(AttendanceRecord.employee_id)
        )
        result = await db.execute(query)
        return result.scalars().all()

