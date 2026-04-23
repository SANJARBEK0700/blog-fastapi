from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    """Post uchun asosiy maydonlar"""
    title: str = Field(..., min_length=1, max_length=200, description="Post sarlavhasi")
    content: str = Field(..., min_length=1, description="Post matni")
    author: str = Field(..., min_length=1, max_length=100, description="Muallif ismi")


class PostCreate(PostBase):
    """Yangi post yaratish uchun schema"""
    pass


class PostUpdate(BaseModel):
    """Postni yangilash uchun schema (barcha maydonlar ixtiyoriy)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1, max_length=100)


class Post(PostBase):
    """Post ma'lumotlarini qaytarish uchun schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
