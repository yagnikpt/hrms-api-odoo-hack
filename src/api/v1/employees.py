from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.employees.schemas import EmployeeCreate, EmployeeOut, EmployeeUpdate
from src.employees.services import EmployeeService
from src.core.deps import (
    get_db,
    admin_required,
)
from src.users.models import User
from src.employees.exceptions import EmployeeAlreadyExistsError

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

service = EmployeeService()


@router.post(
    "/",
    response_model=EmployeeOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    payload: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(admin_required),
):
    try:
        return await service.create_employee(db, payload)
    except EmployeeAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this user_id already exists",
        )


@router.get("/{employee_id}", response_model=EmployeeOut)
async def get_employee(
    employee_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    employee = await service.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return employee


@router.patch("/{employee_id}", response_model=EmployeeOut)
async def update_employee(
    employee_id: UUID,
    payload: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(admin_required),
):
    employee = await service.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return await service.update_profile(db, employee, payload)
