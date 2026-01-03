from fastapi import FastAPI
from src.payroll.router import router as payroll_router
from src.attendance.router import router as attendance_router
from src.leave.router import router as leave_router
from src.api.v1.router import api_v1_router

app = FastAPI(title="Dayflow API")

app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(payroll_router, prefix="/api/v1", tags=["payroll"])
app.include_router(attendance_router, prefix="/api/v1", tags=["attendance"])
app.include_router(leave_router, prefix="/api/v1", tags=["leave"])
