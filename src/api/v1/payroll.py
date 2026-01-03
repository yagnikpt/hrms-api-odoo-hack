from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.payroll import repo, schemas
from src.core.deps import get_db

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.post("/", response_model=schemas.Payroll)
async def create_payroll(
    payroll: schemas.PayrollCreate, db: AsyncSession = Depends(get_db)
):
    return await repo.create_payroll(db=db, payroll=payroll)


@router.get("/", response_model=List[schemas.Payroll])
async def read_payrolls(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    payrolls = await repo.get_payrolls(db, skip=skip, limit=limit)
    return payrolls
