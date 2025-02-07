from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from models import CartItem, User, Product
from schemas import CartItemCreate, CartItemResponse, CartResponse, ProductResponse
from dependencies import get_db
from utils import get_current_user

router = APIRouter(tags=["cart"])

@router.post("/cart/", response_model=CartItemResponse)
async def add_to_cart(
    cart_item: CartItemCreate, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user.id, 
        CartItem.product_id == product.id
    ).first()

    if existing_item:
        existing_item.quantity += cart_item.quantity
    else:
        existing_item = CartItem(user_id=user.id, product_id=product.id, quantity=cart_item.quantity)
        db.add(existing_item)

    db.commit()
    db.refresh(existing_item)

    return CartItemResponse(
        id=existing_item.id,
        product=ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category_id=product.category_id
        ),
        quantity=existing_item.quantity
    )

@router.get("/cart/", response_model=CartResponse)
async def view_cart(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    
    cart_items_serialized = [
        CartItemResponse(
            id=item.id,
            product=ProductResponse(
                id=item.product.id,
                name=item.product.name,
                description=item.product.description,
                price=item.product.price,
                stock=item.product.stock,
                category_id=item.product.category_id
            ),
            quantity=item.quantity
        ) for item in cart_items
    ]
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return {"cart_items": cart_items_serialized, "total_price": total}

@router.put("/cart/{cart_item_id}", response_model=CartItemResponse)
async def update_cart_item(
    cart_item_id: int, 
    cart_item: CartItemCreate, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db_item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.user_id == user.id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    product = db.query(Product).filter(Product.id == db_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if cart_item.quantity > product.stock:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    if cart_item.quantity <= 0:
        db.delete(db_item)
        db.commit()
        return Response(status_code=204)

    db_item.quantity = cart_item.quantity
    db.commit()
    db.refresh(db_item)

    return CartItemResponse(
        id=db_item.id,
        product=ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category_id=product.category_id
        ),
        quantity=db_item.quantity
    )
