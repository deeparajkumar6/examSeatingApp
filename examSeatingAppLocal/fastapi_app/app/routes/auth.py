from fastapi import APIRouter, HTTPException
from typing import Dict, List
from ..models import UserModel, UserResponseModel, LoginRequest, LoginResponse
from ..auth_service import AuthService
import secrets

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest):
    """Authenticate user and return token"""
    user = AuthService.authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    # Generate simple token (in production, use JWT)
    token = secrets.token_urlsafe(32)
    
    return LoginResponse(token=token, user=user)

@router.get("/users", response_model=Dict)
def get_users():
    """Get all users except admin"""
    users = AuthService.get_all_users()
    return {"users": users}

@router.post("/users")
def create_user(user_data: UserModel):
    """Create a new user"""
    AuthService.create_user(user_data)
    return {"message": "User created successfully"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user"""
    AuthService.delete_user(user_id)
    return {"message": "User deleted successfully"}