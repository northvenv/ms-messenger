from sqlalchemy import types
from uuid import UUID, uuid4
import asyncpg

from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from access_service.infrastructure.persistence.models.base import Base




class DBUser(Base):
    __tablename__ = 'users'

    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    phone_number: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(300), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean)