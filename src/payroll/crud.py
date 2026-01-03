from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def get_employee(db: AsyncSession, employee_id: int):
    result = await db.execute(select(models.Employee).filter(models.Employee.id == employee_id))
    return result.scalars().first()

async def get_employees(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Employee).offset(skip).limit(limit))
    return result.scalars().all()

async def create_employee(db: AsyncSession, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

async def get_payrolls(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Payroll).offset(skip).limit(limit))
    return result.scalars().all()

async def create_payroll(db: AsyncSession, payroll: schemas.PayrollCreate):
    net_pay = payroll.basic_salary - payroll.deductions
    db_payroll = models.Payroll(**payroll.dict(), net_pay=net_pay)
    db.add(db_payroll)
    await db.commit()
    await db.refresh(db_payroll)
    return db_payroll
