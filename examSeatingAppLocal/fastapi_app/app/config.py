import os
from typing import List

class Settings:
    # Database settings
    DATABASE_PATH: str = "database.db"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Scheduling settings
    MAX_STUDENTS_PER_CLASS_PER_ROOM: int = 20
    
    # API settings
    API_TITLE: str = "Exam Seating App API"
    API_DESCRIPTION: str = "API for managing exam seating arrangements"
    API_VERSION: str = "1.0.0"

settings = Settings()
