from pydantic import BaseModel
from datetime import datetime
from typing import List

class HistoryBase(BaseModel):
    Meal_name: str
    Calories: float
    Protein: float
    Carbs: float
    Fat: float
    Sugar: float
    Salt: float
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