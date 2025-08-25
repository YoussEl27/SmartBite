from pydantic import BaseModel
from datetime import datetime
from typing import List

class HistoryBase(BaseModel):
    meal_name: str
    calories: int
    protein: int
    carbs: int
    fat: int
    sugar: int
    salt: int

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    id: int
    user_id: int
    meal_date: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    password: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    history: List[History] = []

    class Config:
        from_attributes = True