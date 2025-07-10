import sqlite3
from typing import List, Dict, Tuple
from fastapi import HTTPException
from .database import get_db_cursor
from .config import settings
from .models import (
    ClassModel, ClassResponseModel, StudentModel, StudentResponseModel,
    ExamRoomModel, ExamRoomResponseModel, ScheduleRequest
)

class ClassService:
    @staticmethod
    def get_all_classes() -> List[ClassResponseModel]:
        with get_db_cursor() as cursor:
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
            
            return result

    @staticmethod
    def create_class(class_data: ClassModel) -> None:
        with get_db_cursor() as cursor:
            # Insert class
            cursor.execute("INSERT INTO classes (className) VALUES (?)", (class_data.className,))
            class_id = cursor.lastrowid
            
            # Insert students
            for student in class_data.students:
                cursor.execute("""
                    INSERT INTO students (rollNumber, studentName, classId)
                    VALUES (?, ?, ?)
                """, (student.rollNumber, student.studentName, class_id))

    @staticmethod
    def update_class(class_id: int, class_data: ClassModel) -> None:
        with get_db_cursor() as cursor:
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

    @staticmethod
    def delete_class(class_id: int) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Class not found")
            
            # Delete students first (due to foreign key constraint)
            cursor.execute("DELETE FROM students WHERE classId=?", (class_id,))
            cursor.execute("DELETE FROM classes WHERE id=?", (class_id,))

class StudentService:
    @staticmethod
    def get_students_by_class(class_id: int) -> List[StudentResponseModel]:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT id, rollNumber, studentName, classId FROM students WHERE classId = ?", (class_id,))
            students = cursor.fetchall()
            return [
                StudentResponseModel(
                    id=student[0],
                    rollNumber=student[1],
                    studentName=student[2],
                    classId=student[3]
                )
                for student in students
            ]

    @staticmethod
    def create_student(class_id: int, student_data: StudentModel) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Class not found")
            
            try:
                cursor.execute("""
                    INSERT INTO students (rollNumber, studentName, classId)
                    VALUES (?, ?, ?)
                """, (student_data.rollNumber, student_data.studentName, class_id))
            except sqlite3.IntegrityError:
                raise HTTPException(status_code=400, detail="Student with this roll number already exists in this class")

    @staticmethod
    def delete_student(student_id: int) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Student not found")
            
            cursor.execute("DELETE FROM students WHERE id=?", (student_id,))

class ExamRoomService:
    @staticmethod
    def get_all_exam_rooms() -> List[ExamRoomResponseModel]:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM examRooms")
            exam_rooms = cursor.fetchall()
            return [
                ExamRoomResponseModel(
                    id=row[0],
                    roomNumber=row[1],
                    roomCapacity=row[2],
                    roomFloor=row[3],
                    roomBuilding=row[4]
                )
                for row in exam_rooms
            ]

    @staticmethod
    def create_exam_room(room_data: ExamRoomModel) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO examRooms (roomNumber, roomCapacity, roomFloor, roomBuilding)
                VALUES (?, ?, ?, ?)
            """, (room_data.roomNumber, room_data.roomCapacity, room_data.roomFloor, room_data.roomBuilding))

    @staticmethod
    def update_exam_room(room_id: int, room_data: ExamRoomModel) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM examRooms WHERE id=?", (room_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Exam room not found")
            
            cursor.execute("""
                UPDATE examRooms 
                SET roomNumber=?, roomCapacity=?, roomFloor=?, roomBuilding=?
                WHERE id=?
            """, (room_data.roomNumber, room_data.roomCapacity, room_data.roomFloor, room_data.roomBuilding, room_id))

    @staticmethod
    def delete_exam_room(room_id: int) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM examRooms WHERE id=?", (room_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Exam room not found")
            
            cursor.execute("DELETE FROM examRooms WHERE id=?", (room_id,))

class ScheduleService:
    @staticmethod
    def schedule_exam(data: ScheduleRequest) -> Dict[str, any]:
        max_students_per_class = settings.MAX_STUDENTS_PER_CLASS_PER_ROOM
        
        with get_db_cursor() as cursor:
            # Fetch students for selected classes
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
                        "class_counts": {}
                    })

            # Calculate total capacity
            total_capacity = sum(room["capacity"] for room in rooms)
            if total_capacity < len(all_students):
                raise HTTPException(status_code=400, detail="Not enough capacity in selected rooms for all students")

            # Place students in rooms
            ScheduleService._place_students_in_rooms(all_students, rooms, data.split, max_students_per_class)

            # Build response
            seating_arrangement = {}
            for room in rooms:
                seating_arrangement[room["roomNumber"]] = room["students"]

            return {"date": data.date, "seating_arrangement": seating_arrangement}

    @staticmethod
    def _place_students_in_rooms(all_students: List[Tuple[str, int]], rooms: List[Dict], split: bool, max_per_class: int):
        """Place students in rooms with class distribution logic"""
        if split and len(rooms) > 1:
            # Place students in rooms with class distribution
            for student_roll, class_id in all_students:
                placed = False
                
                # First try rooms where this class has fewer than max students
                for room in rooms:
                    class_count = room["class_counts"].get(class_id, 0)
                    if (len(room["students"]) < room["capacity"] and 
                        class_count < max_per_class):
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
                
                # Try to place in a room where the class has fewer than max students
                for room in rooms:
                    if len(room["students"]) < room["capacity"]:
                        class_count = room["class_counts"].get(class_id, 0)
                        if class_count < max_per_class:
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
