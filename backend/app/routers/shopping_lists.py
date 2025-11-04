from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ShoppingList, ShoppingItem
from app.schemas import ShoppingList as ShoppingListSchema, ShoppingListCreate, ShoppingItem as ShoppingItemSchema, ShoppingItemCreate

router = APIRouter()


@router.post("/", response_model=ShoppingListSchema)
def create_shopping_list(
    shopping_list: ShoppingListCreate,
    db: Session = Depends(get_db)
):
    """Create a new shopping list"""
    db_list = ShoppingList(name=shopping_list.name)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


@router.get("/", response_model=List[ShoppingListSchema])
def get_shopping_lists(db: Session = Depends(get_db)):
    """Get all shopping lists"""
    lists = db.query(ShoppingList).all()
    return lists


@router.get("/{list_id}", response_model=ShoppingListSchema)
def get_shopping_list(list_id: int, db: Session = Depends(get_db)):
    """Get a specific shopping list with all items"""
    db_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return db_list


@router.post("/{list_id}/items", response_model=ShoppingItemSchema)
def add_item_to_list(
    list_id: int,
    item: ShoppingItemCreate,
    db: Session = Depends(get_db)
):
    """Add an item to a shopping list"""
    # Verify list exists
    db_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    db_item = ShoppingItem(
        list_id=list_id,
        item_name=item.item_name,
        quantity=item.quantity,
        unit=item.unit
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/{list_id}/items/{item_id}", response_model=ShoppingItemSchema)
def update_item(
    list_id: int,
    item_id: int,
    item: ShoppingItemCreate,
    db: Session = Depends(get_db)
):
    """Update a shopping list item"""
    db_item = db.query(ShoppingItem).filter(
        ShoppingItem.id == item_id,
        ShoppingItem.list_id == list_id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.item_name = item.item_name
    db_item.quantity = item.quantity
    db_item.unit = item.unit
    db.commit()
    db.refresh(db_item)
    return db_item


@router.patch("/{list_id}/items/{item_id}/toggle", response_model=ShoppingItemSchema)
def toggle_item_purchased(
    list_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """Toggle the purchased status of an item"""
    db_item = db.query(ShoppingItem).filter(
        ShoppingItem.id == item_id,
        ShoppingItem.list_id == list_id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.is_purchased = not db_item.is_purchased
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{list_id}/items/{item_id}")
def delete_item(
    list_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete an item from a shopping list"""
    db_item = db.query(ShoppingItem).filter(
        ShoppingItem.id == item_id,
        ShoppingItem.list_id == list_id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"status": "deleted"}


@router.delete("/{list_id}")
def delete_shopping_list(list_id: int, db: Session = Depends(get_db)):
    """Delete a shopping list and all its items"""
    db_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    db.delete(db_list)
    db.commit()
    return {"status": "deleted"}
