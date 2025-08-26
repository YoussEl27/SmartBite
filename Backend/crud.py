from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def create_history(db: Session, user_id: int, history: schemas.HistoryCreate):
    db_history = models.History(
        user_id=user_id,
        meal_name=history.Meal_name,
        calories=history.Calories,
        protein=history.Protein,
        carbs=history.Carbs,
        fat=history.Fat,
        sugar=history.Sugar,
        salt=history.Salt
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def get_histories_by_user(db: Session, user_id: int):
    return db.query(models.History).filter(models.History.user_id == user_id).all()