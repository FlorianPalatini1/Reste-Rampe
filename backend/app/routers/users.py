from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import User
from .auth import get_current_user_from_token

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/")
def get_users(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all users"
        )
    
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at if hasattr(user, 'created_at') else None
        }
        for user in users
    ]


@router.get("/{user_id}")
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin or self only)"""
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile or be an admin"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "created_at": user.created_at if hasattr(user, 'created_at') else None
    }


@router.put("/{user_id}/admin")
def make_admin(
    user_id: int,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Make a user admin (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can grant admin permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already an admin"
        )
    
    user.is_admin = True
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "message": "User promoted to admin"
    }


@router.delete("/{user_id}/admin")
def remove_admin(
    user_id: int,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Remove admin status from a user (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can revoke admin permissions"
        )
    
    # Prevent removing admin from self
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove admin status from yourself"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not an admin"
        )
    
    user.is_admin = False
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "message": "Admin status removed"
    }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete users"
        )
    
    # Prevent deleting self
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return {
        "id": user.id,
        "message": "User deleted successfully"
    }
