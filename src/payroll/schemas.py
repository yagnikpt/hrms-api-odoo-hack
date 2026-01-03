from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class PayrollBase(BaseModel):
    pay_period_start: date
    pay_period_end: date
    basic_salary: float
    deductions: float = 0.0

class PayrollCreate(PayrollBase):
    employee_id: int

class Payroll(PayrollBase):
    id: int
    net_pay: float
    employee_id: int

    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    name: str
    email: str
    position: str
    department: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    payrolls: List[Payroll] = []

    class Config:
        orm_mode = True
