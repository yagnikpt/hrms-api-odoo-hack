from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import UserCreate, UserOut
from src.users.services import UserService
from src.core.deps import (
    get_db,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

service = UserService()


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await service.create_user(db, payload)
