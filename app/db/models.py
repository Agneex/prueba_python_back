from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    full_name: Mapped[str | None] = mapped_column(String(120))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)

    functions: Mapped[list["ImplicitFunction"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class ImplicitFunction(TimestampMixin, Base):
    __tablename__ = "implicit_functions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    expression: Mapped[str] = mapped_column(Text)
    domain: Mapped[list[list[float]]] = mapped_column(JSONB)
    resolution: Mapped[int] = mapped_column(Integer, default=64)
    version: Mapped[int] = mapped_column(Integer, default=1)

    owner: Mapped[User] = relationship(back_populates="functions")
