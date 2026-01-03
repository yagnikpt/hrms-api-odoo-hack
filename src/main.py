from fastapi import FastAPI
from src.payroll.router import router as payroll_router
from src.api.v1.router import api_v1_router

app = FastAPI(title="Dayflow API")

app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(payroll_router, prefix="/api/v1", tags=["payroll"])
