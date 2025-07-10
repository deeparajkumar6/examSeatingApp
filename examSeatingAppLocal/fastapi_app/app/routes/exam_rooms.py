from fastapi import APIRouter
from typing import Dict
from ..models import ExamRoomModel
from ..services import ExamRoomService

router = APIRouter(prefix="/examRoom", tags=["exam_rooms"])

@router.get("", response_model=Dict)
def get_exam_rooms():
    """Get all exam rooms"""
    exam_rooms = ExamRoomService.get_all_exam_rooms()
    return {"examRooms": exam_rooms}

@router.post("")
def add_exam_room(room_data: ExamRoomModel):
    """Add a new exam room"""
    ExamRoomService.create_exam_room(room_data)
    return {"message": "Exam room added successfully"}

@router.put("/{room_id}")
def update_exam_room(room_id: int, room_data: ExamRoomModel):
    """Update an existing exam room"""
    ExamRoomService.update_exam_room(room_id, room_data)
    return {"message": "Exam room updated successfully"}

@router.delete("/{room_id}")
def delete_exam_room(room_id: int):
    """Delete an exam room"""
    ExamRoomService.delete_exam_room(room_id)
    return {"message": "Exam room deleted successfully"}
