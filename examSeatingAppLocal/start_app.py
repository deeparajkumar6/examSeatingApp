#!/usr/bin/env python3
"""
Startup script for the Exam Seating App
This script helps users get started quickly
"""

import os
import sys
import subprocess
import sqlite3

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is available")
    
    # Check if we're in the right directory
    if not os.path.exists('fastapi_app/main.py'):
        print("❌ Please run this script from the project root directory")
        return False
    print("✅ Project structure looks good")
    
    # Check database
    db_path = 'fastapi_app/database_new.db'
    if os.path.exists(db_path):
        print("✅ Database found")
    else:
        print("⚠️  Database not found, will be created on first run")
    
    return True

def setup_database():
    """Set up the database with sample data"""
    print("\n📊 Setting up database...")
    
    db_path = 'fastapi_app/database_new.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        className TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rollNumber TEXT NOT NULL,
        studentName TEXT,
        classId INTEGER NOT NULL,
        FOREIGN KEY (classId) REFERENCES classes (id) ON DELETE CASCADE,
        UNIQUE(rollNumber, classId)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS examRooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roomNumber TEXT NOT NULL,
        roomCapacity INTEGER NOT NULL,
        roomFloor TEXT NOT NULL,
        roomBuilding TEXT NOT NULL
    )
    ''')
    
    # Check if we have any data
    cursor.execute('SELECT COUNT(*) FROM classes')
    class_count = cursor.fetchone()[0]
    
    if class_count == 0:
        print("📝 Adding sample data...")
        
        # Add sample class
        cursor.execute('INSERT INTO classes (className) VALUES (?)', ('Sample Class',))
        class_id = cursor.lastrowid
        
        # Add sample students
        sample_students = [
            ('101', 'John Doe'),
            ('102', 'Jane Smith'),
            ('103', 'Bob Johnson'),
            ('105', 'Alice Brown'),  # Note: 104 is missing intentionally
            ('107', 'Charlie Wilson')
        ]
        
        for roll, name in sample_students:
            cursor.execute('INSERT INTO students (rollNumber, studentName, classId) VALUES (?, ?, ?)',
                          (roll, name, class_id))
        
        # Add sample exam room
        cursor.execute('INSERT INTO examRooms (roomNumber, roomCapacity, roomFloor, roomBuilding) VALUES (?, ?, ?, ?)',
                      ('Room 101', 30, 'Ground Floor', 'Main Building'))
        
        print("✅ Sample data added")
    else:
        print(f"✅ Database already has {class_count} classes")
    
    conn.commit()
    conn.close()

def show_instructions():
    """Show startup instructions"""
    print("\n🚀 Getting Started:")
    print("1. Start the API server:")
    print("   cd fastapi_app")
    print("   pip install -r requirements.txt")
    print("   fastapi dev main.py")
    print("\n2. Start the UI (in a new terminal):")
    print("   cd UI")
    print("   npm install")
    print("   npm run dev")
    print("\n3. Open your browser to:")
    print("   - API: http://localhost:8000")
    print("   - UI: http://localhost:3000 (or as shown by Vite)")
    print("\n📚 Features:")
    print("   - Add classes with individual students")
    print("   - Upload students from CSV files")
    print("   - Add exam rooms with capacity and location details")
    print("   - Upload exam rooms from CSV files")
    print("   - Generate exam seating arrangements")
    print("   - Export schedules to PDF with college branding")
    print("\n📄 Documentation:")
    print("   - CSV Upload Guide: CSV_UPLOAD_GUIDE.md")
    print("   - PDF Customization Guide: PDF_CUSTOMIZATION_GUIDE.md")
    print("   - Theme Colors Guide: THEME_COLORS.md")
    print("   - API Documentation: http://localhost:8000/docs (when running)")

def main():
    print("🎓 Exam Seating App Setup - Shahun Jain College for Women")
    print("=" * 60)
    
    if not check_requirements():
        sys.exit(1)
    
    setup_database()
    show_instructions()
    
    print("\n✨ Setup complete! Follow the instructions above to start the application.")

if __name__ == "__main__":
    main()
