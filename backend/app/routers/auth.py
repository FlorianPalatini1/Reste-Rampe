from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
from typing import Optional

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, User as UserSchema
from ..auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_from_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if user.email:
        db_email = db.query(User).filter(User.email == user.email).first()
        if db_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    # Find user by username
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
async def get_current_user(current_user: User = Depends(get_current_user_from_token)):
    """Get current user info from token"""
    return current_user
