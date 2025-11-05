#!/usr/bin/env python3
"""
Script to create an admin user in the Reste-Rampe database.
Usage: python3 create_admin.py
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.database import SessionLocal, engine, Base
from app.models import User
from app.auth import hash_password
from sqlalchemy.exc import IntegrityError

def create_admin_user(username: str = "admin", password: str = "admin123", email: str = "admin@reste-rampe.local"):
    """Create an admin user in the database."""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"❌ User '{username}' already exists!")
            return False
        
        # Create new admin user
        hashed_password = hash_password(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ Admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Is Admin: {admin_user.is_admin}")
        print(f"\n🔐 Please change the password after first login!")
        
        return True
        
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Error: User already exists or email conflict!")
        return False
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create an admin user for Reste-Rampe")
    parser.add_argument("--username", default="admin", help="Admin username (default: admin)")
    parser.add_argument("--password", default="admin123", help="Admin password (default: admin123)")
    parser.add_argument("--email", default="admin@reste-rampe.local", help="Admin email")
    
    args = parser.parse_args()
    
    success = create_admin_user(args.username, args.password, args.email)
    sys.exit(0 if success else 1)
