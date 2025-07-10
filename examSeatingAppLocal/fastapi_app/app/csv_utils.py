import csv
import io
import sqlite3
from typing import Dict, List, Any
from fastapi import HTTPException, UploadFile
from .database import get_db_cursor

class CSVProcessor:
    @staticmethod
    async def process_students_csv(file: UploadFile) -> Dict[str, Any]:
        """Process student CSV upload"""
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        try:
            content = await file.read()
            csv_content = content.decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            # Validate required columns
            required_columns = ['className', 'rollNumber', 'studentName']
            CSVProcessor._validate_csv_columns(csv_reader, required_columns)
            
            # Process CSV data
            csv_data = CSVProcessor._extract_student_data(csv_reader)
            
            if not csv_data:
                raise HTTPException(status_code=400, detail="No valid data found in CSV file")
            
            # Group by class name and process
            return CSVProcessor._process_student_classes(csv_data)
            
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File encoding error. Please ensure the CSV file is UTF-8 encoded")
        except csv.Error as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV file: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")

    @staticmethod
    async def process_exam_rooms_csv(file: UploadFile) -> Dict[str, Any]:
        """Process exam rooms CSV upload"""
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        try:
            content = await file.read()
            csv_content = content.decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            # Validate required columns
            required_columns = ['roomNumber', 'roomCapacity', 'roomFloor', 'roomBuilding']
            CSVProcessor._validate_csv_columns(csv_reader, required_columns)
            
            # Process CSV data
            csv_data = CSVProcessor._extract_room_data(csv_reader)
            
            if not csv_data:
                raise HTTPException(status_code=400, detail="No valid data found in CSV file")
            
            return CSVProcessor._process_exam_rooms(csv_data)
            
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File encoding error. Please ensure the CSV file is UTF-8 encoded")
        except csv.Error as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV file: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")

    @staticmethod
    def _validate_csv_columns(csv_reader: csv.DictReader, required_columns: List[str]):
        """Validate CSV has required columns"""
        if not csv_reader.fieldnames:
            raise HTTPException(status_code=400, detail="CSV file appears to be empty or invalid")
        
        missing_columns = [col for col in required_columns if col not in csv_reader.fieldnames]
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {', '.join(missing_columns)}. Required columns are: {', '.join(required_columns)}"
            )

    @staticmethod
    def _extract_student_data(csv_reader: csv.DictReader) -> List[Dict[str, str]]:
        """Extract and validate student data from CSV"""
        csv_data = []
        for row_num, row in enumerate(csv_reader, start=2):
            # Skip rows with missing essential data
            if not row.get('className', '').strip() or not row.get('rollNumber', '').strip():
                continue
            
            csv_data.append({
                'className': row['className'].strip(),
                'rollNumber': row['rollNumber'].strip(),
                'studentName': row.get('studentName', '').strip() or None
            })
        return csv_data

    @staticmethod
    def _extract_room_data(csv_reader: csv.DictReader) -> List[Dict[str, Any]]:
        """Extract and validate room data from CSV"""
        csv_data = []
        for row_num, row in enumerate(csv_reader, start=2):
            # Skip rows with missing essential data
            if not row.get('roomNumber', '').strip() or not row.get('roomCapacity', '').strip():
                continue
            
            # Validate room capacity is a number
            try:
                capacity = int(row['roomCapacity'].strip())
                if capacity <= 0:
                    raise ValueError("Room capacity must be a positive number")
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid room capacity '{row['roomCapacity']}' in row {row_num}. Must be a positive number."
                )
            
            csv_data.append({
                'roomNumber': row['roomNumber'].strip(),
                'roomCapacity': capacity,
                'roomFloor': row.get('roomFloor', '').strip() or 'Not specified',
                'roomBuilding': row.get('roomBuilding', '').strip() or 'Not specified'
            })
        return csv_data

    @staticmethod
    def _process_student_classes(csv_data: List[Dict[str, str]]) -> Dict[str, Any]:
        """Process student classes and insert into database"""
        # Group by class name
        classes_data = {}
        for row in csv_data:
            class_name = row['className']
            if class_name not in classes_data:
                classes_data[class_name] = []
            classes_data[class_name].append(row)
        
        created_classes = []
        updated_classes = []
        errors = []
        total_students = 0
        
        with get_db_cursor() as cursor:
            for class_name, students_data in classes_data.items():
                try:
                    # Check if class already exists
                    cursor.execute("SELECT id FROM classes WHERE className = ?", (class_name,))
                    existing_class = cursor.fetchone()
                    
                    if existing_class:
                        class_id = existing_class[0]
                        updated_classes.append(class_name)
                    else:
                        # Create new class
                        cursor.execute("INSERT INTO classes (className) VALUES (?)", (class_name,))
                        class_id = cursor.lastrowid
                        created_classes.append(class_name)
                    
                    # Add students to the class
                    students_added = 0
                    students_skipped = 0
                    
                    for student_data in students_data:
                        roll_number = student_data['rollNumber']
                        student_name = student_data['studentName']
                        
                        try:
                            cursor.execute("""
                                INSERT INTO students (rollNumber, studentName, classId)
                                VALUES (?, ?, ?)
                            """, (roll_number, student_name, class_id))
                            students_added += 1
                            total_students += 1
                        except sqlite3.IntegrityError:
                            students_skipped += 1
                            errors.append(f"Student {roll_number} already exists in class {class_name}")
                    
                except Exception as e:
                    errors.append(f"Error processing class {class_name}: {str(e)}")
        
        return {
            "message": "CSV upload completed",
            "summary": {
                "total_students_processed": total_students,
                "classes_created": len(created_classes),
                "classes_updated": len(updated_classes),
                "errors_count": len(errors)
            },
            "details": {
                "created_classes": created_classes,
                "updated_classes": updated_classes,
                "errors": errors[:10]  # Limit errors to first 10
            }
        }

    @staticmethod
    def _process_exam_rooms(csv_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process exam rooms and insert into database"""
        rooms_added = 0
        rooms_skipped = 0
        errors = []
        
        with get_db_cursor() as cursor:
            for room_data in csv_data:
                try:
                    # Check if room already exists
                    cursor.execute("SELECT id FROM examRooms WHERE roomNumber = ?", (room_data['roomNumber'],))
                    existing_room = cursor.fetchone()
                    
                    if existing_room:
                        rooms_skipped += 1
                        errors.append(f"Room {room_data['roomNumber']} already exists")
                    else:
                        # Create new exam room
                        cursor.execute("""
                            INSERT INTO examRooms (roomNumber, roomCapacity, roomFloor, roomBuilding)
                            VALUES (?, ?, ?, ?)
                        """, (
                            room_data['roomNumber'],
                            room_data['roomCapacity'],
                            room_data['roomFloor'],
                            room_data['roomBuilding']
                        ))
                        rooms_added += 1
                    
                except sqlite3.IntegrityError as e:
                    rooms_skipped += 1
                    errors.append(f"Error adding room {room_data['roomNumber']}: {str(e)}")
                except Exception as e:
                    errors.append(f"Error processing room {room_data['roomNumber']}: {str(e)}")
        
        return {
            "message": "Exam rooms CSV upload completed",
            "summary": {
                "total_rooms_processed": len(csv_data),
                "rooms_added": rooms_added,
                "rooms_skipped": rooms_skipped,
                "errors_count": len(errors)
            },
            "details": {
                "errors": errors[:10]  # Limit errors to first 10
            }
        }

class CSVTemplates:
    @staticmethod
    def get_student_template() -> str:
        """Get student CSV template content"""
        return """className,rollNumber,studentName
Sample Class A,101,John Doe
Sample Class A,102,Jane Smith
Sample Class A,105,Bob Johnson
Sample Class B,201,Alice Brown
Sample Class B,203,Charlie Wilson"""

    @staticmethod
    def get_exam_room_template() -> str:
        """Get exam room CSV template content"""
        return """roomNumber,roomCapacity,roomFloor,roomBuilding
Room 101,30,Ground Floor,Main Building
Room 102,25,Ground Floor,Main Building
Room 201,35,First Floor,Main Building
Room 202,28,First Floor,Main Building
Lab A,20,Ground Floor,Science Building
Lab B,22,First Floor,Science Building"""
