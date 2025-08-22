from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    if data.username == "admin" and data.password == "1234":
        return {"success": True}
    return {"success": False}
