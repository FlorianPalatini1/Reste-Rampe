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
from ..email_verification import generate_verification_token, send_verification_email

router = APIRouter(prefix="/api/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RegistrationResponse(BaseModel):
    message: str
    email: str


class VerifyEmailRequest(BaseModel):
    token: str


@router.post("/register", response_model=RegistrationResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user - sends verification email"""
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
    
    # Generate verification token
    verification_token = generate_verification_token()
    
    # Create new user (not verified yet)
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        email_verification_token=verification_token,
        is_email_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Send verification email
    email_sent = send_verification_email(user.email, user.username, verification_token)
    
    if not email_sent:
        # Delete user if email sending failed
        db.delete(db_user)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email. Please try again."
        )
    
    return {
        "message": "Registration successful! Please check your email to verify your account.",
        "email": user.email
    }


@router.post("/verify-email", response_model=Token)
async def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    """Verify email with token and return access token"""
    db_user = db.query(User).filter(
        User.email_verification_token == request.token
    ).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Mark email as verified
    db_user.is_email_verified = True
    db_user.email_verification_token = None
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
    
    # Check if email is verified
    if not db_user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
    
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
