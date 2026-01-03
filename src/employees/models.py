from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from src.db.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(unique=True, index=True)

    employee_code: Mapped[str] = mapped_column(String(50), unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    job_title: Mapped[str] = mapped_column(String(100))
    department: Mapped[str] = mapped_column(String(100))

    phone: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(Text)
    profile_picture_url: Mapped[str | None]

    date_of_joining: Mapped[Date]

    def __repr__(self) -> str:
        return f"<Employee {self.employee_code}>"
