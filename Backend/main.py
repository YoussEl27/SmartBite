from fastapi import FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated, List
from pydantic import BaseModel
from database import SessionLocal, engine, get_db
from auth import get_current_user, create_access_token
import models
import crud
import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


class LoginData(BaseModel):
    username: str
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/login")
async def login(data: LoginData, db: db_dependency):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Benutzer nicht gefunden")
    if not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Falsches Passwort")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users")
async def create_user(user: schemas.UserBase, db: db_dependency):
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username oder Email existiert schon")
    return crud.create_user(db, user)

@app.post("/history")
async def create_history(history: schemas.HistoryCreate, db: db_dependency, current_user: models.User = Depends(get_current_user)):
    return crud.create_history(db, user_id= current_user.id, history=history)

@app.get("/history/")
async def get_history(db: db_dependency, current_user: models.User = Depends(get_current_user)):
    return crud.get_histories_by_user(db, user_id= current_user.id)
