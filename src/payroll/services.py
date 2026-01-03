from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from datetime import date
from uuid import UUID
from fastapi import HTTPException, status

from src.payroll.models import Payroll
from src.payroll.schemas import PayrollCreate, PayrollStatus
from src.employees.models import Employee


class PayrollService:
    async def create_payroll_record(self, db: AsyncSession, data: PayrollCreate) -> Payroll:
        # 1. Check for existing payroll in this date range
        existing_query = select(Payroll).where(
            and_(
                Payroll.employee_id == data.employee_id,
                Payroll.pay_period_start == data.pay_period_start,
                Payroll.pay_period_end == data.pay_period_end
            )
        )
        existing = await db.execute(existing_query)
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=400, 
                detail="Payroll already exists for this period."
            )
        # Get employee to check base salary
        result = await db.execute(select(Employee).where(Employee.id == data.employee_id))
        employee = result.scalar_one_or_none()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        basic_salary = employee.base_salary
        net_pay = basic_salary - data.deductions
        
        # Check if payroll already exists for this period? 
        # For now assume multiple slips for same period allowed or handled by admin care.

        db_payroll = Payroll(
            employee_id=data.employee_id,
            pay_period_start=data.pay_period_start,
            pay_period_end=data.pay_period_end,
            basic_salary=basic_salary,
            deductions=data.deductions,
            net_pay=net_pay,
            status=PayrollStatus.DRAFT.value,
        )
        db.add(db_payroll)
        await db.commit()
        await db.refresh(db_payroll)
        return db_payroll

    async def get_my_payrolls(self, db: AsyncSession, user_id: str) -> list[Payroll]:
        # Need to join Employee to filter by user_id
        query = (
            select(Payroll)
            .join(Employee)
            .where(Employee.user_id == user_id)
            .order_by(desc(Payroll.pay_period_start))
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_all_payrolls(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Payroll]:
        query = select(Payroll).order_by(desc(Payroll.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def update_status(self, db: AsyncSession, payroll_id: int, new_status: PayrollStatus) -> Payroll:
        result = await db.execute(select(Payroll).where(Payroll.id == payroll_id))
        payroll = result.scalar_one_or_none()
        if not payroll:
            raise HTTPException(status_code=404, detail="Payroll record not found")

        if payroll.status == PayrollStatus.PAID.value and new_status != PayrollStatus.PAID:
             # Prevent Un-paying? Or allow corrections. Let's allow for now but maybe warn.
             pass

        payroll.status = new_status.value
        if new_status == PayrollStatus.PAID:
            payroll.payment_date = date.today()
        elif new_status == PayrollStatus.DRAFT:
            payroll.payment_date = None
        
        await db.commit()
        await db.refresh(payroll)
        return payroll
