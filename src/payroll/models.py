from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    position = Column(String)
    department = Column(String)

    payrolls = relationship("Payroll", back_populates="employee")

class Payroll(Base):
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    pay_period_start = Column(Date)
    pay_period_end = Column(Date)
    basic_salary = Column(Float)
    deductions = Column(Float, default=0.0)
    net_pay = Column(Float)

    employee = relationship("Employee", back_populates="payrolls")
