#!/bin/bash
set -e

cd /app

echo "Running database initialization..."
python3 scripts/init_db.py || true

echo "Ensuring test users exist..."
python3 << 'PYEOF'
import sys
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
db = SessionLocal()

try:
    # Ensure admin user exists with correct password and email verification
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@reste-rampe.de",
            hashed_password=pwd_context.hash("test123"),
            is_admin=True,
            is_email_verified=True
        )
        db.add(admin)
        print("✅ Created admin user")
    else:
        # Update existing admin user to have verified email and correct password
        admin.hashed_password = pwd_context.hash("test123")
        admin.is_email_verified = True
        admin.email_verification_token = None
        print("✅ Updated admin user")
    
    # Ensure tester6 user exists
    tester6 = db.query(User).filter(User.username == "tester6").first()
    if not tester6:
        tester6 = User(
            username="tester6",
            email="tester6@test.de",
            hashed_password=pwd_context.hash("test123"),
            is_admin=False,
            is_email_verified=True
        )
        db.add(tester6)
        print("✅ Created tester6 user")
    else:
        # Update existing tester6 user
        tester6.hashed_password = pwd_context.hash("test123")
        tester6.is_email_verified = True
        tester6.email_verification_token = None
        print("✅ Updated tester6 user")
    
    # Also handle the tester user (from init_db.py or earlier)
    tester = db.query(User).filter(User.username == "tester").first()
    if tester:
        tester.hashed_password = pwd_context.hash("test123")
        tester.is_email_verified = True
        tester.email_verification_token = None
        print("✅ Updated tester user")
    
    db.commit()
except Exception as e:
    db.rollback()
    print(f"⚠️  Could not create users: {e}")
finally:
    db.close()
PYEOF

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
