from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    sku: str
    description: str | None = None
    price: Decimal
    category_id: int
class ProductCreate(ProductBase):
    pass
class ProductUpdate(BaseModel):
    name:str | None = None
    sku:str | None = None
    description: str | None = None
    price: Decimal | None = None
    category_id: int | None = None
class ProductResponse(ProductBase):
    id:int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)