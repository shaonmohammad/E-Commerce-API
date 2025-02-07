from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserResponse
from dependencies import get_db
from utils import get_hashed_password, create_access_token, create_refresh_token, verify_password

router = APIRouter(tags=["auth"])

@router.post("/signup/", response_model=UserResponse)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_hashed_password(user.password)
    new_user = User(
        username=user.username,  # Ensure username is saved
        email=user.email,
        password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")  # Changed to 401

    access_token = create_access_token(subject=user.email)
    refresh_token = create_refresh_token(subject=user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
