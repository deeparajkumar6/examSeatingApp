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
    shift: str  # Made mandatory
    students: List[StudentModel] = []

class ClassUIModel(BaseModel):
    """UI-specific class model using StudentUIModel"""
    className: str
    shift: str  # Made mandatory
    students: List[StudentUIModel] = []

class ClassResponseModel(BaseModel):
    id: int
    className: str
    shift: Optional[str] = None  # Keep optional for backward compatibility with existing data
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
    language_selections: Optional[Dict[int, List[str]]] = None  # New field: {class_id: [languages]}

class ScheduleResponse(BaseModel):
    date: str
    seating_arrangement: Dict[str, List[Dict]]  # Changed to List[Dict] to include student and class info
    class_summary: Optional[Dict[str, Dict[str, int]]] = None  # Room -> Class -> Count
    class_info: Optional[Dict[int, Dict[str, str]]] = None  # Class ID -> Class details
    language_summary: Optional[Dict[str, Dict[str, int]]] = None  # New: Room -> Language -> Count

class UserModel(BaseModel):
    username: str
    password: str
    name: str

class UserResponseModel(BaseModel):
    id: int
    username: str
    name: str
    created_at: str

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: UserResponseModel
