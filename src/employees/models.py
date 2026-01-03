from sqlalchemy import String, Date, Text, DateTime, Time, func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from datetime import datetime, date, time
from src.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.users.models import User


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), unique=True, index=True
    )
    user: Mapped["User"] = relationship("User")
    job_title: Mapped[str] = mapped_column(String(100))
    department: Mapped[str] = mapped_column(String(100))
    base_salary: Mapped[float] = mapped_column(Float, default=0.0)
    address: Mapped[str | None] = mapped_column(Text)
    profile_picture_url: Mapped[str | None] = mapped_column(Text)
    date_of_joining: Mapped[date] = mapped_column(Date)
    check_in_time: Mapped[time | None] = mapped_column(Time)
    check_out_time: Mapped[time | None] = mapped_column(Time)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Employee {self.id}>"
