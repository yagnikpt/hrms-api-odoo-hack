from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID


class PayrollBase(BaseModel):
    pay_period_start: date
    pay_period_end: date
    basic_salary: float
    deductions: float = 0.0


class PayrollCreate(PayrollBase):
    employee_id: UUID


class Payroll(PayrollBase):
    id: int
    net_pay: float
    employee_id: UUID

    model_config = ConfigDict(from_attributes=True)
