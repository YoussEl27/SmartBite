from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    history = relationship("History", back_populates="user", cascade="all, delete")

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    meal_name = Column(String(100), nullable=False)
    calories = Column(Integer, nullable=False)
    meal_date = Column(TIMESTAMP, server_default=func.now())
    user = relationship("User", back_populates="history")