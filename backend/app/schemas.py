from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class IngredientBase(BaseModel):
    name: str
    category: Optional[str] = None
    location: Optional[str] = "Fridge"
    quantity: Optional[int] = 1
    unit: Optional[str] = "kg"
    expiry_date: Optional[date] = None
    notes: Optional[str] = None


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True


class ShoppingItemBase(BaseModel):
    item_name: str
    quantity: int = 1
    unit: str = "piece"


class ShoppingItemCreate(ShoppingItemBase):
    pass


class ShoppingItem(ShoppingItemBase):
    id: int
    list_id: int
    is_purchased: bool = False

    class Config:
        orm_mode = True


class ShoppingListBase(BaseModel):
    name: str


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingList(ShoppingListBase):
    id: int
    items: List[ShoppingItem] = []

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: str  # JSON list
    instructions: str
    prep_time: Optional[int] = None
    servings: Optional[int] = 1
    calories: Optional[int] = None
    is_healthy: bool = False
    language: str = "de"


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AISuggestionBase(BaseModel):
    text: str
    dietary: Optional[str] = None


class AISuggestion(AISuggestionBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class SaveAIRecipeRequest(BaseModel):
    text: str
    title: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_admin: bool = False

    class Config:
        orm_mode = True


class PageBase(BaseModel):
    slug: str
    title: str
    content: str
    language: str = "de"
    page_key: str = "privacy"


class PageCreate(PageBase):
    pass


class PageUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    language: Optional[str] = None


class PageResponse(PageBase):
    id: int
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


