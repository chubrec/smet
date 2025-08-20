from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class WorkCategory(Base, TimestampMixin):
    __tablename__ = "work_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    works: Mapped[list["Work"]] = relationship("Work", back_populates="category")


class Work(Base, TimestampMixin):
    __tablename__ = "works"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)  # m2, pcs, lm
    base_rate: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    min_rate: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    max_rate: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("work_categories.id"))

    category: Mapped[Optional[WorkCategory]] = relationship("WorkCategory", back_populates="works")


class Material(Base, TimestampMixin):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    vendor: Mapped[Optional[str]] = mapped_column(String(100))  # e.g., Leroy Merlin
    sku: Mapped[Optional[str]] = mapped_column(String(100))


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    client_name: Mapped[Optional[str]] = mapped_column(String(150))
    currency: Mapped[str] = mapped_column(String(3), default="EUR", nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    estimates: Mapped[list["Estimate"]] = relationship("Estimate", back_populates="project")


class Estimate(Base, TimestampMixin):
    __tablename__ = "estimates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    discount_percent: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    surcharge_percent: Mapped[float] = mapped_column(Numeric(5, 2), default=0)

    project: Mapped[Project] = relationship("Project", back_populates="estimates")
    items: Mapped[list["EstimateItem"]] = relationship("EstimateItem", back_populates="estimate", cascade="all, delete-orphan")


class EstimateItem(Base, TimestampMixin):
    __tablename__ = "estimate_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estimate_id: Mapped[int] = mapped_column(ForeignKey("estimates.id"), nullable=False)
    work_id: Mapped[Optional[int]] = mapped_column(ForeignKey("works.id"))
    material_id: Mapped[Optional[int]] = mapped_column(ForeignKey("materials.id"))
    quantity: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    title_override: Mapped[Optional[str]] = mapped_column(String(200))

    estimate: Mapped[Estimate] = relationship("Estimate", back_populates="items")
    work: Mapped[Optional[Work]] = relationship("Work")
    material: Mapped[Optional[Material]] = relationship("Material")

