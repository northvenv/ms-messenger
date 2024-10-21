from uuid import UUID

from sqlalchemy import Uuid, String
from sqlalchemy.orm import Mapped, mapped_column

from access_service.infrastructure.persistence.models.base import Base


class DBUser(Base):
    __tablename__ = 'users'

    user_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(300), nullable=False)