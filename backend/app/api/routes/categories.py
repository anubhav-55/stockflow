from fastapi import APIRouter, Depends, status , HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from app.db.dependencies import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

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
    except IntegrityError as exc:
        db.rollback()
        if "categories_name_key" in str(exc.orig):
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
# get category by id

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = db.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return category
# put category by id
@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db:Session = Depends(get_db),
):
    db_category = db.get(Category, category_id)

    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )
    if category.name is not None:
        db_category.name = category.name

    if category.description is not None:
        db_category.description  = category.description
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()

        if "categories_name_key" in str(exc.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A category with this name already exists.",
            )
        raise
    db.refresh(db_category)
    return db_category
# delete by id
@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id:int,
    db: Session = Depends(get_db),
):
    db_category = db.get(Category,category_id)

    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )
    if db_category.products:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a category that has products.",
        )
    db.delete(db_category)
    db.commit()