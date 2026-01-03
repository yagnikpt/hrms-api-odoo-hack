from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID
from enum import Enum


class PayrollStatus(str, Enum):
    DRAFT = "DRAFT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class PayrollBase(BaseModel):
    pay_period_start: date
    pay_period_end: date
    basic_salary: float
    deductions: float = 0.0


from pydantic import field_validator

class PayrollCreate(BaseModel):
    employee_id: UUID
    pay_period_start: date
    pay_period_end: date
    deductions: float = 0.0

    @field_validator('pay_period_end')
    def check_dates(cls, v, values):
        if 'pay_period_start' in values.data and v < values.data['pay_period_start']:
            raise ValueError('End date must be after start date')
        return v


class PayrollUpdateStatus(BaseModel):
    status: PayrollStatus


class PayrollOut(PayrollBase):
    id: int
    employee_id: UUID
    net_pay: float
    status: str
    payment_date: date | None
    created_at: date
    
    # We might want employee details here too? 
    # For now let's keep it simple or use a separate schema if needed.

    model_config = ConfigDict(from_attributes=True)
