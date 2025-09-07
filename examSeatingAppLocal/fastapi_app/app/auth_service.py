import sqlite3
from typing import List, Optional
from fastapi import HTTPException
from .database import get_db_cursor
from .models import UserModel, UserResponseModel, LoginRequest

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[UserResponseModel]:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT id, username, name, created_at FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            user = cursor.fetchone()
            
            if user:
                return UserResponseModel(
                    id=user[0],
                    username=user[1],
                    name=user[2],
                    created_at=user[3]
                )
            return None
    
    @staticmethod
    def get_all_users() -> List[UserResponseModel]:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT id, username, name, created_at FROM users WHERE username != 'admin' ORDER BY created_at DESC"
            )
            users = cursor.fetchall()
            
            return [
                UserResponseModel(
                    id=user[0],
                    username=user[1],
                    name=user[2],
                    created_at=user[3]
                )
                for user in users
            ]
    
    @staticmethod
    def create_user(user_data: UserModel) -> None:
        with get_db_cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                    (user_data.username, user_data.password, user_data.name)
                )
            except sqlite3.IntegrityError:
                raise HTTPException(
                    status_code=400,
                    detail="Username already exists"
                )
    
    @staticmethod
    def delete_user(user_id: int) -> None:
        with get_db_cursor() as cursor:
            # Prevent deletion of admin user
            cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            if user[0] == "admin":
                raise HTTPException(status_code=400, detail="Cannot delete admin user")
            
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))