from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List
import sqlite3

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
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    className TEXT NOT NULL,
    startRollNumber INTEGER NOT NULL,
    endRollNumber INTEGER NOT NULL
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

class ClassModel(BaseModel):
    className: str
    startRollNumber: int
    endRollNumber: int

class ClassResponseModel(ClassModel):
    id: int
    

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
    result = [
        ClassResponseModel(
            id=row[0],
            className=row[1],
            startRollNumber=row[2],
            endRollNumber=row[3]
        )
        for row in classes
    ]
    return {"classes": result}

@app.post("/class")
def add_class(class_data: ClassModel):
    cursor.execute("""
        INSERT INTO classes (className, startRollNumber, endRollNumber)
        VALUES (?, ?, ?)
    """, (class_data.className, class_data.startRollNumber, class_data.endRollNumber))
    conn.commit()
    return {"message": "Class added successfully"}

@app.put("/class/{class_id}")
def update_class(class_id: int, class_data: ClassModel):
    cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Class not found")
    
    cursor.execute("""
        UPDATE classes 
        SET className=?, startRollNumber=?, endRollNumber=?
        WHERE id=?
    """, (class_data.className, class_data.startRollNumber, class_data.endRollNumber, class_id))
    conn.commit()
    return {"message": "Class updated successfully"}

@app.delete("/class/{class_id}")
def delete_class(class_id: int):
    cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Class not found")
    
    cursor.execute("DELETE FROM classes WHERE id=?", (class_id,))
    conn.commit()
    return {"message": "Class deleted successfully"}


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
        cursor.execute("SELECT id, className, startRollNumber, endRollNumber FROM classes WHERE id = ?", (class_id,))
        result = cursor.fetchone()
        if result:
            class_id, class_name, start, end = result
            class_students = list(range(start, end + 1))
            students_by_class[class_id] = class_students
            all_students.extend(class_students)

    all_students.sort()  # Keep all roll numbers sorted

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
        # Create a list of students with their class IDs for tracking
        student_class_map = []
        for class_id, students in students_by_class.items():
            for student in students:
                student_class_map.append((student, class_id))
        
        # Sort by student ID (roll number)
        student_class_map.sort(key=lambda x: x[0])
        
        # Place students in rooms
        for student, class_id in student_class_map:
            # Find a suitable room for this student
            placed = False
            
            # First try rooms where this class has fewer than MAX_STUDENTS_PER_CLASS students
            for room in rooms:
                class_count = room["class_counts"].get(class_id, 0)
                if (len(room["students"]) < room["capacity"] and 
                    class_count < MAX_STUDENTS_PER_CLASS):
                    room["students"].append(student)
                    room["class_counts"][class_id] = class_count + 1
                    placed = True
                    break
            
            # If no room has space under the class limit, try any room with capacity
            if not placed:
                for room in rooms:
                    if len(room["students"]) < room["capacity"]:
                        room["students"].append(student)
                        class_count = room["class_counts"].get(class_id, 0)
                        room["class_counts"][class_id] = class_count + 1
                        placed = True
                        break
            
            if not placed:
                raise HTTPException(status_code=500, detail="Failed to place all students despite sufficient capacity")
    else:
        # For non-split option, still respect the class size limit if possible
        student_class_map = []
        for class_id, students in students_by_class.items():
            for student in students:
                student_class_map.append((student, class_id))
        
        student_class_map.sort(key=lambda x: x[0])
        
        for student, class_id in student_class_map:
            placed = False
            
            # Try to place in a room where the class has fewer than MAX_STUDENTS_PER_CLASS students
            for room in rooms:
                if len(room["students"]) < room["capacity"]:
                    class_count = room["class_counts"].get(class_id, 0)
                    if class_count < MAX_STUDENTS_PER_CLASS:
                        room["students"].append(student)
                        room["class_counts"][class_id] = class_count + 1
                        placed = True
                        break
            
            # If no room has space under the class limit, try any room with capacity
            if not placed:
                for room in rooms:
                    if len(room["students"]) < room["capacity"]:
                        room["students"].append(student)
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