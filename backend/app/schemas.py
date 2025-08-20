from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WorkBase(BaseModel):
    name: str
    unit: str
    base_rate: float = Field(ge=0)
    min_rate: Optional[float] = Field(default=None, ge=0)
    max_rate: Optional[float] = Field(default=None, ge=0)
    category_id: Optional[int] = None


class WorkCreate(WorkBase):
    pass


class WorkOut(WorkBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MaterialBase(BaseModel):
    name: str
    unit: str
    price: float = Field(ge=0)
    vendor: Optional[str] = None
    sku: Optional[str] = None


class MaterialCreate(MaterialBase):
    pass


class MaterialOut(MaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    client_name: Optional[str] = None
    currency: str = "EUR"
    notes: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EstimateItemBase(BaseModel):
    work_id: Optional[int] = None
    material_id: Optional[int] = None
    quantity: float = Field(ge=0)
    unit: str
    unit_price: float = Field(ge=0)
    title_override: Optional[str] = None


class EstimateItemCreate(EstimateItemBase):
    pass


class EstimateItemOut(EstimateItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EstimateBase(BaseModel):
    project_id: int
    name: str
    discount_percent: float = 0
    surcharge_percent: float = 0


class EstimateCreate(EstimateBase):
    items: list[EstimateItemCreate] = []


class EstimateOut(EstimateBase):
    id: int
    items: list[EstimateItemOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Totals(BaseModel):
    subtotal: float
    discount: float
    surcharge: float
    total: float

