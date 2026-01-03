from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.employees.models import Employee


class EmployeeRepository:
    async def get_by_id(self, db: AsyncSession, employee_id) -> Employee | None:
        result = await db.execute(select(Employee).where(Employee.id == employee_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, db: AsyncSession, user_id) -> Employee | None:
        result = await db.execute(select(Employee).where(Employee.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, employee: Employee) -> Employee:
        db.add(employee)
        await db.commit()
        await db.refresh(employee)
        return employee
