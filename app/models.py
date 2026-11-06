from datetime import date
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="Applied")
    applied_date: Mapped[date] = mapped_column(default=date.today)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)