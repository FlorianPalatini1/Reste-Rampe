from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NULL = shared/global
    name = Column(String(200), nullable=False, unique=False)  # Not unique anymore (per user)
    category = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True, default="Fridge")
    quantity = Column(Integer, nullable=True, default=1)
    unit = Column(String(50), nullable=True, default="kg")
    expiry_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)


class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    items = relationship("ShoppingItem", back_populates="list", cascade="all, delete-orphan")


class ShoppingItem(Base):
    __tablename__ = "shopping_items"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    item_name = Column(String(200), nullable=False)
    quantity = Column(Integer, default=1)
    unit = Column(String(50), default="piece")
    is_purchased = Column(Boolean, default=False)
    list = relationship("ShoppingList", back_populates="items")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=False)  # JSON list
    instructions = Column(Text, nullable=False)
    prep_time = Column(Integer, nullable=True)  # in minutes
    servings = Column(Integer, nullable=True, default=1)
    calories = Column(Integer, nullable=True)
    language = Column(String(10), default="de", nullable=False)  # Language code (de, en, fr, etc)
    is_healthy = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class AISuggestion(Base):
    __tablename__ = "ai_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    dietary = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    excerpt = Column(String(1000), nullable=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    source = Column(String(200), nullable=True)
    image_url = Column(String(500), nullable=True)
    language = Column(String(10), default="de", nullable=False)
    published_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class Page(Base):
    __tablename__ = "pages"
    __table_args__ = (
        UniqueConstraint('page_key', 'language', name='uq_page_key_language'),
    )

    id = Column(Integer, primary_key=True, index=True)
    page_key = Column(String(100), nullable=False, default="privacy")
    slug = Column(String(100), nullable=False)
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(10), default="de", nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


