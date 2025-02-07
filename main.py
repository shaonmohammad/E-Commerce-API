from fastapi import FastAPI
from models import Base, engine
from routers import auth, category, product, cart, order

app = FastAPI(title="E-commerce API")

# Include routers
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)

# Create tables
Base.metadata.create_all(bind=engine)