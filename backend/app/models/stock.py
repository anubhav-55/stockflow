from sqlalchemy import DateTime , ForeignKey
from sqlalchemy.orm import Mapped , mapped_column, relationship
from app.db.base import Base
from datetime import UTC , datetime
class Stock(Base):
    __tablename__ = "stock"
    id: Mapped[int] = mapped_column(primary_key=True)

    # one product has exactly one current stock record.
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        unique=True,
        nullable=False,
    )
    # current quantity available in inventory.
    quantity: Mapped[int] = mapped_column(
        nullable = False,
        default = 0,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
    product: Mapped["Product"] = relationship(
        back_populates="stock",
    )