from fastapi import APIRouter

from src.api.v1 import users, employees, payroll, attendance
from src.auth import router as auth


api_v1_router = APIRouter()

api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(employees.router)
api_v1_router.include_router(payroll.router)
api_v1_router.include_router(attendance.router)
