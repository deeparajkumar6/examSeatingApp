from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import csv
import io

app = FastAPI()

#enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# SQLite3 database setup
conn = sqlite3.connect("database_new.db", check_same_thread=False)
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


# ---------- Pydantic Models ----------

class StudentModel(BaseModel):
    rollNumber: str
    studentName: Optional[str] = None

class StudentResponseModel(StudentModel):
    id: int
    classId: int

class ClassModel(BaseModel):
    className: str
    students: List[StudentModel] = []

class ClassResponseModel(BaseModel):
    id: int
    className: str
    students: List[StudentResponseModel] = []

class ExamRoomModel(BaseModel):
    roomNumber: str
    roomCapacity: int
    roomFloor: str
    roomBuilding: str

class ExamRoomResponseModel(ExamRoomModel):
    id: int

class ScheduleRequest(BaseModel):
    date: str
    classes: List[int]
    exam_rooms: List[int]
    split: bool

# --------- /class Endpoints ---------

@app.get("/class", response_model=dict)
def get_classes():
    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()
    result = []
    
    for class_row in classes:
        class_id, class_name = class_row
        
        # Get students for this class
        cursor.execute("SELECT id, rollNumber, studentName, classId FROM students WHERE classId = ?", (class_id,))
        students = cursor.fetchall()
        
        student_list = [
            StudentResponseModel(
                id=student[0],
                rollNumber=student[1],
                studentName=student[2],
                classId=student[3]
            )
            for student in students
        ]
        
        result.append(ClassResponseModel(
            id=class_id,
            className=class_name,
            students=student_list
        ))
    
    return {"classes": result}

@app.post("/class")
def add_class(class_data: ClassModel):
    # Insert class
    cursor.execute("INSERT INTO classes (className) VALUES (?)", (class_data.className,))
    class_id = cursor.lastrowid
    
    # Insert students
    for student in class_data.students:
        cursor.execute("""
            INSERT INTO students (rollNumber, studentName, classId)
            VALUES (?, ?, ?)
        """, (student.rollNumber, student.studentName, class_id))
    
    conn.commit()
    return {"message": "Class added successfully"}

@app.put("/class/{class_id}")
def update_class(class_id: int, class_data: ClassModel):
    cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Update class name
    cursor.execute("UPDATE classes SET className=? WHERE id=?", (class_data.className, class_id))
    
    # Delete existing students for this class
    cursor.execute("DELETE FROM students WHERE classId=?", (class_id,))
    
    # Insert new students
    for student in class_data.students:
        cursor.execute("""
            INSERT INTO students (rollNumber, studentName, classId)
            VALUES (?, ?, ?)
        """, (student.rollNumber, student.studentName, class_id))
    
    conn.commit()
    return {"message": "Class updated successfully"}

@app.delete("/class/{class_id}")
def delete_class(class_id: int):
    cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Delete students first (due to foreign key constraint)
    cursor.execute("DELETE FROM students WHERE classId=?", (class_id,))
    cursor.execute("DELETE FROM classes WHERE id=?", (class_id,))
    conn.commit()
    return {"message": "Class deleted successfully"}

# --------- /student Endpoints ---------

@app.get("/student/{class_id}", response_model=dict)
def get_students_by_class(class_id: int):
    cursor.execute("SELECT id, rollNumber, studentName, classId FROM students WHERE classId = ?", (class_id,))
    students = cursor.fetchall()
    result = [
        StudentResponseModel(
            id=student[0],
            rollNumber=student[1],
            studentName=student[2],
            classId=student[3]
        )
        for student in students
    ]
    return {"students": result}

@app.post("/student/{class_id}")
def add_student(class_id: int, student_data: StudentModel):
    cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Class not found")
    
    try:
        cursor.execute("""
            INSERT INTO students (rollNumber, studentName, classId)
            VALUES (?, ?, ?)
        """, (student_data.rollNumber, student_data.studentName, class_id))
        conn.commit()
        return {"message": "Student added successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Student with this roll number already exists in this class")

@app.delete("/student/{student_id}")
def delete_student(student_id: int):
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    return {"message": "Student deleted successfully"}

# --------- CSV Upload Endpoint ---------

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload CSV file with columns: className, rollNumber, studentName
    Creates classes and students from the CSV data
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    try:
        # Read CSV content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Parse CSV using built-in csv module
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        # Validate required columns
        required_columns = ['className', 'rollNumber', 'studentName']
        if not csv_reader.fieldnames:
            raise HTTPException(status_code=400, detail="CSV file appears to be empty or invalid")
        
        missing_columns = [col for col in required_columns if col not in csv_reader.fieldnames]
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {', '.join(missing_columns)}. Required columns are: className, rollNumber, studentName"
            )
        
        # Process CSV data
        csv_data = []
        for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 because row 1 is headers
            # Skip rows with missing essential data
            if not row.get('className', '').strip() or not row.get('rollNumber', '').strip():
                continue
            
            csv_data.append({
                'className': row['className'].strip(),
                'rollNumber': row['rollNumber'].strip(),
                'studentName': row.get('studentName', '').strip() or None
            })
        
        if not csv_data:
            raise HTTPException(status_code=400, detail="No valid data found in CSV file")
        
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
                        # Student with this roll number already exists in this class
                        students_skipped += 1
                        errors.append(f"Student {roll_number} already exists in class {class_name}")
                
                print(f"Class {class_name}: {students_added} students added, {students_skipped} skipped")
                
            except Exception as e:
                errors.append(f"Error processing class {class_name}: {str(e)}")
        
        conn.commit()
        
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
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding error. Please ensure the CSV file is UTF-8 encoded")
    except csv.Error as e:
        raise HTTPException(status_code=400, detail=f"Error parsing CSV file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")

@app.get("/download-csv-template")
def download_csv_template():
    """
    Download a CSV template file for bulk student upload
    """
    from fastapi.responses import Response
    
    template_content = """className,rollNumber,studentName
Sample Class A,101,John Doe
Sample Class A,102,Jane Smith
Sample Class A,105,Bob Johnson
Sample Class B,201,Alice Brown
Sample Class B,203,Charlie Wilson"""
    
    return Response(
        content=template_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=student_upload_template.csv"}
    )

# --------- Exam Room CSV Upload Endpoint ---------

@app.post("/upload-exam-rooms-csv")
async def upload_exam_rooms_csv(file: UploadFile = File(...)):
    """
    Upload CSV file with columns: roomNumber, roomCapacity, roomFloor, roomBuilding
    Creates exam rooms from the CSV data
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    try:
        # Read CSV content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Parse CSV using built-in csv module
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        # Validate required columns
        required_columns = ['roomNumber', 'roomCapacity', 'roomFloor', 'roomBuilding']
        if not csv_reader.fieldnames:
            raise HTTPException(status_code=400, detail="CSV file appears to be empty or invalid")
        
        missing_columns = [col for col in required_columns if col not in csv_reader.fieldnames]
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {', '.join(missing_columns)}. Required columns are: roomNumber, roomCapacity, roomFloor, roomBuilding"
            )
        
        # Process CSV data
        csv_data = []
        for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 because row 1 is headers
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
        
        if not csv_data:
            raise HTTPException(status_code=400, detail="No valid data found in CSV file")
        
        rooms_added = 0
        rooms_skipped = 0
        errors = []
        
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
        
        conn.commit()
        
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
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding error. Please ensure the CSV file is UTF-8 encoded")
    except csv.Error as e:
        raise HTTPException(status_code=400, detail=f"Error parsing CSV file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")

@app.get("/download-exam-rooms-csv-template")
def download_exam_rooms_csv_template():
    """
    Download a CSV template file for bulk exam room upload
    """
    from fastapi.responses import Response
    
    template_content = """roomNumber,roomCapacity,roomFloor,roomBuilding
Room 101,30,Ground Floor,Main Building
Room 102,25,Ground Floor,Main Building
Room 201,35,First Floor,Main Building
Room 202,28,First Floor,Main Building
Lab A,20,Ground Floor,Science Building
Lab B,22,First Floor,Science Building"""
    
    return Response(
        content=template_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=exam_rooms_upload_template.csv"}
    )

# --------- /examRoom Endpoints ---------

@app.get("/examRoom", response_model=dict)
def get_exam_rooms():
    cursor.execute("SELECT * FROM examRooms")
    exam_rooms = cursor.fetchall()
    result = [
        ExamRoomResponseModel(
            id=row[0],
            roomNumber=row[1],
            roomCapacity=row[2],
            roomFloor=row[3],
            roomBuilding=row[4]
        )
        for row in exam_rooms
    ]
    return {"examRooms": result}


@app.post("/examRoom")
def add_exam_room(room_data: ExamRoomModel):
    cursor.execute("""
        INSERT INTO examRooms (roomNumber, roomCapacity, roomFloor, roomBuilding)
        VALUES (?, ?, ?, ?)
    """, (room_data.roomNumber, room_data.roomCapacity, room_data.roomFloor, room_data.roomBuilding))
    conn.commit()
    return {"message": "Exam room added successfully"}

@app.put("/examRoom/{room_id}")
def update_exam_room(room_id: int, room_data: ExamRoomModel):
    cursor.execute("SELECT * FROM examRooms WHERE id=?", (room_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Exam room not found")
    
    cursor.execute("""
        UPDATE examRooms 
        SET roomNumber=?, roomCapacity=?, roomFloor=?, roomBuilding=?
        WHERE id=?
    """, (room_data.roomNumber, room_data.roomCapacity, room_data.roomFloor, room_data.roomBuilding, room_id))
    conn.commit()
    return {"message": "Exam room updated successfully"}

@app.delete("/examRoom/{room_id}")
def delete_exam_room(room_id: int):
    cursor.execute("SELECT * FROM examRooms WHERE id=?", (room_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Exam room not found")
    
    cursor.execute("DELETE FROM examRooms WHERE id=?", (room_id,))
    conn.commit()
    return {"message": "Exam room deleted successfully"}

# --------- /schedule Endpoints ---------
@app.post("/schedule")
def schedule_exam(data: ScheduleRequest):
    # Fetch students for selected classes - keep track of which class each student belongs to
    students_by_class = {}
    all_students = []
    
    for class_id in data.classes:
        cursor.execute("SELECT className FROM classes WHERE id = ?", (class_id,))
        class_result = cursor.fetchone()
        if class_result:
            cursor.execute("SELECT rollNumber FROM students WHERE classId = ? ORDER BY rollNumber", (class_id,))
            student_results = cursor.fetchall()
            class_students = [row[0] for row in student_results]
            students_by_class[class_id] = class_students
            all_students.extend([(student, class_id) for student in class_students])

    # Sort all students by roll number
    all_students.sort(key=lambda x: x[0])

    # Fetch room details
    rooms = []
    for room_id in data.exam_rooms:
        cursor.execute("SELECT roomNumber, roomCapacity FROM examRooms WHERE id = ?", (room_id,))
        result = cursor.fetchone()
        if result:
            rooms.append({
                "roomNumber": result[0],
                "capacity": result[1],
                "students": [],
                "class_counts": {}  # Track how many students from each class
            })

    # Calculate total capacity
    total_capacity = sum(room["capacity"] for room in rooms)
    if total_capacity < len(all_students):
        raise HTTPException(status_code=400, detail="Not enough capacity in selected rooms for all students")

    # Max students from same class per room
    MAX_STUDENTS_PER_CLASS = 20

    if data.split and len(rooms) > 1:
        # Place students in rooms with class distribution
        for student_roll, class_id in all_students:
            # Find a suitable room for this student
            placed = False
            
            # First try rooms where this class has fewer than MAX_STUDENTS_PER_CLASS students
            for room in rooms:
                class_count = room["class_counts"].get(class_id, 0)
                if (len(room["students"]) < room["capacity"] and 
                    class_count < MAX_STUDENTS_PER_CLASS):
                    room["students"].append(student_roll)
                    room["class_counts"][class_id] = class_count + 1
                    placed = True
                    break
            
            # If no room has space under the class limit, try any room with capacity
            if not placed:
                for room in rooms:
                    if len(room["students"]) < room["capacity"]:
                        room["students"].append(student_roll)
                        class_count = room["class_counts"].get(class_id, 0)
                        room["class_counts"][class_id] = class_count + 1
                        placed = True
                        break
            
            if not placed:
                raise HTTPException(status_code=500, detail="Failed to place all students despite sufficient capacity")
    else:
        # For non-split option, still respect the class size limit if possible
        for student_roll, class_id in all_students:
            placed = False
            
            # Try to place in a room where the class has fewer than MAX_STUDENTS_PER_CLASS students
            for room in rooms:
                if len(room["students"]) < room["capacity"]:
                    class_count = room["class_counts"].get(class_id, 0)
                    if class_count < MAX_STUDENTS_PER_CLASS:
                        room["students"].append(student_roll)
                        room["class_counts"][class_id] = class_count + 1
                        placed = True
                        break
            
            # If no room has space under the class limit, try any room with capacity
            if not placed:
                for room in rooms:
                    if len(room["students"]) < room["capacity"]:
                        room["students"].append(student_roll)
                        class_count = room["class_counts"].get(class_id, 0)
                        room["class_counts"][class_id] = class_count + 1
                        placed = True
                        break
            
            if not placed:
                raise HTTPException(status_code=500, detail="Failed to place all students despite sufficient capacity")

    # Build response
    seating_arrangement = {}
    for room in rooms:
        # Remove the class_counts from the response
        seating_arrangement[room["roomNumber"]] = room["students"]

    return {"date": data.date, "seating_arrangement": seating_arrangement}
