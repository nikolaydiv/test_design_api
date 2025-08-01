from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()
users = {}

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(..., ge=1, le=100)
    password: str = Field(..., min_length=6, max_length=20)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@app.post("/register")
def register_user(user: UserRegistration):
    if "admin" in user.username.lower():
        raise HTTPException(status_code=400, detail="Username cannot contain 'admin'")
    if user.password == "123456":
        raise HTTPException(status_code=400, detail="Too weak password")
    if user.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    users[user.email] = user.password
    return {"message": "User registered successfully"}

@app.post("/login")
def login_user(user: UserLogin):
    if user.email not in users:
        raise HTTPException(status_code=400, detail="Email not registered")
    if users[user.email] != user.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"message": "Login successful"}

@app.get("/user/{email}")
def get_user(email: EmailStr):
    if email in users:
        return {"email": email, "registered": True}
    else:
        raise HTTPException(status_code=400, detail="User is not registered")
