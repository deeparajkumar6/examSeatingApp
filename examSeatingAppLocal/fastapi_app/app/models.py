from pydantic import BaseModel
from typing import List, Optional, Dict

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

class ScheduleResponse(BaseModel):
    date: str
    seating_arrangement: Dict[str, List[str]]
