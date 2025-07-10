from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class StudentModel(BaseModel):
    rollNumber: Optional[str] = None
    studentName: Optional[str] = None
    language: Optional[str] = None
    dateOfBirth: Optional[str] = None

class StudentResponseModel(StudentModel):
    id: int
    classId: int

class StudentUIModel(BaseModel):
    """UI-specific student model without rollNumber"""
    studentName: Optional[str] = None
    language: Optional[str] = None
    dateOfBirth: Optional[str] = None

class ClassModel(BaseModel):
    className: str
    shift: Optional[str] = None
    students: List[StudentModel] = []

class ClassUIModel(BaseModel):
    """UI-specific class model using StudentUIModel"""
    className: str
    shift: Optional[str] = None
    students: List[StudentUIModel] = []

class ClassResponseModel(BaseModel):
    id: int
    className: str
    shift: Optional[str] = None
    students: List[StudentResponseModel] = []

class BulkImportRequest(BaseModel):
    academicYear: Optional[str] = None

class BulkImportResponse(BaseModel):
    message: str
    classesCreated: int
    studentsCreated: int
    details: List[Dict]

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
