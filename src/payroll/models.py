from sqlalchemy import Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base
from src.employees.models import Employee
from uuid import UUID
from datetime import date


class Payroll(Base):
    __tablename__ = "payrolls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[UUID] = mapped_column(ForeignKey("employees.id"))
    pay_period_start: Mapped[date] = mapped_column(Date)
    pay_period_end: Mapped[date] = mapped_column(Date)
    basic_salary: Mapped[float] = mapped_column(Float)
    deductions: Mapped[float] = mapped_column(Float, default=0.0)
    net_pay: Mapped[float] = mapped_column(Float)

    employee: Mapped["Employee"] = relationship("Employee")
