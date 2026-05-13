from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BookmarkCreate(BaseModel):
    url: str
    title: str
    description: Optional[str] = None
    tags: list[str] = []


class BookmarkUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[list[str]] = None
