"""
Admin Mailbox Management Router

Admin-only endpoints for managing mailboxes:
- List all mailboxes
- Disable/enable mailboxes
- Manage quotas
- View statistics
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import User
from ..auth import get_current_user_from_token
from ..mailcow_api import MailcowAPI
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin/mailboxes", tags=["admin-mailbox"])

# ============ SCHEMAS ============


class MailboxListItem(BaseModel):
    """Mailbox item in list"""
    email: str
    username: str
    active: bool
    quota_mb: int
    quota_used_mb: int
    quota_percent: int
    messages: int


class AdminMailboxStats(BaseModel):
    """Overall mailbox statistics"""
    total_mailboxes: int
    active_mailboxes: int
    total_quota_mb: int
    total_used_mb: int


# ============ HELPER FUNCTIONS ============


def check_admin(current_user: User = Depends(get_current_user_from_token)):
    """Verify current user is admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def get_mailcow_client() -> MailcowAPI:
    """Get Mailcow API client"""
    return MailcowAPI()


# ============ ADMIN ENDPOINTS ============


@router.get("", response_model=List[MailboxListItem])
async def list_all_mailboxes(
    _: User = Depends(check_admin),
    db: Session = Depends(get_db),
):
    """List all mailboxes (admin only)"""
    mailcow = get_mailcow_client()

    mailboxes = mailcow.get_all_mailboxes()
    if mailboxes is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch mailboxes from Mailcow"
        )

    result = []
    for mb in mailboxes:
        email = mb.get("username", "")
        username = email.split("@")[0] if "@" in email else email

        quota_total = mb.get("quota", 1)  # Avoid division by zero
        quota_used = mb.get("bytes", 0)
        quota_percent = int((quota_used / quota_total * 100)) if quota_total > 0 else 0

        result.append(MailboxListItem(
            email=email,
            username=username,
            active=mb.get("active", 0) == 1,
            quota_mb=int(quota_total / (1024 * 1024)),
            quota_used_mb=int(quota_used / (1024 * 1024)),
            quota_percent=quota_percent,
            messages=mb.get("messages", 0),
        ))

    return result


@router.get("/stats", response_model=AdminMailboxStats)
async def get_mailbox_statistics(
    _: User = Depends(check_admin),
    db: Session = Depends(get_db),
):
    """Get overall mailbox statistics"""
    mailcow = get_mailcow_client()

    mailboxes = mailcow.get_all_mailboxes()
    if mailboxes is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch mailboxes from Mailcow"
        )

    total_mailboxes = len(mailboxes)
    active_mailboxes = sum(1 for mb in mailboxes if mb.get("active", 0) == 1)
    total_quota_mb = sum(int(mb.get("quota", 0) / (1024 * 1024)) for mb in mailboxes)
    total_used_mb = sum(int(mb.get("bytes", 0) / (1024 * 1024)) for mb in mailboxes)

    return AdminMailboxStats(
        total_mailboxes=total_mailboxes,
        active_mailboxes=active_mailboxes,
        total_quota_mb=total_quota_mb,
        total_used_mb=total_used_mb,
    )


@router.post("/{username}/disable")
async def disable_mailbox_admin(
    username: str,
    _: User = Depends(check_admin),
    db: Session = Depends(get_db),
):
    """Disable a mailbox (admin only)"""
    mailcow = get_mailcow_client()

    success = mailcow.disable_mailbox(username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to disable mailbox"
        )

    # Update user record
    user = db.query(User).filter(
        User.email.like(f"{username}@%")
    ).first()
    if user:
        user.mailbox_active = False
        db.commit()

    return {"message": f"Mailbox {username} disabled"}


@router.post("/{username}/enable")
async def enable_mailbox_admin(
    username: str,
    _: User = Depends(check_admin),
    db: Session = Depends(get_db),
):
    """Enable a mailbox (admin only)"""
    mailcow = get_mailcow_client()

    success = mailcow.enable_mailbox(username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to enable mailbox"
        )

    # Update user record
    user = db.query(User).filter(
        User.email.like(f"{username}@%")
    ).first()
    if user:
        user.mailbox_active = True
        db.commit()

    return {"message": f"Mailbox {username} enabled"}


@router.post("/{username}/quota")
async def set_mailbox_quota_admin(
    username: str,
    quota_mb: int = Query(..., gt=0),
    _: User = Depends(check_admin),
    db: Session = Depends(get_db),
):
    """Set mailbox quota (admin only)"""
    mailcow = get_mailcow_client()

    success = mailcow.set_mailbox_quota(username, quota_mb)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set quota"
        )

    # Update user record
    user = db.query(User).filter(
        User.email.like(f"{username}@%")
    ).first()
    if user:
        user.mailbox_quota_mb = quota_mb
        db.commit()

    return {"message": f"Quota for {username} set to {quota_mb}MB"}


@router.get("/{username}")
async def get_mailbox_admin(
    username: str,
    _: User = Depends(check_admin),
    db: Session = Depends(get_db),
):
    """Get detailed mailbox information (admin only)"""
    mailcow = get_mailcow_client()

    # Get details
    details = mailcow.get_mailbox_details(username)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mailbox not found"
        )

    # Get forwarding rules
    forwarding = mailcow.get_forwarding_rules(username)

    quota_total = details.get("quota", 1)
    quota_used = details.get("bytes", 0)
    quota_percent = int((quota_used / quota_total * 100)) if quota_total > 0 else 0

    return {
        "email": details.get("username"),
        "name": details.get("name"),
        "active": details.get("active") == 1,
        "quota_mb": int(quota_total / (1024 * 1024)),
        "quota_used_mb": int(quota_used / (1024 * 1024)),
        "quota_percent": quota_percent,
        "messages": details.get("messages", 0),
        "forwarding_rules": forwarding or [],
        "created": details.get("created"),
        "modified": details.get("modified"),
    }


@router.delete("/{username}")
async def delete_mailbox_admin(
    username: str,
    _: User = Depends(check_admin),
    db: Session = Depends(get_db),
):
    """Delete mailbox (admin only)"""
    mailcow = get_mailcow_client()

    success = mailcow.delete_mailbox(username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete mailbox"
        )

    # Update user record
    user = db.query(User).filter(
        User.email.like(f"{username}@%")
    ).first()
    if user:
        user.mailbox_enabled = False
        user.mailbox_active = False
        db.commit()

    return {"message": f"Mailbox {username} deleted"}
