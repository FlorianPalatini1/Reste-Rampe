from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.database import get_db
from app.auth import get_current_user_from_token

router = APIRouter(prefix="/api/ingredients", tags=["ingredients"])


@router.get("/", response_model=List[schemas.Ingredient])
def list_ingredients(skip: int = 0, limit: int = 100, current_user: models.User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """List only the current user's ingredients"""
    return db.query(models.Ingredient).filter(models.Ingredient.user_id == current_user.id).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.Ingredient)
def create_ingredient(item: schemas.IngredientCreate, current_user: models.User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Create ingredient for current user"""
    db_item = models.Ingredient(
        user_id=current_user.id,
        name=item.name,
        category=item.category,
        location=item.location,
        quantity=item.quantity,
        unit=item.unit,
        expiry_date=item.expiry_date,
        notes=item.notes
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/{ingredient_id}", response_model=schemas.Ingredient)
def get_ingredient(ingredient_id: int, current_user: models.User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Get ingredient - only if it belongs to current user"""
    item = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id, models.Ingredient.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item


@router.put("/{ingredient_id}", response_model=schemas.Ingredient)
def update_ingredient(ingredient_id: int, item: schemas.IngredientCreate, current_user: models.User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Update ingredient - only if it belongs to current user"""
    db_item = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id, models.Ingredient.user_id == current_user.id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # Update fields
    db_item.name = item.name
    db_item.category = item.category
    db_item.location = item.location
    db_item.quantity = item.quantity
    db_item.unit = item.unit
    db_item.expiry_date = item.expiry_date
    db_item.notes = item.notes
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, current_user: models.User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Delete ingredient - only if it belongs to current user"""
    item = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id, models.Ingredient.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
