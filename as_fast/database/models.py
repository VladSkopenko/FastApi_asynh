from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), index=True)
    second_name: Mapped[str] = mapped_column(String(50), index=True)
    email_add: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    phone_num: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    birth_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
