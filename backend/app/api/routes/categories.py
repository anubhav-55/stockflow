from fastapi import APIRouter, Depends, status , HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from app.db.dependencies import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)
# post 
@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    db_category = Category(
        name=category.name,
        description=category.description,
    )
    db.add(db_category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A category with this name already exists.",
        )
    db.refresh(db_category)

    return db_category
# get 
@router.get(
    "/",
    response_model=list[CategoryResponse],
    )
def list_categories(
    db: Session = Depends(get_db),
):
    return db.query(Category).all()
