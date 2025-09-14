import sqlite3
from typing import List, Dict, Tuple
from fastapi import HTTPException
from .database import get_db_cursor
from .config import settings
from .models import (
    ClassModel,
    ClassResponseModel,
    StudentModel,
    StudentResponseModel,
    ExamRoomModel,
    ExamRoomResponseModel,
    ScheduleRequest,
    BulkImportResponse,
)
from .excel_utils import ExcelParser, ExcelValidator


class ClassService:
    @staticmethod
    def get_all_classes() -> List[ClassResponseModel]:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM classes")
            classes = cursor.fetchall()
            result = []

            for class_row in classes:
                # Handle both old and new schema
                if len(class_row) == 2:
                    class_id, class_name = class_row
                    shift = None
                else:
                    class_id, class_name, shift = class_row

                # Get students for this class
                cursor.execute(
                    "SELECT id, rollNumber, studentName, classId, language, dateOfBirth FROM students WHERE classId = ?",
                    (class_id,),
                )
                students = cursor.fetchall()

                student_list = []
                for student in students:
                    # Handle both old and new schema
                    if len(student) == 4:
                        student_id, roll_num, name, class_id = student
                        language = None
                        date_of_birth = None
                    else:
                        (
                            student_id,
                            roll_num,
                            name,
                            class_id,
                            language,
                            date_of_birth,
                        ) = student

                    student_list.append(
                        StudentResponseModel(
                            id=student_id,
                            rollNumber=roll_num,
                            studentName=name,
                            classId=class_id,
                            language=language,
                            dateOfBirth=date_of_birth,
                        )
                    )

                result.append(
                    ClassResponseModel(
                        id=class_id,
                        className=class_name,
                        shift=shift,
                        students=student_list,
                    )
                )

            return result

    @staticmethod
    def create_class(class_data: ClassModel) -> None:
        # Validate that shift is provided and not empty
        if not class_data.shift or not class_data.shift.strip():
            raise HTTPException(
                status_code=400, detail="Shift is required and cannot be empty"
            )

        with get_db_cursor() as cursor:
            # Insert class
            cursor.execute(
                "INSERT INTO classes (className, shift) VALUES (?, ?)",
                (class_data.className, class_data.shift.strip()),
            )
            class_id = cursor.lastrowid

            # Insert students
            for index, student in enumerate(class_data.students):
                # Generate rollNumber if not provided
                roll_number = student.rollNumber
                if not roll_number:
                    # Generate a simple roll number based on class_id and student index
                    roll_number = f"STU{class_id:03d}{index+1:03d}"

                cursor.execute(
                    """
                    INSERT INTO students (rollNumber, studentName, language, dateOfBirth, classId)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        roll_number,
                        student.studentName,
                        student.language,
                        student.dateOfBirth,
                        class_id,
                    ),
                )

    @staticmethod
    def update_class(class_id: int, class_data: ClassModel) -> None:
        # Validate that shift is provided and not empty
        if not class_data.shift or not class_data.shift.strip():
            raise HTTPException(
                status_code=400, detail="Shift is required and cannot be empty"
            )

        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Class not found")

            # Update class name and shift
            cursor.execute(
                "UPDATE classes SET className=?, shift=? WHERE id=?",
                (class_data.className, class_data.shift.strip(), class_id),
            )

            # Delete existing students for this class
            cursor.execute("DELETE FROM students WHERE classId=?", (class_id,))

            # Insert new students
            for index, student in enumerate(class_data.students):
                # Generate rollNumber if not provided
                roll_number = student.rollNumber
                if not roll_number:
                    # Generate a simple roll number based on class_id and student index
                    roll_number = f"STU{class_id:03d}{index+1:03d}"

                cursor.execute(
                    """
                    INSERT INTO students (rollNumber, studentName, language, dateOfBirth, classId)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        roll_number,
                        student.studentName,
                        student.language,
                        student.dateOfBirth,
                        class_id,
                    ),
                )

    @staticmethod
    def delete_class(class_id: int) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Class not found")

            # Delete students first (due to foreign key constraint)
            cursor.execute("DELETE FROM students WHERE classId=?", (class_id,))
            cursor.execute("DELETE FROM classes WHERE id=?", (class_id,))

    @staticmethod
    def bulk_import_from_excel(file_content: bytes, filename: str = "Unknown") -> BulkImportResponse:
        """Bulk import classes and students from Excel file"""
        try:
            # Parse Excel file
            parsed_data = ExcelParser.parse_student_excel(file_content, filename)

            # Validate parsed data
            validation_errors = ExcelValidator.validate_parsed_data(parsed_data)
            if validation_errors:
                raise HTTPException(
                    status_code=400,
                    detail=f"Validation errors: {'; '.join(validation_errors)}",
                )

            classes_created = 0
            students_created = 0
            details = []

            with get_db_cursor() as cursor:
                for class_data in parsed_data["classes"]:
                    class_name = class_data["class_name"]
                    shift = class_data["shift"]
                    students = class_data["students"]

                    # Validate shift is not empty
                    if not shift or not shift.strip():
                        raise HTTPException(
                            status_code=400,
                            detail=f"Shift is required for class {class_name}",
                        )

                    # Check if class already exists
                    cursor.execute(
                        "SELECT id FROM classes WHERE className = ? AND shift = ?",
                        (class_name, shift.strip()),
                    )
                    existing_class = cursor.fetchone()

                    if existing_class:
                        class_id = existing_class[0]
                        # Update existing class - delete old students and add new ones
                        cursor.execute(
                            "DELETE FROM students WHERE classId = ?", (class_id,)
                        )
                        action = "updated"
                    else:
                        # Create new class
                        cursor.execute(
                            "INSERT INTO classes (className, shift) VALUES (?, ?)",
                            (class_name, shift.strip()),
                        )
                        class_id = cursor.lastrowid
                        classes_created += 1
                        action = "created"

                    # Add students to the class
                    class_students_added = 0
                    for student in students:
                        try:
                            cursor.execute(
                                """
                                INSERT INTO students (rollNumber, studentName, language, dateOfBirth, classId)
                                VALUES (?, ?, ?, ?, ?)
                            """,
                                (
                                    student["register_number"],
                                    student["name"],
                                    student["language"],
                                    student["date_of_birth"],
                                    class_id,
                                ),
                            )
                            class_students_added += 1
                            students_created += 1
                        except sqlite3.IntegrityError as e:
                            # Handle duplicate register numbers
                            print(
                                f"Skipping duplicate student {student['register_number']}: {e}"
                            )

                    details.append(
                        {
                            "className": class_name,
                            "shift": shift.strip(),
                            "action": action,
                            "studentsAdded": class_students_added,
                        }
                    )

            return BulkImportResponse(
                message=f"Successfully imported {classes_created} classes with {students_created} students",
                classesCreated=classes_created,
                studentsCreated=students_created,
                details=details,
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during bulk import: {str(e)}"
            )


    @staticmethod
    def selective_import_from_excel(file_content: bytes, selected_class_identifiers: List[dict], filename: str = "Unknown") -> BulkImportResponse:
        """Import only selected classes from Excel file"""
        try:
            # Parse Excel file
            parsed_data = ExcelParser.parse_student_excel(file_content, filename)
            
            # Filter only selected classes by matching class_name and shift
            all_classes = parsed_data["classes"]
            selected_classes = []
            
            for class_data in all_classes:
                for selected in selected_class_identifiers:
                    if (class_data["class_name"] == selected["class_name"] and 
                        class_data["shift"] == selected["shift"]):
                        selected_classes.append(class_data)
                        break
            
            if not selected_classes:
                raise HTTPException(status_code=400, detail="No valid classes selected for import")
            
            classes_created = 0
            students_created = 0
            details = []
            
            with get_db_cursor() as cursor:
                for class_data in selected_classes:
                    class_name = class_data["class_name"]
                    shift = class_data["shift"]
                    students = class_data["students"]
                    
                    # Check if class already exists
                    cursor.execute("SELECT id FROM classes WHERE className = ? AND shift = ?", (class_name, shift.strip()))
                    existing_class = cursor.fetchone()
                    
                    if existing_class:
                        class_id = existing_class[0]
                        cursor.execute("DELETE FROM students WHERE classId = ?", (class_id,))
                        action = "updated"
                    else:
                        cursor.execute("INSERT INTO classes (className, shift) VALUES (?, ?)", (class_name, shift.strip()))
                        class_id = cursor.lastrowid
                        classes_created += 1
                        action = "created"
                    
                    # Add students
                    class_students_added = 0
                    for student in students:
                        try:
                            cursor.execute("INSERT INTO students (rollNumber, studentName, language, dateOfBirth, classId) VALUES (?, ?, ?, ?, ?)", (student["register_number"], student["name"], student["language"], student["date_of_birth"], class_id))
                            class_students_added += 1
                            students_created += 1
                        except sqlite3.IntegrityError:
                            pass
                    
                    details.append({"className": class_name, "shift": shift.strip(), "action": action, "studentsAdded": class_students_added})
            
            return BulkImportResponse(message=f"Successfully imported {len(selected_classes)} selected classes with {students_created} students", classesCreated=classes_created, studentsCreated=students_created, details=details)
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during selective import: {str(e)}")

class StudentService:
    @staticmethod
    def get_students_by_class(class_id: int) -> List[StudentResponseModel]:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT id, rollNumber, studentName, classId, language, dateOfBirth FROM students WHERE classId = ?",
                (class_id,),
            )
            students = cursor.fetchall()

            student_list = []
            for student in students:
                # Handle both old and new schema
                if len(student) == 4:
                    student_id, roll_num, name, class_id = student
                    language = None
                    date_of_birth = None
                else:
                    (
                        student_id,
                        roll_num,
                        name,
                        class_id,
                        language,
                        date_of_birth,
                    ) = student

                student_list.append(
                    StudentResponseModel(
                        id=student_id,
                        rollNumber=roll_num,
                        studentName=name,
                        classId=class_id,
                        language=language,
                        dateOfBirth=date_of_birth,
                    )
                )

            return student_list

    @staticmethod
    def create_student(class_id: int, student_data: StudentModel) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM classes WHERE id=?", (class_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Class not found")

            # Generate rollNumber if not provided
            roll_number = student_data.rollNumber
            if not roll_number:
                # Get the count of existing students in this class to generate unique roll number
                cursor.execute(
                    "SELECT COUNT(*) FROM students WHERE classId=?", (class_id,)
                )
                student_count = cursor.fetchone()[0]
                roll_number = f"STU{class_id:03d}{student_count+1:03d}"

            try:
                cursor.execute(
                    """
                    INSERT INTO students (rollNumber, studentName, language, dateOfBirth, classId)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        roll_number,
                        student_data.studentName,
                        student_data.language,
                        student_data.dateOfBirth,
                        class_id,
                    ),
                )
            except sqlite3.IntegrityError:
                raise HTTPException(
                    status_code=400,
                    detail="Student with this roll number already exists in this class",
                )

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
                    roomBuilding=row[4],
                )
                for row in exam_rooms
            ]

    @staticmethod
    def create_exam_room(room_data: ExamRoomModel) -> None:
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO examRooms (roomNumber, roomCapacity, roomFloor, roomBuilding)
                VALUES (?, ?, ?, ?)
            """,
                (
                    room_data.roomNumber,
                    room_data.roomCapacity,
                    room_data.roomFloor,
                    room_data.roomBuilding,
                ),
            )

    @staticmethod
    def update_exam_room(room_id: int, room_data: ExamRoomModel) -> None:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM examRooms WHERE id=?", (room_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Exam room not found")

            cursor.execute(
                """
                UPDATE examRooms 
                SET roomNumber=?, roomCapacity=?, roomFloor=?, roomBuilding=?
                WHERE id=?
            """,
                (
                    room_data.roomNumber,
                    room_data.roomCapacity,
                    room_data.roomFloor,
                    room_data.roomBuilding,
                    room_id,
                ),
            )

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
            # Fetch class information including shift
            class_info = {}
            for class_id in data.classes:
                cursor.execute(
                    "SELECT className, shift FROM classes WHERE id = ?", (class_id,)
                )
                class_result = cursor.fetchone()
                if class_result:
                    class_name, shift = class_result
                    # Create display name with shift for PDF
                    display_name = f"{class_name} - {shift}" if shift else class_name
                    class_info[class_id] = {
                        "name": class_name,
                        "shift": shift,
                        "display_name": display_name,
                    }

            # Fetch students for selected classes
            students_by_class = {}
            all_students = []

            for class_id in data.classes:
                if class_id in class_info:
                    # Check if language selections are specified for this class
                    selected_languages = None
                    if (
                        hasattr(data, "language_selections")
                        and data.language_selections
                        and class_id in data.language_selections
                    ):
                        selected_languages = data.language_selections[class_id]
                        # If empty array is provided, treat as no filtering (include all students)
                        if (
                            isinstance(selected_languages, list)
                            and len(selected_languages) == 0
                        ):
                            selected_languages = None
                    # If class is not in language_selections dict, no filtering is applied (selected_languages remains None)

                    cursor.execute(
                        "SELECT rollNumber, studentName, language FROM students WHERE classId = ? ORDER BY rollNumber",
                        (class_id,),
                    )
                    student_results = cursor.fetchall()

                    class_students = []
                    for row in student_results:
                        roll_number = row[0]
                        student_name = row[1] if len(row) > 1 else None
                        language = row[2] if len(row) > 2 else None

                        # Filter by language if specified
                        if selected_languages:
                            if language and language not in selected_languages:
                                continue  # Skip students with non-matching languages
                            if not language and None not in selected_languages:
                                continue  # Skip students without language if not explicitly included

                        student_data = {
                            "rollNumber": roll_number,
                            "studentName": student_name,
                            "language": language,
                            "classId": class_id,
                            "className": class_info[class_id]["display_name"],
                        }
                        class_students.append(student_data)

                    students_by_class[class_id] = class_students
                    # Add to all_students list with new format
                    all_students.extend(class_students)

            # Sort all students by roll number
            all_students.sort(key=lambda x: x["rollNumber"])

            # Fetch room details
            rooms = []
            for room_id in data.exam_rooms:
                cursor.execute(
                    "SELECT roomNumber, roomCapacity FROM examRooms WHERE id = ?",
                    (room_id,),
                )
                result = cursor.fetchone()
                if result:
                    rooms.append(
                        {
                            "roomNumber": result[0],
                            "capacity": result[1],
                            "students": [],
                            "class_counts": {},
                            "class_info": {},  # Store class information for each room
                        }
                    )

            # Calculate total capacity
            total_capacity = sum(room["capacity"] for room in rooms)
            if total_capacity < len(all_students):
                raise HTTPException(
                    status_code=400,
                    detail="Not enough capacity in selected rooms for all students",
                )

            # Place students in rooms with class information
            ScheduleService._place_students_in_rooms_with_student_info(
                all_students, rooms, data.split, max_students_per_class
            )

            # Build response with class and language information
            seating_arrangement = {}
            class_summary = {}
            language_summary = {}

            for room in rooms:
                # Students already have complete information including language
                seating_arrangement[room["roomNumber"]] = room["students"]

                # Create class summary for this room
                class_summary[room["roomNumber"]] = room.get("class_info", {})

                # Create language summary for this room
                room_language_summary = {}
                for student in room["students"]:
                    language = student.get("language")
                    # Handle None or empty language values
                    if not language:
                        language = "No Language"
                    if language not in room_language_summary:
                        room_language_summary[language] = 0
                    room_language_summary[language] += 1
                language_summary[room["roomNumber"]] = room_language_summary

            return {
                "date": data.date,
                "seating_arrangement": seating_arrangement,
                "class_summary": class_summary,
                "class_info": class_info,
                "language_summary": language_summary,
            }

    @staticmethod
    def _place_students_in_rooms_with_student_info(
        all_students: List[Dict], rooms: List[Dict], split: bool, max_per_class: int
    ):
        """Place students in rooms with class distribution logic and include student information"""
        if split and len(rooms) > 1:
            # Place students in rooms with class distribution
            for student_data in all_students:
                placed = False
                class_id = student_data["classId"]

                # First try rooms where this class has fewer than max students
                for room in rooms:
                    class_count = room["class_counts"].get(class_id, 0)
                    if (
                        len(room["students"]) < room["capacity"]
                        and class_count < max_per_class
                    ):
                        # Add student with complete information
                        room["students"].append(student_data)
                        room["class_counts"][class_id] = class_count + 1

                        # Update class info for the room
                        class_display_name = student_data["className"]
                        if class_display_name not in room["class_info"]:
                            room["class_info"][class_display_name] = 0
                        room["class_info"][class_display_name] += 1

                        placed = True
                        break

                # If no room has space under the class limit, try any room with capacity
                if not placed:
                    for room in rooms:
                        if len(room["students"]) < room["capacity"]:
                            room["students"].append(student_data)
                            class_count = room["class_counts"].get(class_id, 0)
                            room["class_counts"][class_id] = class_count + 1

                            # Update class info for the room
                            class_display_name = student_data["className"]
                            if class_display_name not in room["class_info"]:
                                room["class_info"][class_display_name] = 0
                            room["class_info"][class_display_name] += 1

                            placed = True
                            break

                if not placed:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to place all students despite sufficient capacity",
                    )
        else:
            # For non-split option, still respect the class size limit if possible
            for student_data in all_students:
                placed = False
                class_id = student_data["classId"]

                # Try to place in a room where the class has fewer than max students
                for room in rooms:
                    if len(room["students"]) < room["capacity"]:
                        class_count = room["class_counts"].get(class_id, 0)
                        if class_count < max_per_class:
                            room["students"].append(student_data)
                            room["class_counts"][class_id] = class_count + 1

                            # Update class info for the room
                            class_display_name = student_data["className"]
                            if class_display_name not in room["class_info"]:
                                room["class_info"][class_display_name] = 0
                            room["class_info"][class_display_name] += 1

                            placed = True
                            break

                # If no room has space under the class limit, try any room with capacity
                if not placed:
                    for room in rooms:
                        if len(room["students"]) < room["capacity"]:
                            room["students"].append(student_data)
                            class_count = room["class_counts"].get(class_id, 0)
                            room["class_counts"][class_id] = class_count + 1

                            # Update class info for the room
                            class_display_name = student_data["className"]
                            if class_display_name not in room["class_info"]:
                                room["class_info"][class_display_name] = 0
                            room["class_info"][class_display_name] += 1

                            placed = True
                            break

                if not placed:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to place all students despite sufficient capacity",
                    )

    @staticmethod
    def _place_students_in_rooms(
        all_students: List[Tuple[str, int]],
        rooms: List[Dict],
        split: bool,
        max_per_class: int,
    ):
        """Place students in rooms with class distribution logic"""
        if split and len(rooms) > 1:
            # Place students in rooms with class distribution
            for student_roll, class_id in all_students:
                placed = False

                # First try rooms where this class has fewer than max students
                for room in rooms:
                    class_count = room["class_counts"].get(class_id, 0)
                    if (
                        len(room["students"]) < room["capacity"]
                        and class_count < max_per_class
                    ):
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
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to place all students despite sufficient capacity",
                    )
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
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to place all students despite sufficient capacity",
                    )
