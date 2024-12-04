from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional


class ChristianBase(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr
    phone: str
    status: Optional[str] = None
    role: str
    event_id: Optional[int] 
    joined_date: Optional[date] = None  

class ChristianCreate(ChristianBase):
    joined_date: Optional[date] = None  

class Christian(ChristianBase):
    id: int

    class Config:
        orm_mode = True  

class EventCreate(BaseModel):
    name: str
    location: str
    date: date
    description: Optional[str] = None  

class Event(EventCreate):
    id: int
    attendees: List[Christian] = []  

    class Config:
        orm_mode = True  
