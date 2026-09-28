from datetime import UTC , datetime
from enum import Enum

from sqlalchemy import DateTime , ForeignKey , String
from sqlalchemy.orm import Mapped , mapped_column , relationship

from app.db.base import Base

class MovementType(str,Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"
class StockMovement(Base):
    __tablename__ = "stock_movements"
    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )
    # Always store the moved quantity as a positive number.
    # MovementType determines whether stock increases or decreases.
    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )
    movement_type: Mapped[MovementType] = mapped_column(
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    product: Mapped["Product"] = relationship(
        back_populates="stock_movements",
    )