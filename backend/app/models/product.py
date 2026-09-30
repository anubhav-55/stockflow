from datetime import UTC, datetime

from sqlalchemy import DateTime,ForeignKey, Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.db.base import Base
from app.models.category import Category

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    # SKU uniquely identifies a product for inventory operations.
    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    price: Mapped[float] = mapped_column(
        Numeric(10,2),
        nullable=False,
    )
    category_id:Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda:datetime.now(UTC),
        nullable=False,
    )
    #Many products can belong to one category.
    category: Mapped["Category"] = relationship(
        back_populates="products",
    )
    # One product has one current stock record.
    stock: Mapped["Stock"] = relationship(
    back_populates="product",
    uselist=False,
)
# keeps the complete inventory movement history for this product
    stock_movements: Mapped[list["StockMovement"]] = relationship(
    back_populates="product",
)