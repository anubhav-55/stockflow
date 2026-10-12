from pydantic import BaseModel

from app.models.stock_movement import  MovementType

class StockOperation(BaseModel):
    movement_type: MovementType
    quantity: int
    reason: str
