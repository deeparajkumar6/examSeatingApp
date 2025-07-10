from fastapi import APIRouter
from typing import Dict
from ..models import StudentModel
from ..services import StudentService

router = APIRouter(prefix="/student", tags=["students"])

@router.get("/{class_id}", response_model=Dict)
def get_students_by_class(class_id: int):
    """Get all students in a specific class"""
    students = StudentService.get_students_by_class(class_id)
    return {"students": students}

@router.post("/{class_id}")
def add_student(class_id: int, student_data: StudentModel):
    """Add a new student to a class"""
    StudentService.create_student(class_id, student_data)
    return {"message": "Student added successfully"}

@router.delete("/{student_id}")
def delete_student(student_id: int):
    """Delete a student"""
    StudentService.delete_student(student_id)
    return {"message": "Student deleted successfully"}
