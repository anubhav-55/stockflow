from datetime import UTC,datetime

from sqlalchemy import DateTime , String , Text
from sqlalchemy.orm import Mapped, mapped_column , relationship

from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    description: Mapped[str | None] = mapped_column(Text,nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(UTC),
        nullable=False,
    )
    # A category can contain multiple products.
    products:Mapped[list["Product"]] = relationship(
        back_populates="category",
    )