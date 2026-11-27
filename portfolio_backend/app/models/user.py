from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

#my sql table structure
class User(Base):
  __tablename__ = "users"
  id:Mapped[int] = mapped_column(
    Integer,
    primary_key=True,
    index=True
  )
  username:Mapped[str] = mapped_column(
    String(255),
    unique=True,
    nullable=False,
    index=True
  )
  email:Mapped[str] = mapped_column(
    String(255),
    unique=True,
    nullable=False,
    index=True
  )