from fastapi import APIRouter
from typing import Dict
from ..models import ClassModel, ClassResponseModel
from ..services import ClassService

router = APIRouter(prefix="/class", tags=["classes"])

@router.get("", response_model=Dict)
def get_classes():
    """Get all classes with their students"""
    classes = ClassService.get_all_classes()
    return {"classes": classes}

@router.post("")
def add_class(class_data: ClassModel):
    """Add a new class with students"""
    ClassService.create_class(class_data)
    return {"message": "Class added successfully"}

@router.put("/{class_id}")
def update_class(class_id: int, class_data: ClassModel):
    """Update an existing class"""
    ClassService.update_class(class_id, class_data)
    return {"message": "Class updated successfully"}

@router.delete("/{class_id}")
def delete_class(class_id: int):
    """Delete a class and all its students"""
    ClassService.delete_class(class_id)
    return {"message": "Class deleted successfully"}
