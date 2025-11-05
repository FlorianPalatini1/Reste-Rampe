"""
Mailbox Management Router

Handles user mailbox operations:
- Create mailbox
- Get mailbox status and quota
- Delete mailbox
- Manage forwarding rules
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from ..database import get_db
from ..models import User
from ..auth import get_current_user_from_token
from ..mailcow_api import MailcowAPI

router = APIRouter(prefix="/api/mailbox", tags=["mailbox"])

# ============ SCHEMAS ============


class MailboxStatus(BaseModel):
    """Mailbox status response"""
    enabled: bool
    username: str
    email: str
    quota_mb: int
    quota_percent: int
    active: bool
    created_at: Optional[datetime] = None


class MailboxQuota(BaseModel):
    """Mailbox quota information"""
    quota_total_mb: int
    quota_used_mb: int
    quota_percent: int


class CreateMailboxRequest(BaseModel):
    """Request to create mailbox"""
    password: str  # User provides password


class MailboxPassword(BaseModel):
    """Password change request"""
    new_password: str


class ForwardingRule(BaseModel):
    """Email forwarding rule"""
    destination: EmailStr
    keep_local_copy: bool = True


# ============ HELPER FUNCTIONS ============


def get_mailcow_client() -> MailcowAPI:
    """Get Mailcow API client instance"""
    return MailcowAPI()


def get_mailbox_username(user: User) -> str:
    """Extract mailbox username from user email"""
    if not user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email not set"
        )
    # Extract username part (before @)
    return user.email.split("@")[0]


# ============ USER ENDPOINTS ============


@router.get("", response_model=MailboxStatus)
async def get_mailbox_status(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """Get current user's mailbox status"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    mailbox_username = get_mailbox_username(user)
    mailcow = get_mailcow_client()

    # Get mailbox details from Mailcow
    details = mailcow.get_mailbox_details(mailbox_username)

    if not details:
        # Mailbox doesn't exist in Mailcow
        return MailboxStatus(
            enabled=False,
            username=mailbox_username,
            email=user.email,
            quota_mb=user.mailbox_quota_mb,
            quota_percent=0,
            active=False,
            created_at=user.mailbox_created_at,
        )

    # Mailbox exists, return details
    quota_total = details.get("quota", 0)
    quota_used = details.get("bytes", 0)
    quota_percent = int((quota_used / quota_total * 100)) if quota_total > 0 else 0

    return MailboxStatus(
        enabled=True,
        username=mailbox_username,
        email=user.email,
        quota_mb=int(quota_total / (1024 * 1024)),  # Convert bytes to MB
        quota_percent=quota_percent,
        active=details.get("active", 0) == 1,
        created_at=user.mailbox_created_at,
    )


@router.post("", status_code=201)
async def create_mailbox(
    request: CreateMailboxRequest,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """Create mailbox for current user"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if mailbox already exists
    if user.mailbox_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mailbox already exists for this user"
        )

    mailbox_username = get_mailbox_username(user)
    mailcow = get_mailcow_client()

    # Create mailbox in Mailcow
    success = mailcow.create_mailbox(
        username=mailbox_username,
        password=request.password,
        display_name=user.username,
        quota_mb=user.mailbox_quota_mb,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create mailbox. Check API logs for details."
        )

    # Update user record
    user.mailbox_enabled = True
    user.mailbox_active = True
    user.mailbox_created_at = datetime.utcnow()
    db.commit()

    return {
        "message": "Mailbox created successfully",
        "email": f"{mailbox_username}@reste-rampe.tech",
    }


@router.delete("", status_code=200)
async def delete_mailbox(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """Delete mailbox for current user"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.mailbox_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No mailbox to delete"
        )

    mailbox_username = get_mailbox_username(user)
    mailcow = get_mailcow_client()

    # Delete mailbox from Mailcow
    success = mailcow.delete_mailbox(mailbox_username)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete mailbox"
        )

    # Update user record
    user.mailbox_enabled = False
    user.mailbox_active = False
    db.commit()

    return {"message": "Mailbox deleted successfully"}


@router.get("/quota", response_model=MailboxQuota)
async def get_mailbox_quota(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """Get mailbox quota and usage"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.mailbox_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no mailbox"
        )

    mailbox_username = get_mailbox_username(user)
    mailcow = get_mailcow_client()

    quota = mailcow.get_mailbox_quota(mailbox_username)

    if not quota:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve quota information"
        )

    return MailboxQuota(
        quota_total_mb=int(quota["quota_total"] / (1024 * 1024)),
        quota_used_mb=int(quota["quota_used"] / (1024 * 1024)),
        quota_percent=quota["quota_percent"],
    )


@router.post("/password")
async def change_mailbox_password(
    request: MailboxPassword,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """Change mailbox password"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.mailbox_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no mailbox"
        )

    mailbox_username = get_mailbox_username(user)
    mailcow = get_mailcow_client()

    success = mailcow.set_mailbox_password(mailbox_username, request.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )

    return {"message": "Password changed successfully"}


@router.post("/forwarding")
async def add_forwarding_rule(
    request: ForwardingRule,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """Add email forwarding rule"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.mailbox_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no mailbox"
        )

    mailbox_username = get_mailbox_username(user)
    mailcow = get_mailcow_client()

    success = mailcow.add_forwarding(
        username=mailbox_username,
        forward_to=request.destination,
        keep_local=request.keep_local_copy,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add forwarding rule"
        )

    return {
        "message": "Forwarding rule added",
        "destination": request.destination,
    }


@router.delete("/forwarding/{destination}")
async def remove_forwarding_rule(
    destination: str,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """Remove email forwarding rule"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.mailbox_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no mailbox"
        )

    mailbox_username = get_mailbox_username(user)
    mailcow = get_mailcow_client()

    success = mailcow.remove_forwarding(mailbox_username, destination)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove forwarding rule"
        )

    return {"message": "Forwarding rule removed"}


@router.get("/forwarding")
async def get_forwarding_rules(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """Get all forwarding rules for user's mailbox"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.mailbox_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no mailbox"
        )

    mailbox_username = get_mailbox_username(user)
    mailcow = get_mailcow_client()

    rules = mailcow.get_forwarding_rules(mailbox_username)

    if rules is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve forwarding rules"
        )

    return {"forwarding_rules": rules or []}
