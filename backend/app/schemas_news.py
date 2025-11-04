from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsBase(BaseModel):
    title: str
    excerpt: str
    content: str
    category: str
    source: str
    image_url: Optional[str] = None
    language: str = "de"


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    source: Optional[str] = None
    image_url: Optional[str] = None


class NewsResponse(NewsBase):
    id: int
    published_at: datetime

    class Config:
        from_attributes = True
