from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.core.deps import get_db, admin_required, get_current_user
from src.users.models import User
from src.payroll import schemas
from src.payroll.services import PayrollService

router = APIRouter(prefix="/payroll", tags=["Payroll"])
service = PayrollService()


@router.post("/", response_model=schemas.PayrollOut)
async def create_payroll(
    payroll: schemas.PayrollCreate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(admin_required),
):
    """
    Admin: Generate a payroll record for an employee.
    """
    return await service.create_payroll_record(db, payroll)


@router.get("/me", response_model=List[schemas.PayrollOut])
async def get_my_payrolls(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Employee: View my own payslip history.
    """
    return await service.get_my_payrolls(db, current_user.id)


@router.get("/", response_model=List[schemas.PayrollOut])
async def get_all_payrolls(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(admin_required),
):
    """
    Admin: View all payroll records.
    """
    return await service.get_all_payrolls(db, skip, limit)


@router.put("/{payroll_id}/status", response_model=schemas.PayrollOut)
async def update_payroll_status(
    payroll_id: int = Path(..., title="The ID of the payroll record"),
    status_update: schemas.PayrollUpdateStatus = ...,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(admin_required),
):
    """
    Admin: Update status (e.g. mark as PAID).
    """
    return await service.update_status(db, payroll_id, status_update.status)
