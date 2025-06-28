#!/usr/bin/env python3
"""
Database migration script to convert from roll number ranges to explicit student records.
Run this script once to migrate your existing data.
"""

import sqlite3
import os

def migrate_database():
    db_path = "database.db"
    backup_path = "database_backup.db"
    
    # Create backup
    if os.path.exists(db_path):
        print("Creating backup of existing database...")
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if old structure exists
        cursor.execute("PRAGMA table_info(classes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'startRollNumber' in columns and 'endRollNumber' in columns:
            print("Old database structure detected. Starting migration...")
            
            # Get existing classes with roll number ranges
            cursor.execute("SELECT id, className, startRollNumber, endRollNumber FROM classes")
            old_classes = cursor.fetchall()
            
            # Drop existing students table if it exists
            cursor.execute("DROP TABLE IF EXISTS students")
            
            # Create new tables with correct structure
            cursor.execute("""
            CREATE TABLE classes_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                className TEXT NOT NULL
            )
            """)
            
            cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rollNumber TEXT NOT NULL,
                studentName TEXT,
                classId INTEGER NOT NULL,
                FOREIGN KEY (classId) REFERENCES classes (id) ON DELETE CASCADE,
                UNIQUE(rollNumber, classId)
            )
            """)
            
            # Migrate data
            for old_class in old_classes:
                class_id, class_name, start_roll, end_roll = old_class
                
                # Insert class into new structure
                cursor.execute("INSERT INTO classes_new (className) VALUES (?)", (class_name,))
                new_class_id = cursor.lastrowid
                
                # Generate students from roll number range
                for roll_num in range(start_roll, end_roll + 1):
                    cursor.execute("""
                        INSERT INTO students (rollNumber, studentName, classId)
                        VALUES (?, ?, ?)
                    """, (str(roll_num), None, new_class_id))
                
                print(f"Migrated class '{class_name}' with {end_roll - start_roll + 1} students")
            
            # Drop old table and rename new one
            cursor.execute("DROP TABLE classes")
            cursor.execute("ALTER TABLE classes_new RENAME TO classes")
            
            conn.commit()
            print("Migration completed successfully!")
            print("Note: All students have been created with roll numbers but no names.")
            print("You can now add student names through the UI.")
            
        else:
            print("Database already uses the new structure. No migration needed.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
