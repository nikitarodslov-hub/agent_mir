from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=dict)
async def register(user: RegisterRequest):
    return {"status": "success", "message": "User registered"}

@router.post("/login", response_model=TokenResponse)
async def login(user: LoginRequest):
    return {"access_token": "token_123", "token_type": "bearer"}

@router.post("/logout")
async def logout():
    return {"status": "success"}

@router.post("/refresh-token")
async def refresh_token():
    return {"access_token": "new_token"}

@router.get("/me")
async def get_current_user(token: str = None):
    return {"user_id": "user_123", "email": "user@example.com"}
