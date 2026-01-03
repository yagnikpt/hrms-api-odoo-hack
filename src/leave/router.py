from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
import uuid
from datetime import datetime

from src.core.deps import get_db, get_current_user
from src.users.models import User
from src.employees.models import Employee
from src.leave.models import LeaveType, LeaveRequest
from src.leave import schemas

router = APIRouter()

# --- Leave Types ---

@router.post("/leave/types", response_model=schemas.LeaveTypeOut, status_code=status.HTTP_201_CREATED)
async def create_leave_type(
    leave_type: schemas.LeaveTypeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: Add admin check if needed
    result = await db.execute(select(LeaveType).where(LeaveType.name == leave_type.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Leave type already exists")
    
    new_type = LeaveType(**leave_type.model_dump())
    db.add(new_type)
    await db.commit()
    await db.refresh(new_type)
    return new_type

@router.get("/leave/types", response_model=List[schemas.LeaveTypeOut])
async def get_leave_types(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(LeaveType))
    return result.scalars().all()

# --- Leave Requests ---

@router.post("/leave/requests", response_model=schemas.LeaveRequestOut, status_code=status.HTTP_201_CREATED)
async def create_leave_request(
    request: schemas.LeaveRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify employee profile exists
    result = await db.execute(select(Employee).where(Employee.user_id == current_user.id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=400, detail="Employee profile not found")

    # Verify leave type exists
    leave_type = await db.get(LeaveType, request.leave_type_id)
    if not leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")

    new_request = LeaveRequest(
        id=uuid.uuid4(),
        employee_id=employee.id,
        leave_type_id=request.leave_type_id,
        start_date=request.start_date,
        end_date=request.end_date,
        remarks=request.remarks,
        status="PENDING"
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    
    # Manually attach leave_type for the response model
    new_request.leave_type = leave_type
    
    return new_request

@router.get("/leave/requests", response_model=List[schemas.LeaveRequestOut])
async def get_leave_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(LeaveRequest).options(selectinload(LeaveRequest.leave_type))
    
    if current_user.role not in ["ADMIN", "HR"]:
        result = await db.execute(select(Employee).where(Employee.user_id == current_user.id))
        employee = result.scalar_one_or_none()
        if not employee:
            return []
        stmt = stmt.where(LeaveRequest.employee_id == employee.id)
    
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/leave/requests/{request_id}", response_model=schemas.LeaveRequestOut)
async def get_leave_request(
    request_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(LeaveRequest).where(LeaveRequest.id == request_id).options(selectinload(LeaveRequest.leave_type))
    result = await db.execute(stmt)
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    # Check permission
    if current_user.role not in ["ADMIN", "HR"]:
        emp_result = await db.execute(select(Employee).where(Employee.user_id == current_user.id))
        employee = emp_result.scalar_one_or_none()
        if not employee or request.employee_id != employee.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this request")

    return request

@router.patch("/leave/requests/{request_id}", response_model=schemas.LeaveRequestOut)
async def update_leave_status(
    request_id: uuid.UUID,
    update_data: schemas.LeaveRequestUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["ADMIN", "HR"]:
        raise HTTPException(status_code=403, detail="Only admins/HR can update leave status")

    stmt = select(LeaveRequest).where(LeaveRequest.id == request_id).options(selectinload(LeaveRequest.leave_type))
    result = await db.execute(stmt)
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    request.status = update_data.status
    request.review_comment = update_data.review_comment
    request.reviewed_by = current_user.id
    request.reviewed_at = datetime.now()
    
    await db.commit()
    await db.refresh(request)
    # relationship should still be loaded as it's the same object, but if needed we could reload or assume it persists.
    # Since we fetched it with selectinload, it should be fine.
    
    return request
