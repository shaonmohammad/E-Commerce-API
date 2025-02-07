from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Order, OrderItem, CartItem, User, Product
from schemas import OrderResponse
from dependencies import get_db
from utils import get_current_user

router = APIRouter(tags=["orders"])

@router.post("/checkout/", response_model=OrderResponse)
async def checkout(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user).first()
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    total = 0.0
    order = Order(user_id=user.id, total_amount=0.0)
    db.add(order)
    db.flush()
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product.stock < item.quantity:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        product.stock -= item.quantity
        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, unit_price=product.price)
        db.add(order_item)
        total += product.price * item.quantity
    order.total_amount = total
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    return order