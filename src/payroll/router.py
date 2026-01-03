from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, models, schemas
from src.db.session import get_db

router = APIRouter()

@router.post("/employees/", response_model=schemas.Employee)
async def create_employee(employee: schemas.EmployeeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_employee(db=db, employee=employee)

@router.get("/employees/", response_model=List[schemas.Employee])
async def read_employees(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    employees = await crud.get_employees(db, skip=skip, limit=limit)
    return employees

@router.post("/payrolls/", response_model=schemas.Payroll)
async def create_payroll(payroll: schemas.PayrollCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_payroll(db=db, payroll=payroll)

@router.get("/payrolls/", response_model=List[schemas.Payroll])
async def read_payrolls(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    payrolls = await crud.get_payrolls(db, skip=skip, limit=limit)
    return payrolls
