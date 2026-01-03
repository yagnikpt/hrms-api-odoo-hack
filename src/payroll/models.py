from sqlalchemy import Integer, Numeric, Date, ForeignKey, String
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
    basic_salary: Mapped[float] = mapped_column(Numeric(10, 2)) 
    deductions: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    net_pay: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String, default="DRAFT")  # DRAFT, PAID, CANCELLED
    payment_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    employee: Mapped["Employee"] = relationship("Employee")
