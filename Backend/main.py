from fastapi import FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel
from database import SessionLocal, engine
import psycopg2 as sql
import models
import crud
import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root():
    return {
        "message": "✅ SmartBite API läuft!",
        "endpoints": [
            "GET /test-db",
            "POST /login",
            "POST /users",
            "GET /docs"
        ]
    }

class LoginData(BaseModel):
    username: str
    password: str

class UserBase(BaseModel):
    username: str
    password: str
    email: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Benutzer nicht gefunden")
    if not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Falsches Passwort")

    return {"success": True, "message": "Login erfolgreich", "user_id": user.id}

@app.post("/users")
def create_user(user: UserBase, db: db_dependency):
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username oder Email existiert schon")
    return crud.create_user(db, user)

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute("SELECT 1").scalar()
        return {"db_connection": True, "result": result}
    except Exception as e:
        return {"db_connection": False, "error": str(e)}

while True:
    try:
        conn = sql.connect(
            database="postgres",
            user="postgres",
            host="localhost",
            password="Ysf@2002",
            port="5432",
        )
        cursor = conn.cursor()
        print("Successfully!")
        break

    except Exception as e:
        print("Not Successfull!")
        break