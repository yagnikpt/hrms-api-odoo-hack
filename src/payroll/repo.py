from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.payroll import models, schemas


async def get_payrolls(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Payroll).offset(skip).limit(limit))
    return result.scalars().all()


async def create_payroll(db: AsyncSession, payroll: schemas.PayrollCreate):
    net_pay = payroll.basic_salary - payroll.deductions
    db_payroll = models.Payroll(**payroll.model_dump(), net_pay=net_pay)
    db.add(db_payroll)
    await db.commit()
    await db.refresh(db_payroll)
    return db_payroll
