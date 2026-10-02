from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate , ProductResponse , ProductUpdate
from app.models.category import Category

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)
# post
@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,

)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    category = db.get(Category,product.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )
    db_product = Product(
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
    )
    db.add(db_product)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()

        if "products_sku_key" in str(exc.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A product with this SKU alreday exists.",
            )
        raise
    db.refresh(db_product)

    return db_product
# list all products 
@router.get(
    "/",
    response_model=list[ProductResponse],
)
def list_products(
    db: Session = Depends(get_db),
):
    return db.query(Product).all()
@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product
# updat_product
@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    db_product = db.get(Product, product_id)

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    if product.name is not None:
        db_product.name = product.name

    if product.sku is not None:
        db_product.sku = product.sku

    if product.description is not None:
        db_product.description = product.description

    if product.price is not None:
        db_product.price = product.price

    if product.category_id is not None:
        category = db.get(Category, product.category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        db_product.category_id = product.category_id

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()

        if "products_sku_key" in str(exc.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A product with this SKU already exists.",
            )

        raise

    db.refresh(db_product)

    return db_product