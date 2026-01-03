from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.employees.models import Employee


class EmployeeRepository:
    async def get_by_id(self, db: AsyncSession, employee_id) -> Employee | None:
        result = await db.execute(
            select(Employee)
            .options(selectinload(Employee.user))
            .where(Employee.id == employee_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, db: AsyncSession, user_id) -> Employee | None:
        result = await db.execute(select(Employee).where(Employee.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, employee: Employee) -> Employee:
        db.add(employee)
        await db.commit()
        await db.refresh(employee)
        # Ensure user relationship is loaded
        # We can either explicit refresh or just let next query handle it,
        # but for API response we need it.
        # Since we have the user object in service, we could attach it,
        # but cleaner to reload from DB if needed.
        # Actually simplest is to execute a select with load.
        # But refresh with list might work: await db.refresh(employee, ["user"])
        # However, "user" relationship lookup requires a query.
        return await self.get_by_id(db, employee.id)
