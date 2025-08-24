from pydantic import BaseModel
from datetime import datetime
from typing import List

class HistoryBase(BaseModel):
    meal_name: str
    calories: int

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    id: int
    meal_date: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    history: List[History] = []

    class Config:
        from_attributes = True