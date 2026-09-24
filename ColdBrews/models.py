from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Brew(Base):
    __tablename__ = "brews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    bean_origin: Mapped[str] = mapped_column(String(100))
    steep_hours: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class BrewCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    bean_origin: str = Field(min_length=1, max_length=100)
    steep_hours: float = Field(gt=0, le=48)
    price: float = Field(ge=0)


class BrewUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    bean_origin: str | None = Field(default=None, min_length=1, max_length=100)
    steep_hours: float | None = Field(default=None, gt=0, le=48)
    price: float | None = Field(default=None, ge=0)


class BrewRead(BrewCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
