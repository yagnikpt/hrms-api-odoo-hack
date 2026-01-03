from fastapi import APIRouter

from src.api.v1 import (
    users,
    employees,
)

api_v1_router = APIRouter()

api_v1_router.include_router(users.router)
api_v1_router.include_router(employees.router)
