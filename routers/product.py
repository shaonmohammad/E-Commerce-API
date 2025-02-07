from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Product, Category
from schemas import ProductCreate, ProductResponse
from dependencies import get_db
from utils import get_current_user

router = APIRouter(tags=["products"])

@router.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: Optional[int] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if in_stock is not None:
        query = query.filter(Product.stock > 0) if in_stock else query.filter(Product.stock <= 0)
    if limit is not None:
        query = query.limit(limit).offset(skip)
    return query.all()

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product