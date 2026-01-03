from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(20))
    company: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[Date] = mapped_column(Date)
    updated_at: Mapped[Date] = mapped_column(Date)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
