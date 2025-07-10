import sqlite3
import os
from contextlib import contextmanager
from .config import settings

def get_connection():
    """Get database connection with foreign key support enabled"""
    conn = sqlite3.connect(settings.DATABASE_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@contextmanager
def get_db_cursor():
    """Context manager for database operations"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_database():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        className TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rollNumber TEXT NOT NULL,
        studentName TEXT,
        classId INTEGER NOT NULL,
        FOREIGN KEY (classId) REFERENCES classes (id) ON DELETE CASCADE,
        UNIQUE(rollNumber, classId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS examRooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roomNumber TEXT NOT NULL,
        roomCapacity INTEGER NOT NULL,
        roomFloor TEXT NOT NULL,
        roomBuilding TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()
