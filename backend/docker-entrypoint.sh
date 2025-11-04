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
    # Check if admin user exists
    admin_exists = db.query(User).filter(User.username == "admin").first()
    if not admin_exists:
        admin = User(
            username="admin",
            email="admin@reste-rampe.de",
            hashed_password=pwd_context.hash("test123"),
            is_admin=True
        )
        db.add(admin)
        print("✅ Created admin user")
    else:
        print("✅ Admin user already exists")
    
    # Check if tester6 user exists
    tester_exists = db.query(User).filter(User.username == "tester6").first()
    if not tester_exists:
        tester = User(
            username="tester6",
            email="tester6@test.de",
            hashed_password=pwd_context.hash("test123"),
            is_admin=False
        )
        db.add(tester)
        print("✅ Created tester6 user")
    else:
        print("✅ Tester6 user already exists")
    
    db.commit()
except Exception as e:
    db.rollback()
    print(f"⚠️  Could not create users: {e}")
finally:
    db.close()
PYEOF

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
