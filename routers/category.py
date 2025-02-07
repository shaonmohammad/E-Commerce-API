from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Category
from schemas import CategoryCreate, CategoryResponse
from dependencies import get_db
from typing import List
from utils import get_current_user
router = APIRouter(tags=["product's category"])

@router.post("/categories/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/categories/", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}", response_model=CategoryResponse)
async def delete_category(category_id: int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category