from sqlalchemy import Integer, String, Boolean, ForeignKey, Date, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from datetime import date, datetime
from src.db.base import Base


class LeaveType(Base):
    __tablename__ = "leave_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    is_paid: Mapped[bool] = mapped_column(Boolean)


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    employee_id: Mapped[UUID] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE"))
    leave_type_id: Mapped[int] = mapped_column(ForeignKey("leave_types.id"))
    leave_type: Mapped["LeaveType"] = relationship("LeaveType")
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    remarks: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20))
    reviewed_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    review_comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now)
    reviewed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
