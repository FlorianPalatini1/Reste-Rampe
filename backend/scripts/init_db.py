"""Very small seeding script for dev use."""
from app.database import SessionLocal, engine, Base
from app import models


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(models.Ingredient).first():
            items = [
                models.Ingredient(name="Tomato", category="Vegetable"),
                models.Ingredient(name="Flour", category="Baking"),
                models.Ingredient(name="Sugar", category="Baking"),
            ]
            db.add_all(items)
            db.commit()
            print("Seeded ingredients")
        else:
            print("Ingredients already present, skipping")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
